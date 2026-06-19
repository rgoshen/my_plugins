# GitLab CI

Reference for GitLab CI pipeline patterns — structure, DAG, conditional rules, caching, OIDC to AWS, environment gates, and security. Flag version-sensitive details as **verify via Context7** before use.

## Table of contents
- `.gitlab-ci.yml` structure
- `needs:` DAG for parallel jobs
- `rules:` and `workflow:rules:` for conditional jobs
- Caching and artifacts
- OIDC to AWS via `id_tokens`
- Environments and manual approval gates
- Security callout

---

## `.gitlab-ci.yml` structure

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

default:
  image: node:20-alpine    # default image for all jobs; pin to digest in production

lint:
  stage: lint
  script:
    - npm ci
    - npm run lint

test:
  stage: test
  script:
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'   # parse coverage from output

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour
```

Jobs in the same stage run in parallel. Jobs in later stages wait for all jobs in earlier stages to succeed (unless `needs:` overrides this — see below).

---

## `needs:` DAG for parallel jobs

The `needs:` keyword turns the pipeline into a directed acyclic graph (DAG), allowing a job to start as soon as its specific dependencies complete rather than waiting for a whole stage:

```yaml
stages:
  - test
  - build
  - deploy

unit-test:
  stage: test
  script: npm test

integration-test:
  stage: test
  script: npm run test:integration

build-app:
  stage: build
  needs: [unit-test]   # starts as soon as unit-test passes; doesn't wait for integration-test
  script: npm run build

deploy-staging:
  stage: deploy
  needs: [build-app, integration-test]
  script: ./deploy.sh staging
```

---

## `rules:` and `workflow:rules:` for conditional jobs

`rules:` replaces the older `only:`/`except:` syntax and supports complex conditions:

```yaml
deploy-prod:
  stage: deploy
  script: ./deploy.sh prod
  rules:
    # Only run on push to main, not on MRs
    - if: '$CI_COMMIT_BRANCH == "main" && $CI_PIPELINE_SOURCE == "push"'
      when: on_success
    - when: never
```

`workflow:rules:` controls whether the whole pipeline runs at all — useful to skip pipelines on certain commit message patterns or avoid duplicate pipelines on MR + push:

```yaml
workflow:
  rules:
    # Run on MRs
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    # Run on main branch push
    - if: '$CI_COMMIT_BRANCH == "main"'
    # Skip on tag pipelines if you handle tags separately
    - if: '$CI_COMMIT_TAG'
      when: never
```

---

## Caching and artifacts

**Cache** — persists files across pipeline runs (slow-changing, e.g. `node_modules`); keyed by a `key:` expression. Cache hits are best-effort; jobs must tolerate cache misses.

**Artifacts** — pass files between jobs within the same pipeline (build outputs, test reports). Artifacts are guaranteed; cache is not.

```yaml
# Cache example
test:
  cache:
    key:
      files:
        - package-lock.json    # cache key invalidates when lockfile changes
    paths:
      - node_modules/
    policy: pull-push   # pull at start, push at end (default); use 'pull' for read-only jobs

# Artifact example — pass built dist/ to the deploy job
build:
  artifacts:
    paths:
      - dist/
    reports:
      junit: test-results.xml   # surfaces test results in the MR UI
    expire_in: 2 hours

deploy:
  needs:
    - job: build
      artifacts: true   # explicitly request artifact download
```

---

## OIDC to AWS via `id_tokens`

GitLab CI can exchange a job-scoped OIDC token for short-lived AWS credentials without any long-lived keys. **Verify the `id_tokens` syntax and the OIDC provider URL format via Context7 — this feature and its syntax evolved across GitLab versions.**

```yaml
deploy:
  stage: deploy
  image: amazon/aws-cli:latest   # pin to digest in production
  id_tokens:
    AWS_OIDC_TOKEN:
      aud: https://sts.amazonaws.com   # audience must match the IAM OIDC provider config
  script:
    - |
      CREDENTIALS=$(aws sts assume-role-with-web-identity \
        --role-arn "${AWS_DEPLOY_ROLE_ARN}" \
        --role-session-name "gitlab-ci-${CI_JOB_ID}" \
        --web-identity-token "${AWS_OIDC_TOKEN}" \
        --duration-seconds 3600 \
        --output json)
      export AWS_ACCESS_KEY_ID=$(echo "$CREDENTIALS" | jq -r '.Credentials.AccessKeyId')
      export AWS_SECRET_ACCESS_KEY=$(echo "$CREDENTIALS" | jq -r '.Credentials.SecretAccessKey')
      export AWS_SESSION_TOKEN=$(echo "$CREDENTIALS" | jq -r '.Credentials.SessionToken')
    - aws s3 sync dist/ s3://${S3_BUCKET}/
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

**IAM trust policy (the AWS side):**  
The condition should bind to `gitlab.com:sub` (or your self-hosted GitLab URL). Scope to a specific project and optionally a specific branch or ref type. The HCL for the OIDC provider and role lives in IaC — see `iac-pipelines.md`.

---

## Environments and manual approval gates

Define environments in `.gitlab-ci.yml`; GitLab tracks deployments and allows rollback in the UI. Add `when: manual` to require human action before a job runs:

```yaml
deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script: ./deploy.sh staging
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

deploy-prod:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  when: manual        # pauses the pipeline; requires a human click to proceed
  allow_failure: false
  script: ./deploy.sh prod
  needs: [deploy-staging]
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

Use protected environments (GitLab settings) to restrict who can trigger `when: manual` jobs in production.

---

## Security callout

**Protected branches and variables.** Mark `main` and release branches as protected. Mark CI/CD variables that hold credentials as **protected** (only available on protected branches/tags) and **masked** (redacted in job logs). Never store plaintext credentials as unprotected, unmasked variables.

**Variable scoping.** Scope variables to specific environments rather than the whole project. GitLab allows environment-scoped variables — use them so prod credentials are never available in MR pipelines.

**Pin image digests.** Runner container images referenced by tag are mutable — the same tag can be silently updated to a compromised version. In production pipelines, pin images to their SHA digest:

```yaml
# Bad — mutable tag
image: node:20-alpine

# Good — pinned digest; resolve the current digest via Context7 or the registry
image: node@sha256:<digest>
```

**Secret scanning and SAST.** GitLab Ultimate/Gold includes built-in SAST and secret detection jobs that can be added with a template include:

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
```

Verify template names and compatibility with your GitLab version via Context7.

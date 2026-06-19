# Woodpecker CI

Reference for Woodpecker CI pipeline patterns — container-native structure, conditional steps, plugins, secrets, and security. Woodpecker CI is Apache-2.0 licensed, fully open-source, and self-hosted. **Verify syntax against your installed Woodpecker version via Context7 — the YAML schema has evolved across releases.**

## Table of contents
- Woodpecker model overview
- `.woodpecker.yml` structure
- `when:` conditions (branch and event)
- Plugins and `settings:`
- Secrets (`from_secret`)
- Security callout

---

## Woodpecker model overview

Woodpecker CI is a community-maintained, self-hosted CI system forked from Drone CI. Its key design characteristic is that **every step runs inside a container** — there is no host-level script execution. The CI server schedules work to agents; agents run pipeline steps as Docker containers against a specific workspace volume.

This means:
- No dependency on a shared runner image or hosted environment — you own the infrastructure.
- Each step declares its own image; steps share the workspace directory via a mounted volume.
- Plugin ecosystem (`plugins/*`) provides reusable containers for publishing, deploying, and notifying.
- Secret injection is handled server-side; secrets are never stored in the pipeline YAML.

---

## `.woodpecker.yml` structure

A minimal pipeline:

```yaml
# .woodpecker.yml
steps:
  lint:
    image: node:20-alpine    # pin to digest in production; see Security section
    commands:
      - npm ci
      - npm run lint

  test:
    image: node:20-alpine
    commands:
      - npm ci
      - npm test
    depends_on: [lint]   # explicit dependency ordering; steps run in parallel by default

  build:
    image: node:20-alpine
    commands:
      - npm ci
      - npm run build
    depends_on: [lint, test]
```

By default, steps without `depends_on` run in parallel. Declare explicit `depends_on` to enforce ordering.

Multiple pipelines can be defined in a single file or in a `.woodpecker/` directory (one file per pipeline):

```yaml
# .woodpecker/ci.yml  (alternative: split files for organization)
when:
  - event: pull_request

steps:
  test:
    image: node:20-alpine
    commands:
      - npm ci && npm test
```

---

## `when:` conditions (branch and event)

`when:` limits which events or branches trigger a step (or the whole pipeline). Conditions can be at the pipeline level or per-step:

```yaml
# Pipeline-level: only run this pipeline on push to main or on pull_request events
when:
  - event: push
    branch: main
  - event: pull_request

steps:
  test:
    image: node:20-alpine
    commands:
      - npm test

  deploy:
    image: alpine
    commands:
      - ./deploy.sh
    when:
      # Step-level override: only deploy on push to main, not on PRs
      - event: push
        branch: main
```

Common event values: `push`, `pull_request`, `tag`, `cron`, `manual`. **Verify event names against your Woodpecker version via Context7.**

---

## Plugins and `settings:`

Woodpecker plugins are Docker images that accept configuration via environment variables prefixed `PLUGIN_`. The `settings:` key in the pipeline YAML passes named values to these variables automatically:

```yaml
steps:
  publish:
    image: plugins/docker    # verify image digest via Context7; pin to digest
    settings:
      repo: myorg/myapp
      tags:
        - latest
        - ${CI_COMMIT_SHA}
      username:
        from_secret: DOCKER_USERNAME
      password:
        from_secret: DOCKER_PASSWORD
```

The `plugins/docker` image builds and pushes a Docker image using the workspace contents. Other common plugins: `plugins/s3` for S3 uploads, `plugins/slack` for notifications, `plugins/git` for submodule handling. Browse the official plugin index for the full list — verify plugin images are maintained before adopting.

Custom plugin: any Docker image that reads `PLUGIN_*` environment variables and exits 0/non-0 for success/failure is a valid Woodpecker plugin.

---

## Secrets (`from_secret`)

Secrets are managed in the Woodpecker server UI (or API) at the organization or repository level. They are never stored in pipeline YAML. Reference them with `from_secret:`:

```yaml
steps:
  deploy:
    image: amazon/aws-cli
    environment:
      AWS_ACCESS_KEY_ID:
        from_secret: AWS_ACCESS_KEY_ID
      AWS_SECRET_ACCESS_KEY:
        from_secret: AWS_SECRET_ACCESS_KEY
      AWS_DEFAULT_REGION: us-east-1
    commands:
      - aws s3 sync dist/ s3://$S3_BUCKET/
```

**Organization vs repository secrets:** Organization-scoped secrets are available to all repositories in the organization — use sparingly. Repository-scoped secrets are preferred for credentials specific to one service or deployment target.

**Pull request secret exposure:** By default, Woodpecker does not expose secrets to pipelines triggered by pull requests from forks (the `pull_request` event). This is the safe default — do not change it for secrets that hold production credentials.

---

## Security callout

**Pin plugin and base images to digests.** Plugin images referenced by tag (e.g. `plugins/docker:latest`) are mutable. A compromised image pushed under the same tag would be silently used in your next pipeline run. Pin to the SHA256 digest:

```yaml
# Bad — mutable tag
image: plugins/docker:latest

# Good — pinned digest; resolve via `docker pull plugins/docker && docker inspect` or Context7
image: plugins/docker@sha256:<digest>
```

**Scope secrets to the repositories that need them.** Avoid org-wide secrets for credentials that only one repository uses. Narrowing scope limits the blast radius of a compromised secret.

**Review plugin source code before adoption.** Because Woodpecker plugins are arbitrary Docker containers, inspect the plugin's Dockerfile and source — especially for third-party, community-maintained plugins — before granting them access to your credentials and workspace.

**Self-hosted infrastructure security.** Woodpecker agents run on your infrastructure. Ensure agents run with minimal host permissions (no privileged containers unless required), agents are network-isolated from internal services they don't need to reach, and the Woodpecker server API is not publicly exposed without authentication.

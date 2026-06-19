# GitHub Actions

Reference for GitHub Actions pipeline patterns — anatomy, caching, reusable workflows, OIDC to AWS, environment gates, and security. Flag version-sensitive details as **verify via Context7** before use.

## Table of contents
- Workflow / job / step anatomy
- Triggers (`on:`)
- Matrix builds
- Caching
- Reusable workflows and composite actions
- OIDC to AWS
- Environments and manual approval gates
- Security callout

---

## Workflow / job / step anatomy

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest    # verify current runner image via Context7
    permissions:
      contents: read          # set explicit permissions at job level

    steps:
      - uses: actions/checkout@v4   # pin to commit SHA in production; see Security section
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

Jobs within a workflow run in parallel by default. Use `needs:` to declare dependencies:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps: [...]

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps: [...]
```

---

## Triggers (`on:`)

```yaml
on:
  # Run on PRs targeting main
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  # Run on pushes to main (post-merge)
  push:
    branches: [main]

  # Allow manual trigger with optional inputs
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, prod]

  # Schedule (cron) — verify cron syntax in Actions docs
  schedule:
    - cron: '0 6 * * 1-5'
```

Use `paths:` filters to skip CI when only documentation changes:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package*.json'
    paths-ignore:
      - 'docs/**'
      - '*.md'
```

---

## Matrix builds

Test across multiple versions or platforms without duplicating job definitions:

```yaml
jobs:
  test:
    strategy:
      fail-fast: false   # continue other matrix legs if one fails
      matrix:
        node-version: ['18', '20', '22']
        os: [ubuntu-latest, windows-latest]

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci && npm test
```

---

## Caching

Cache package manager dependencies by lockfile hash so clean installs are only paid when dependencies actually change. **Verify the `actions/cache` action version via Context7 before pinning.**

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Cache node_modules
    uses: actions/cache@v4   # verify version via Context7
    with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-

  - run: npm ci
```

Many `setup-*` actions have built-in caching (`cache: 'npm'` input on `actions/setup-node`); prefer that over a manual cache step when available — fewer moving parts.

---

## Reusable workflows and composite actions

**Reusable workflow** — a whole workflow file called from another workflow via `workflow_call`. Use for shared CI pipelines (e.g., a shared test workflow used across repos):

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm test
```

Caller:

```yaml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets: inherit
```

**Composite action** — a reusable set of steps in `action.yml`; lighter than a reusable workflow and can be used as a single step. Good for shared setup sequences (checkout + cache + install):

```yaml
# .github/actions/setup-node-cache/action.yml
name: 'Setup Node with cache'
description: 'Checkout, setup Node, restore npm cache'
inputs:
  node-version:
    required: false
    default: '20'
runs:
  using: composite
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm
    - run: npm ci
      shell: bash
```

---

## OIDC to AWS

GitHub Actions can assume an AWS IAM role via OIDC without any long-lived credentials stored in repository secrets. The workflow gets a short-lived token; the IAM role trust policy restricts which repos and branches can assume it.

**Workflow side:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # required for OIDC token request
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4   # verify version via Context7; pin to commit SHA in production
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy-prod
          aws-region: us-east-1
          # No aws-access-key-id or aws-secret-access-key — OIDC only

      - name: Deploy
        run: aws s3 sync dist/ s3://my-bucket/
```

**IAM trust policy (the AWS side):**  
The trust policy lives in IaC — see `iac-pipelines.md` and the `devops-engineer` IaC skill for the HCL. The key claim to constrain is `token.actions.githubusercontent.com:sub`. Scope it to a specific repo and optionally a specific branch:

```json
{
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:ref:refs/heads/main"
    }
  }
}
```

Using a wildcard `repo:my-org/*` trust condition is overbroad — any repo in the org could assume the role.

---

## Environments and manual approval gates

Create environments (e.g. `staging`, `production`) in the repository settings and add required reviewers. The job pauses until a reviewer approves.

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com   # shown in the deployment UI
    needs: [deploy-staging]

    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh prod
```

Combine with `concurrency:` to prevent simultaneous deployments to the same environment:

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false   # don't cancel in-flight deploys; queue instead
```

---

## Security callout

**Pin third-party actions to commit SHAs.** Version tags are mutable; a compromised publisher can push malicious code under the same tag. Use the SHA of the release commit and keep a human-readable comment:

```yaml
# Bad — tag is mutable
- uses: aws-actions/configure-aws-credentials@v4

# Good — pinned to a commit SHA; resolve the current SHA via Context7 or the action's release page
- uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.x.x
```

Resolve current SHAs for your pinned actions via Context7 (`resolve-library-id` for the action, then `query-docs` for the latest release SHA) — do not trust examples in documentation.

**Minimal `permissions:` block.** Default permissions vary by repository settings. Always set explicit permissions at the workflow or job level and grant only what is needed:

```yaml
permissions:
  contents: read
  id-token: write    # only on jobs that need OIDC
  pull-requests: write  # only on jobs that post PR comments
```

**Fork PR protection.** Secrets are not exposed to workflows triggered by PRs from forks. Do not add workarounds (e.g. `pull_request_target` with `checkout` of untrusted code) — that is a well-documented RCE vector.

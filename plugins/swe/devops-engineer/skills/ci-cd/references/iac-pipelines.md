# IaC pipelines

Reference for CI/CD patterns around OpenTofu/Terraform — plan-on-PR, gated apply-on-merge, OIDC auth, state concurrency, and worked GitHub Actions snippets. The HCL conventions, state backend configuration, and IAM trust policy HCL belong to the `devops-engineer` IaC skill; this reference covers the pipeline YAML side of the bridge.

## Table of contents
- Plan-on-PR / apply-on-merge pattern
- `tofu fmt`, `tofu validate`, `tofu plan` as PR checks
- OIDC-to-AWS for the CI runner
- State and concurrency
- Worked GitHub Actions example

---

## Plan-on-PR / apply-on-merge pattern

IaC changes have a higher blast radius than application deploys: a bad `tofu apply` can destroy shared infrastructure. The core discipline is:

1. **Plan on PR** — run `tofu plan` on every pull request; post the plan output as an artifact or PR comment so reviewers can inspect the proposed diff before approving the merge.
2. **Gate the apply** — `tofu apply` only runs after the PR is merged to the main branch and (for high-risk environments) after a manual approval gate.
3. **Never apply on PR** — applying from a PR allows any author to execute arbitrary HCL against production state before peer review.

This mirrors the application deployment pattern (build-on-PR, deploy-on-merge) but with the added constraint that IaC changes affect shared state.

---

## `tofu fmt`, `tofu validate`, `tofu plan` as PR checks

Three lightweight checks serve as fast feedback on PRs:

| Check | What it catches | Cost |
|-------|----------------|------|
| `tofu fmt -check` | Formatting inconsistencies (fail-fast, no auth needed) | Seconds |
| `tofu validate` | Syntax and schema errors (requires provider init, no cloud API calls) | ~30s |
| `tofu plan` | Actual resource diff (requires cloud auth and state access) | Minutes |

Run `tofu fmt -check` and `tofu validate` early in the pipeline — they are cheap and catch the most obvious errors without needing cloud credentials. Run `tofu plan` after those pass, with the plan posted for human review.

**Post the plan as a PR comment:**  
Use the `github-script` action or a purpose-built action (e.g. `borchero/terraform-plan-comment`) to post the plan diff to the PR. This keeps the artifact visible in the review context. **Verify tool versions via Context7 before pinning — the ecosystem moves frequently.**

---

## OIDC-to-AWS for the CI runner

The CI runner needs read access to state and the ability to call AWS APIs for `tofu plan`, and write access for `tofu apply`. Use OIDC in both cases — no static keys.

**Two roles, two trust scopes** is the recommended pattern:
- **plan role** — `s3:GetObject`, `s3:ListBucket` on the state bucket, plus read-only permissions on the resources being planned. Trusted by any PR branch.
- **apply role** — `s3:GetObject`, `s3:PutObject` on the state bucket, plus write permissions on managed resources. Trusted **only** by the `main` branch (or the specific `apply` job ref).

The trust condition difference prevents a PR author from triggering an apply by crafting a workflow file, because the apply job only runs on `main` and only the apply role can write state.

**The IAM trust policy HCL** for these roles (the OIDC provider resource, the IAM role, and the trust policy) lives in IaC and is managed by the `devops-engineer` IaC skill. See `github-actions.md` and `gitlab-ci.md` for the workflow-side OIDC setup.

---

## State and concurrency

`tofu apply` acquires a state lock for the duration of the operation. Concurrent applies against the same state file will conflict: one will error with a lock failure. In CI, this can happen when:
- Two PRs merge to main in quick succession before the first apply completes.
- A manually triggered apply runs while an automated one is in progress.

**Serialize applies** using the CI platform's concurrency mechanism:

```yaml
# GitHub Actions — one apply at a time per state path
concurrency:
  group: tofu-apply-${{ github.ref }}
  cancel-in-progress: false   # queue; don't cancel in-flight applies
```

For GitLab CI, `resource_group:` achieves the same effect:

```yaml
deploy:
  resource_group: tofu-apply-prod
  script: tofu apply -auto-approve
```

`cancel-in-progress: false` (or the GitLab equivalent) is important — cancelling an in-flight `apply` mid-run can leave state in a partial/locked state.

---

## Worked GitHub Actions example

A complete two-job workflow: `plan` runs on PRs, `apply` runs on merge to `main` with a manual approval gate. **Verify action versions via Context7 — pin all third-party actions to commit SHAs in production.**

```yaml
# .github/workflows/tofu.yml
name: OpenTofu

on:
  pull_request:
    paths:
      - 'infra/**'
  push:
    branches: [main]
    paths:
      - 'infra/**'

env:
  TF_VERSION: "1.8.0"   # verify current OpenTofu version via Context7
  AWS_REGION: us-east-1
  WORKING_DIR: infra/environments/prod

concurrency:
  group: tofu-apply-${{ github.ref }}
  cancel-in-progress: false

jobs:
  plan:
    name: Plan
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    permissions:
      contents: read
      id-token: write
      pull-requests: write   # to post plan as PR comment

    steps:
      - uses: actions/checkout@v4   # pin to SHA in production

      - name: Set up OpenTofu
        uses: opentofu/setup-opentofu@v1   # verify version + SHA via Context7
        with:
          tofu_version: ${{ env.TF_VERSION }}

      - name: Configure AWS credentials (plan role)
        uses: aws-actions/configure-aws-credentials@v4   # pin to SHA
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-tofu-plan
          aws-region: ${{ env.AWS_REGION }}

      - name: tofu fmt check
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu fmt -check -recursive

      - name: tofu init
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu init

      - name: tofu validate
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu validate

      - name: tofu plan
        id: plan
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu plan -out=tfplan -no-color 2>&1 | tee plan.txt

      - name: Post plan to PR
        if: always()
        uses: actions/github-script@v7   # pin to SHA
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.WORKING_DIR }}/plan.txt', 'utf8');
            const maxLen = 65000;
            const body = plan.length > maxLen
              ? plan.substring(0, maxLen) + '\n...(truncated)'
              : plan;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '```\n' + body + '\n```'
            });

  apply:
    name: Apply
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment:
      name: production    # requires manual approval from a configured reviewer
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up OpenTofu
        uses: opentofu/setup-opentofu@v1
        with:
          tofu_version: ${{ env.TF_VERSION }}

      - name: Configure AWS credentials (apply role)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-tofu-apply
          aws-region: ${{ env.AWS_REGION }}

      - name: tofu init
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu init

      - name: tofu apply
        working-directory: ${{ env.WORKING_DIR }}
        run: tofu apply -auto-approve
```

**Key decisions in this example:**
- Two separate IAM roles (`plan` vs `apply`) with different trust conditions — the apply role requires `ref:refs/heads/main`.
- `environment: production` with required reviewers pauses the apply job for human sign-off.
- `concurrency.cancel-in-progress: false` queues applies rather than cancelling in-flight ones.
- `paths:` filter avoids triggering the pipeline on unrelated changes.
- Action versions use the tag form in this example for readability — **pin all third-party actions to commit SHAs in production** (see `pipeline-security.md`).

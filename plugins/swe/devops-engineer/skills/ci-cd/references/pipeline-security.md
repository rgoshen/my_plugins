# Pipeline security

Reference for securing CI/CD pipelines — OIDC over static keys, action/image pinning, secret handling, least-privilege permissions, and supply chain. This is a checklist-first topic: security debt in pipelines is uniquely dangerous because pipelines run with elevated cloud credentials and direct access to production.

## Table of contents
- OIDC over static keys
- Pin third-party actions and images to commit SHAs / digests
- Secret handling
- Least-privilege permissions
- Supply chain (dependency scanning, SBOM, provenance)
- Review checklist

---

## OIDC over static keys

Long-lived cloud credentials stored in CI secrets are the single highest-risk item in most pipelines. A leaked `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` pair provides persistent, policy-bounded access to your AWS account. Rotating them is manual and often deferred.

**OIDC eliminates this risk** by letting the CI platform generate a short-lived, job-scoped JWT that the cloud provider (AWS, GCP, Azure) exchanges for temporary credentials. The JWT is valid for the duration of one job and cannot be reused.

| | Static keys | OIDC |
|---|---|---|
| Credential lifetime | Until rotated (often never) | Minutes (one job) |
| Leak impact | Persistent access | Expires automatically |
| Rotation burden | Manual | None |
| Scope control | IAM policy only | IAM policy + trust condition (repo, branch, ref) |

**How OIDC scoping works:**  
The IAM role trust policy includes a condition on the CI platform's JWT subject claim (`sub`). For GitHub Actions, the `sub` claim encodes the repository and ref:

```
repo:my-org/my-repo:ref:refs/heads/main
```

This means only jobs running on `main` in `my-org/my-repo` can assume the role. For GitLab CI, the claim encodes the project path and pipeline source. Scope the condition as narrowly as possible — environment, branch, or even specific pipeline source.

**Worked OIDC setup:** see `github-actions.md` (GitHub) and `gitlab-ci.md` (GitLab) for the workflow YAML; the IAM trust policy HCL belongs to the `devops-engineer` IaC skill.

---

## Pin third-party actions and images to commit SHAs / digests

Version tags (e.g. `actions/checkout@v4`, `node:20-alpine`) are **mutable references** — the tag can be updated to point to any commit, including a compromised one, without any change to your pipeline YAML. This is a supply chain attack vector.

**The fix: pin to an immutable reference.**

For GitHub Actions — pin to the commit SHA of the release, not the tag:

```yaml
# Bad — mutable tag
- uses: actions/checkout@v4

# Good — pinned commit SHA with a human-readable comment
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Resolve the current SHA: check the action's GitHub releases page, or use Context7 (`resolve-library-id` for the action, then `query-docs` for the latest release). Do not trust SHA examples in documentation — they age.

For container images — pin to the manifest digest:

```yaml
# Bad
image: node:20-alpine

# Good — pinned manifest digest
image: node@sha256:<digest>   # resolve via: docker pull node:20-alpine && docker inspect node:20-alpine --format '{{index .RepoDigests 0}}'
```

**Updating pinned references:** Dependabot (GitHub) and Renovate can automate PRs that update pinned SHAs when new releases come out, keeping security patches flowing without manual tracking.

---

## Secret handling

**Masking.** CI platforms mask known secret values in logs — but only if you use the platform's secret mechanism, not plaintext environment variables hard-coded in YAML. Always inject secrets through the platform's secret store.

**Scoping.** Scope secrets to the narrowest available context:
- In GitHub Actions: environment-scoped secrets are only available to jobs targeting that environment. Repository secrets are available to all jobs — use sparingly.
- In GitLab CI: protect and mask variables; scope to specific environments.
- In Woodpecker CI: prefer repository-scoped secrets over organization-scoped.

**Never echo secrets.** Do not `echo $SECRET` or print environment variables in debug output. If a step must inspect its environment, scrub secrets from the output.

**Fork PR protection.** Secrets must not be accessible to pipelines triggered by pull requests from external forks. This is the default safe behavior on GitHub Actions (`pull_request` event) and Woodpecker CI. Do not use `pull_request_target` to check out untrusted fork code in a context with secret access — this is a well-documented remote code execution vector.

---

## Least-privilege permissions

**GitHub Actions `permissions:` block.** The default token permissions vary by repository settings (and can be permissive). Always set an explicit block:

```yaml
# At workflow level — applies to all jobs unless overridden
permissions:
  contents: read

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write    # only jobs that need OIDC
```

Grant `id-token: write` only to jobs that request an OIDC token. Grant `pull-requests: write` only to jobs that post PR comments.

**IAM roles.** CI deploy roles should follow least-privilege: `s3:PutObject` on a specific bucket prefix, `ecs:RegisterTaskDefinition` + `ecs:UpdateService` on specific clusters, never `*`. Audit role policies on a regular cadence. Use AWS IAM Access Analyzer to surface unused permissions.

**Scoped runner tokens.** In self-hosted runner setups (GitHub Actions self-hosted, GitLab runners, Woodpecker agents), the runner host should not have credentials other than the OIDC exchange capability. Avoid running runners with instance profiles that grant broader-than-needed access.

---

## Supply chain

**Dependency scanning.** Run a dependency scanner in CI to surface known CVEs in your transitive dependency tree. Tools: Dependabot (GitHub-native), Trivy, Grype, Snyk. Block on high/critical severity with exceptions for false positives.

**SBOM generation.** On production builds, generate a Software Bill of Materials capturing the exact dependency graph. Tools: Syft (SPDX or CycloneDX output). Store the SBOM as a build artifact alongside the container image or release binary.

**Build provenance / attestation.** GitHub Actions supports SLSA-grade build provenance attestation, recording what workflow produced a given artifact. Combined with `gh attestation verify`, this lets downstream consumers verify the artifact was built from a specific workflow, not modified post-build. Sigstore (Cosign) provides a similar capability for container images.

These controls are defense-in-depth — most teams start with dependency scanning and pin-to-SHA, then add SBOM and attestation as the deployment criticality warrants.

---

## Review checklist

Run this checklist when reviewing any pipeline configuration:

**Critical — fix before merge:**
- [ ] No long-lived cloud credentials (AWS keys, GCP service account keys) stored as CI secrets; OIDC used instead
- [ ] All third-party actions pinned to commit SHAs, not version tags or branch refs
- [ ] Container images pinned to digest in production pipelines
- [ ] Secrets accessed via the platform's secret mechanism, not hard-coded in YAML
- [ ] No secrets echoed or printed in job output
- [ ] Explicit `permissions:` block at workflow or job level; no broad defaults
- [ ] `pull_request_target` not used with checkout of untrusted fork code

**High — fix in same PR if possible:**
- [ ] OIDC trust conditions scoped to specific repository and branch (not org-wide wildcard)
- [ ] Secrets scoped to the environment that needs them, not the whole repository
- [ ] IAM roles used by the pipeline follow least-privilege; reviewed recently

**Medium — track as follow-up:**
- [ ] Dependency scanning job present and blocking on high/critical CVEs
- [ ] SBOM generated on release builds
- [ ] Pinned SHA update process automated (Dependabot, Renovate)
- [ ] Self-hosted runner isolation reviewed (if applicable)

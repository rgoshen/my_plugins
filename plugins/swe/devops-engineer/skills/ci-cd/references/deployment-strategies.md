# Deployment strategies

Reference for deployment strategies — mechanics, tradeoffs, rollback behavior, and a comparison table. Choose the strategy based on acceptable downtime, rollback requirements, infra cost, and team/tooling complexity.

## Table of contents
- Recreate
- Rolling
- Blue-green
- Canary
- Manual gates and environments
- Rollback
- Comparison table

---

## Recreate

Stop all instances of the current version, then start the new version. The simplest possible strategy.

**How it works:** The load balancer drains connections; the old version is terminated; the new version starts and health checks pass; traffic resumes.

**Downtime profile:** Guaranteed downtime during the gap between old termination and new startup. Duration depends on startup time and warmup.

**When to use:**
- Non-production environments where brief downtime is acceptable.
- Single-instance or non-redundant deployments (development, local CI mirrors).
- Services that cannot run two versions simultaneously due to state or schema incompatibility.

**Rollback:** Deploy the previous artifact/image; same downtime window as the original deploy.

---

## Rolling

Replace instances one at a time (or in small batches), keeping the majority of capacity serving traffic during the rollout.

**How it works:** The orchestrator (Kubernetes, ECS, etc.) terminates one instance, starts a replacement running the new version, waits for health checks, then proceeds to the next. Batch size is configurable.

**Downtime profile:** No planned downtime if the batch size keeps enough healthy instances in rotation. Risk: mixed-version traffic during rollout (old and new versions serve requests simultaneously — ensure backward-compatible changes).

**When to use:**
- Applications where the new and old versions can coexist (no database schema changes that break the old version).
- Kubernetes Deployments with a `RollingUpdate` strategy (the default).
- When blue-green's infra cost is not justified.

**Rollback:** Update the Deployment image back to the previous tag/digest; the rolling process reverses. Rollback is faster than recreate but still runs two versions simultaneously during the reversal.

---

## Blue-green

Two full, identical environments ("blue" and "green") exist simultaneously. Only one is live at a time. To deploy, bring the idle environment up with the new version, validate it, then cut traffic over via the load balancer or DNS.

**How it works:**
1. Blue is currently live.
2. Deploy new version to green.
3. Run smoke tests / health checks against green (before it receives real traffic).
4. Shift load balancer target from blue to green.
5. Keep blue warm for a rollback window (then decommission or use as next deployment target).

**Downtime profile:** Near-zero — the cutover is a DNS or load balancer change, typically milliseconds.

**Rollback:** Shift the load balancer back to blue. Instant.

**When to use:**
- High-traffic production services where zero-downtime and instant rollback are required.
- Regulated environments where pre-prod validation before traffic switch is required.
- When infra cost of running two environments is justified by the rollback/safety requirement.

**What it costs:**
- Double the compute/memory cost during the deployment window.
- Stateful services (databases, caches) must handle connections from both environments or be carefully migrated.

---

## Canary

Route a small fraction of production traffic to the new version, monitor key metrics (error rate, latency, business metrics), and gradually increase the percentage. If metrics degrade, roll back automatically or via a human gate.

**How it works:**
1. Deploy the new version to a subset of instances or via weighted routing rules.
2. Send e.g. 5% of traffic to the new version, 95% to the old.
3. Monitor for a defined bake time (e.g. 15 minutes, 1 hour).
4. If metrics pass thresholds, promote: 25% → 50% → 100%.
5. If metrics degrade, shift traffic back to 0% and roll back.

**Downtime profile:** None — only a fraction of users hit the new version.

**When to use:**
- High-confidence production deploys where real traffic validation is needed before full rollout.
- Services with clear SLIs (error rate, p99 latency) that can drive automated promotion/rollback.
- Organizations with progressive delivery infrastructure (Argo Rollouts, Flagger, feature flag platforms).

**What it costs:**
- Highest operational complexity of any strategy.
- Requires robust metric collection and defined thresholds before it can automate.
- Both versions serve real users simultaneously — changes must be backward-compatible (same database schema constraint as rolling).

---

## Manual gates and environments

All strategies benefit from environment-scoped manual approval gates for production deploys:

- **In GitHub Actions:** use `environment:` with required reviewers in the repo settings. The job pauses until approval.
- **In GitLab CI:** use `when: manual` on the deploy job and protect the environment to restrict who can approve.
- **In Woodpecker CI:** pause with a `when: event: manual` step or use an external gate (e.g., a Slack approval webhook).

Manual gates are essential for:
- Regulated environments requiring change-board sign-off.
- Production deploys with high blast radius.
- Any deploy that needs a human to verify the staging/canary results before proceeding.

---

## Rollback

A safe rollback depends on **immutable, versioned artifacts**:

- Container images tagged with the git SHA or semantic version, stored in a registry that supports immutable tags.
- Release artifacts (binaries, packages) stored with version in the filename or object key.
- IaC state versions (S3-versioned state bucket) that allow reverting to the last known-good state.

**Database migration caveat:** Database schema changes are the hardest part of rollback. The pattern that preserves rollback capability:
1. Deploy the new version of the app alongside the *old* schema (no breaking changes — additive column, nullable, with a default).
2. Migrate data in a background job or post-deploy step.
3. Only after the new version is stable, run the cleanup migration (drop old column, add constraint).

This "expand / migrate / contract" pattern means you can roll back the app code at any point in steps 1–2 without the schema fighting you.

---

## Comparison table

| Strategy | Downtime | Rollback speed | Extra infra cost | Complexity |
|----------|----------|----------------|------------------|------------|
| Recreate | Planned window | Same as deploy | None | Very low |
| Rolling | None (if sized correctly) | Medium (reruns rolling update in reverse) | None | Low |
| Blue-green | Near-zero | Instant (load balancer flip) | ~2× during window | Medium |
| Canary | None | Fast (shift traffic to 0%) | Partial (canary instances) | High |

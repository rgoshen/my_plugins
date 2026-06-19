# Branching models

Reference for GitHub Flow, GitFlow, and trunk-based development — mechanics, tradeoffs, and a decision guide. No house default; the right model depends on your team and release cadence.

## Table of contents
- GitHub Flow
- GitFlow
- Trunk-based development
- Decision guide
- Hotfix and release mechanics

---

## GitHub Flow

Single long-lived branch (`main`), short-lived feature branches, merge via pull request with required CI checks, deploy from `main`.

**How it works:**
1. Create a branch from `main` (e.g. `feature/add-login`).
2. Commit, push; open a PR with required status checks.
3. Review and approve; merge to `main`.
4. `main` triggers deployment automatically or on a manual gate.

**When it fits:**
- Teams practicing continuous deployment (one or more releases per day).
- SaaS products with a single production version.
- Small-to-medium teams that value simplicity over ceremony.
- No simultaneous maintenance of multiple released versions.

**What it costs:**
- Requires feature flags for long-running work to avoid blocking main.
- No structured release window — every merge is potentially deployable, which can surprise stakeholders used to scheduled releases.
- Hotfix discipline matters: because main is always release-ready, a hotfix is just a normal branch-and-PR cycle.

---

## GitFlow

Two long-lived branches (`main` and `develop`), plus structured short-lived branches: `feature/`, `release/`, and `hotfix/`. Many teams (including projects with their own CLAUDE.md mandating GitFlow) choose this model.

**Branch purposes:**
| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code only; tagged with each release |
| `develop` | Integration branch; the base for feature branches |
| `feature/*` | New functionality; branch off `develop`, merge back to `develop` |
| `release/*` | Pre-release stabilization; branch off `develop`, merged to both `main` and `develop` |
| `hotfix/*` | Urgent prod fixes; branch off `main`, merged to both `main` and `develop` |

**When it fits:**
- Products with a defined release cadence (weekly, monthly, quarterly).
- Versioned libraries or APIs where multiple versions are maintained simultaneously.
- Environments requiring a formal change window, release sign-off, or audit trail per release.
- Larger teams that need clear ownership of "what's going to production next."

**What it costs:**
- More branch overhead and merge ceremony than GitHub Flow.
- `develop` can lag `main` after hotfixes if the merge-back is missed.
- Not well-suited to continuous deployment — the release branch exists to slow things down, which is a feature or a bug depending on your situation.

---

## Trunk-based development

All developers commit to a single trunk (often `main` or `trunk`) or use very short-lived branches (< 1 day). Integration is continuous; long-running work ships behind feature flags.

**How it works:**
- Developers push small, complete commits to trunk several times per day.
- Automated test coverage must be high — trunk must be deployable at all times.
- Feature flags gate incomplete features from users while work progresses.
- CI runs on every commit; any red build is fixed immediately (not scheduled for next sprint).

**When it fits:**
- High-deploy-frequency teams (tens of deploys per day, or want to get there).
- Organizations investing heavily in automated testing and progressive delivery infrastructure.
- Teams that find long-running branches the root cause of integration pain.

**What it costs:**
- Feature flag discipline: flags must be added, managed, and cleaned up; flag debt accumulates if not actively pruned.
- Requires high automated test coverage and fast CI — a slow or flaky pipeline defeats the model.
- Not well-suited to maintaining multiple shipped versions simultaneously.

---

## Decision guide

Use the signals below to anchor the conversation. No model is universally superior; most teams make their choice once and stay there (switching has a real migration cost).

| Signal | Points toward |
|--------|--------------|
| Deploy frequency ≥ 1/day, SaaS product | GitHub Flow or trunk-based |
| Deploy frequency weekly or slower | GitFlow |
| Versioned library / product (v1, v2 shipped simultaneously) | GitFlow |
| Regulatory / audit requirement for formal release records | GitFlow |
| Team size < 10, single product version | GitHub Flow |
| Team invests heavily in feature flags and automated testing | Trunk-based |
| Scheduled release trains (release every sprint end) | GitFlow |
| Continuous delivery, fast iteration, minimal ceremony | GitHub Flow or trunk-based |
| Multiple long-running environment tiers (dev / staging / prod with different cadences) | GitFlow or GitHub Flow with environment gates |

When in doubt, default to the model already in place — switching branching models mid-stream causes noise without guaranteed improvement.

---

## Hotfix and release mechanics

### GitHub Flow
An urgent prod fix is a normal branch-and-PR cycle — there is no dedicated hotfix branch type. Discipline: keep the fix minimal and the PR review fast.

```
main ──●──────────────────●── (tagged release)
        \                /
         hotfix/login-500
```

### GitFlow
Hotfix branches from `main`, not `develop`. This preserves `develop`'s unreleased changes while patching production. After merging to `main` (tag the release), **immediately merge back to `develop`** — skipping this step is the single most common GitFlow mistake.

```
main    ──●─────────────────────●──  (tag v1.2.1)
           \                   /
            hotfix/login-500  /
                              ↓
develop ──●───────────────────●──  (merge-back)
```

### Trunk-based
Hot fixes commit directly to trunk (or via a very short-lived branch). Since trunk is always deployable, the fix ships on the next deployment cycle, which in a high-frequency team is usually minutes. For environments with lower deploy cadence, a short-lived `release/` branch can be used.

### Release branch (GitFlow)
A `release/1.3.0` branch forks off `develop` when the feature set is frozen. Only bug fixes go in; new features wait for the next cycle. Once stable, merge to `main` (tag) and back to `develop`.

```
develop ──●──●─────────────────●──  (continuing features)
              \               /
               release/1.3.0 /
                             ↓
main    ──────────────────────●──  (tag v1.3.0)
```

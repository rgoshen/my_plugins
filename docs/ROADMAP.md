# Roadmap

This document tracks planned releases and features for the `my_plugins` marketplace.

> Issues and milestones are the source of truth — this file provides human-readable context.
> See the [GitHub Milestones](https://github.com/rgoshen/my_plugins/milestones) for live progress.

---

## Released

### v0.0.x — cs-tutor bootstrap
Initial plugin with `arch-tutor` and `pl-tutor` agents and the `session-state-manager` shared skill.

### v0.1.0 — cs-tutor
Core language and architecture tutors. `arch-teach` and `pl-teach` skills added.

### v0.2.0 — cs-tutor (current)
Shared session infrastructure and core tutor skills.

### v0.1.0 — devops-engineer (swe family)
**Plugin:** `devops-engineer` | First plugin in the `swe` family (`plugins/swe/`). Senior DevOps/platform-engineering specialist for OpenTofu, Terraform, IaC, and AWS — inline skill + delegated sub-agent with Context7 lookup.

### v0.1.0 — ai-engineer (swe family)
**Plugin:** `ai-engineer` | Second plugin in the `swe` family (`plugins/swe/`). Senior AI/ML engineer — a self-contained decision-framework sub-agent plus nine indexed skills (RAG, evaluation, security, model selection, inference, agent design, fine-tuning, deployment), wired to Context7.

---

## Planned

### v0.3.0 — cs-tutor Tier 1
**Plugin:** `cs-tutor` | **Milestone:** [v0.1.0](https://github.com/rgoshen/my_plugins/milestone/5)

Foundation infrastructure + first-tier tutors covering the core CS curriculum.

| Issue | Tutor | Track |
|---|---|---|
| [#8](https://github.com/rgoshen/my_plugins/issues/8) | shared session-prelude skill | infrastructure |
| [#9](https://github.com/rgoshen/my_plugins/issues/9) | software-design-teach | design |
| [#10](https://github.com/rgoshen/my_plugins/issues/10) | dsa-teach | foundations |
| [#11](https://github.com/rgoshen/my_plugins/issues/11) | databases-teach | systems |
| [#12](https://github.com/rgoshen/my_plugins/issues/12) | design-patterns-teach | design |
| [#13](https://github.com/rgoshen/my_plugins/issues/13) | system-design-teach | systems |
| [#14](https://github.com/rgoshen/my_plugins/issues/14) | security-fundamentals-teach | security |
| [#15](https://github.com/rgoshen/my_plugins/issues/15) | web-dev-teach | web |

---

### v0.4.0 — cs-tutor Tier 2
**Plugin:** `cs-tutor` | **Milestone:** [v0.2.0](https://github.com/rgoshen/my_plugins/milestone/6)

Intermediate tutors covering systems, foundations, and SE practice.

| Issue | Tutor | Track |
|---|---|---|
| [#16](https://github.com/rgoshen/my_plugins/issues/16) | linear-algebra-teach | foundations |
| [#17](https://github.com/rgoshen/my_plugins/issues/17) | probability-stats-teach | foundations |
| [#18](https://github.com/rgoshen/my_plugins/issues/18) | os-teach | systems |
| [#19](https://github.com/rgoshen/my_plugins/issues/19) | networks-teach | systems |
| [#20](https://github.com/rgoshen/my_plugins/issues/20) | distributed-systems-teach | systems |
| [#21](https://github.com/rgoshen/my_plugins/issues/21) | testing-teach | se-practice |
| [#22](https://github.com/rgoshen/my_plugins/issues/22) | appsec-teach | security |
| [#23](https://github.com/rgoshen/my_plugins/issues/23) | devops-teach | se-practice |

---

### v0.5.0 — cs-tutor Tier 3
**Plugin:** `cs-tutor` | **Milestone:** [v0.3.0](https://github.com/rgoshen/my_plugins/milestone/7)

Advanced tutors covering AI/ML, compilers, and professional SE practice.

| Issue | Tutor | Track |
|---|---|---|
| [#24](https://github.com/rgoshen/my_plugins/issues/24) | ml-teach | ai-ml |
| [#25](https://github.com/rgoshen/my_plugins/issues/25) | deep-learning-teach | ai-ml |
| [#26](https://github.com/rgoshen/my_plugins/issues/26) | llm-teach | ai-ml |
| [#27](https://github.com/rgoshen/my_plugins/issues/27) | compilers-teach | foundations |
| [#28](https://github.com/rgoshen/my_plugins/issues/28) | computer-org-teach | foundations |
| [#29](https://github.com/rgoshen/my_plugins/issues/29) | clean-code-teach | design |
| [#30](https://github.com/rgoshen/my_plugins/issues/30) | api-design-teach | se-practice |
| [#31](https://github.com/rgoshen/my_plugins/issues/31) | sre-teach | se-practice |
| [#32](https://github.com/rgoshen/my_plugins/issues/32) | discrete-math-teach | foundations |

---

### v0.6.0 — project-scaffolding plugin
**Plugin:** `project-scaffolding` (new) | **Milestone:** [v0.4.0](https://github.com/rgoshen/my_plugins/milestone/8)

New plugin for scaffolding standard project files from `~/.claude/templates/` on demand.

| Issue | Feature |
|---|---|
| [#37](https://github.com/rgoshen/my_plugins/issues/37) | template-manager skill |

---

### swe family (planned)
**Folder:** `plugins/swe/` | Each role is its own standalone plugin, a senior-engineer persona like `devops-engineer`. Milestones TBD.

| Issue | Plugin | Focus |
|---|---|---|
| [#41](https://github.com/rgoshen/my_plugins/issues/41) | `backend-engineer` | APIs, services, data modeling, service design |
| [#42](https://github.com/rgoshen/my_plugins/issues/42) | `frontend-engineer` | UI architecture, state, accessibility, performance |
| [#43](https://github.com/rgoshen/my_plugins/issues/43) | `sre` | SLOs, observability, incident response, reliability |
| [#44](https://github.com/rgoshen/my_plugins/issues/44) | `security-engineer` | Threat modeling, OWASP, secure design review |
| [#45](https://github.com/rgoshen/my_plugins/issues/45) | `software-architect` | System design, architecture tradeoffs, ADRs |

---

## Plugin Registry

| Plugin | Status | Latest Version | Description |
|---|---|---|---|
| `cs-tutor` | active | v0.2.0 | Senior-engineer mentors for CS topics |
| `devops-engineer` | active | v0.1.0 | Senior DevOps specialist (OpenTofu/Terraform/IaC/AWS) |
| `project-scaffolding` | planned | — | Scaffold project files from templates |
| `ai-engineer` | active | v0.1.0 | Senior AI engineer agent and skills |

---
title: devops-engineer
layout: default
parent: Plugins
nav_order: 2
---

# devops-engineer

![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)
![CI](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Senior DevOps/platform-engineering specialist for OpenTofu, Terraform, IaC, and AWS. Two entry points share one body of conventions: an inline skill that activates on IaC/AWS context, and a delegated sub-agent for multi-step work. Wired to Context7 for live documentation lookup.
{: .fs-5 }

---

## Prerequisites

### Context7 MCP

The plugin ships a Context7 MCP server (`.mcp.json`) for live provider/version/AWS documentation lookup. Claude Code prompts to approve it on first use. If you already have Context7 configured globally, `/doctor` may note a duplicate server — expected and harmless.

---

## Install

```
/plugin marketplace add rgoshen/my_plugins
/plugin install devops-engineer@my-plugins
```

---

## Components

### Commands

| Command | Description |
|---|---|
| `/devops-engineer:devops-engineer` | Invoke the DevOps engineer skill directly for IaC/AWS work |

### Agents

| Agent | Description |
|---|---|
| `devops-engineer` | Delegated sub-agent for multi-step IaC/AWS work in its own context; preloads the skill and enforces Context7 lookup. Invoke as `@devops-engineer:devops-engineer`. |

### Skills

| Skill | Description |
|---|---|
| `devops-engineer` | Senior DevOps expertise — write/review/advise modes, OpenTofu-first defaults, security-first review, read-the-repo-before-prescribing. Auto-activates on `.tf`/`.tofu` files, tofu/terraform commands, plan/apply errors. |

---

## How it works

- **Inline skill**: just start working on IaC/AWS — it activates on context. Quick hits and mid-conversation expertise.
- **Sub-agent**: delegate multi-step work (audits, module writing, debugging plan/apply/state errors). It runs in its own context and returns a self-contained summary, leading with the highest-severity findings.
- **One body of conventions**: the agent preloads the skill via `skills:` frontmatter, so there's no duplication drift. Concrete HCL patterns live in `references/conventions.md`.

---

## Philosophy

- **Read the repo before prescribing.** Match existing style; escalate hard on safety (IAM `*`, open SGs, unencrypted/public storage, secrets in state) regardless of repo convention.
- **OpenTofu first** for greenfield, with Terraform as the parenthetical; match the repo if it's already on Terraform.
- **Look it up, don't guess.** Version-sensitive provider/AWS facts go through Context7 before being asserted, then cited.
- **Security-first review.** Highest-severity issues lead; style nits never bury a critical finding.

---

## Changelog

See [CHANGELOG.md](https://github.com/rgoshen/my_plugins/blob/main/plugins/swe/devops-engineer/CHANGELOG.md).

---

## Source

[github.com/rgoshen/my_plugins/tree/main/plugins/swe/devops-engineer](https://github.com/rgoshen/my_plugins/tree/main/plugins/swe/devops-engineer)

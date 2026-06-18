# Changelog

All notable changes to the `devops-engineer` plugin.

## [0.1.0] - 2026-06-18

### Added
- Initial release. Imported into the `my_plugins` marketplace under `plugins/swe/`.
- `devops-engineer` skill — senior DevOps/platform-engineering expertise for OpenTofu, Terraform, IaC, and AWS. Three modes (write / review / advise), read-the-repo-before-prescribing rule, OpenTofu-first defaults, security-first review priority, and a self-critique habit. Auto-activates on `.tf`/`.tofu` files, tofu/terraform commands, and plan/apply/state errors; also invocable as `/devops-engineer:devops-engineer`.
- `devops-engineer` sub-agent — delegated, own-context variant that enforces Context7 documentation lookup harder than the inline skill.
- `references/conventions.md` — concrete HCL patterns (repo layout, `versions.tf`, S3 native locking, provider `default_tags`, module-per-resource-group composition).
- Context7 MCP server (`.mcp.json`) for live provider/version/AWS documentation lookup.

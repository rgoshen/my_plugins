---
title: Home
layout: home
nav_order: 1
---

# my-plugins

A personal [Claude Code](https://claude.ai/code) plugin marketplace by Rick Goshen.

[![Build](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/rgoshen/my_plugins/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/rgoshen/my_plugins/blob/main/LICENSE)

---

## Install this marketplace

```
/plugin marketplace add rgoshen/my_plugins
```

Once added, browse and install individual plugins:

```
/plugin install <plugin-name>@my-plugins
```

---

## Available plugins

| Plugin | Category | Description |
|---|---|---|
| [cs-tutor](./plugins/cs-tutor) | Education | Senior-engineer mentors for architecture patterns and programming language learning |

---

## How it works

Claude Code plugin marketplaces are git-hosted catalogs. When you add this marketplace, Claude Code clones the repository and makes plugins available to install. Installed plugins provide agents, skills, and slash commands that extend Claude Code directly.

For details on how this marketplace is structured, see the [GitHub repository](https://github.com/rgoshen/my_plugins).

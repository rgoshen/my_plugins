# Conventions: concrete patterns

Code patterns implementing the house style. Read when writing greenfield HCL or doing a standardization pass. Adapt to repo conventions where they already exist. Version-sensitive details are flagged for Context7 verification — they drift.

## Table of contents
- Repo layout
- versions.tf (pinning + OpenTofu)
- S3 backend with native locking
- Provider default_tags
- Module-per-resource-group composition

## Repo layout

```
infra/
├── modules/
│   ├── networking/     # vpc, subnets, routes, nat, sg
│   ├── data/           # rds, s3, dynamodb, elasticache
│   ├── compute/        # ecs/eks, asg, lambda
│   └── iam/            # roles, policies, oidc
└── environments/
    ├── dev/
    │   ├── main.tf      # composes modules
    │   ├── backend.tf
    │   ├── providers.tf
    │   └── versions.tf
    ├── staging/
    └── prod/
```

One state file per environment per logical component is the smaller-blast-radius extreme; one state per environment is the common middle ground. Choose based on team size and change frequency, and explain the tradeoff.

## versions.tf

The `terraform {}` block name, `required_version`, the `versions.tf` filename, and the `.terraform.lock.hcl` lockfile are inherited syntax OpenTofu kept for compatibility — correct under `tofu`, not Terraform-isms.

```hcl
terraform {
  required_version = ">= 1.8.0"   # OpenTofu version; confirm threshold via Context7

  required_providers {
    aws = {
      source  = "hashicorp/aws"   # OpenTofu mirrors this namespace from its own registry
      version = "~> 5.0"
    }
  }
}
```

Pin provider major versions with `~>`. Commit `.terraform.lock.hcl`. Verify current provider major versions via Context7 rather than trusting the example.

## S3 backend with native locking

OpenTofu (1.10+) — Terraform (1.11+) — supports S3-native state locking via `use_lockfile`, removing the DynamoDB lock table. **Confirm the exact version threshold via Context7 before relying on it; these numbers drift.**

```hcl
terraform {
  backend "s3" {
    bucket       = "myorg-tofu-state-prod"
    key          = "networking/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
```

State bucket: versioning on, SSE on, public access blocked, ideally a separate hardened account. On older versions, use `dynamodb_table = "..."` instead of `use_lockfile`.

## Provider default_tags

Apply the tagging standard once, not per-resource:

```hcl
provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project
      Owner       = var.owner
      ManagedBy   = "OpenTofu"
      CostCenter  = var.cost_center
    }
  }
}
```

Note: a few resource types don't inherit `default_tags` cleanly (e.g. some ASG-propagated tags); handle those explicitly.

## Module-per-resource-group composition

Root config wires modules together, passing outputs as inputs — explicit dependencies, no cross-module reaching:

```hcl
module "networking" {
  source      = "../../modules/networking"
  environment = var.environment
  cidr_block  = "10.0.0.0/16"
}

module "data" {
  source      = "../../modules/data"
  environment = var.environment
  subnet_ids  = module.networking.private_subnet_ids
  vpc_id      = module.networking.vpc_id
}
```

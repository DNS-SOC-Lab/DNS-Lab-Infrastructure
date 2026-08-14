# AWS Build

This folder records what has actually been built in AWS. It is intentionally separate from the architecture folder: the architecture explains the design; this folder proves the implementation.

## Current implementation status

| AWS work | Status |
|---|---|
| IAM user access / admin group / password policy | Complete |
| MFA and account access hardening | Complete |
| Monthly cost budget | Complete |
| EC2 SSM role | Complete |
| `SOC-LAB-VPC` | Complete |
| `ATTACK-LAB-VPC` | Complete |
| Four current subnets | Complete |
| Two Internet Gateways | Complete |
| SOC public/private route tables | Complete |
| Attack public route table | Complete |
| Baseline security groups | Complete |
| EC2 instances | **Next** |
| Route 53 lab zone / delegation | Not built yet |
| AWS security/log telemetry | Not built yet |

## Documents

- [`01-account-security-and-access.md`](01-account-security-and-access.md)
- [`02-vpc-subnets-and-routing.md`](02-vpc-subnets-and-routing.md)
- [`03-security-groups-and-ssm.md`](03-security-groups-and-ssm.md)
- [`screenshots/`](screenshots/) — implementation evidence captured from the AWS console

New build files are added only when that AWS component is actually implemented.

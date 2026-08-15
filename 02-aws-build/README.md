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
| Scenario 01 EC2 deployment | Complete |
| Route 53 lab zone / delegation | **Next** |
| AWS security/log telemetry | Not built yet |

## Current AWS environment

The Scenario 01 compute layer is now running across the separated SOC and attacker VPCs.

![Scenario 01 EC2 inventory](screenshots/ec2-deployment/scenario01-ec2-inventory.png)

*The active inventory contains the web target, Splunk/SIEM host and separate attacker host, all passing EC2 status checks at the time of capture.*

## Documents

- [`01-account-security-and-access.md`](01-account-security-and-access.md)
- [`02-vpc-subnets-and-routing.md`](02-vpc-subnets-and-routing.md)
- [`03-security-groups-and-ssm.md`](03-security-groups-and-ssm.md)
- [`04-ec2-deployment.md`](04-ec2-deployment.md)
- [`screenshots/`](screenshots/) — implementation evidence captured from the AWS console and SSM sessions

New build files are added only when that AWS component is actually implemented.

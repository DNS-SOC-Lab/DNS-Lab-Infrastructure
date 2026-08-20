# AWS Build

This folder records what has actually been built in AWS. Architecture files explain the design; this folder proves the deployed implementation.

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
| Route 53 parent DNS migration | Complete |
| Route 53 child zone / parent-to-child delegation | Complete |
| Public DNS validation | Complete |
| Child `www` CNAME + training TXT fixture | Complete |
| Nginx / HTTPS for main + `www` hostnames | Complete |
| Route 53 public authoritative query logging | **Complete** |
| VPC Flow Logs - `SOC-LAB-VPC` | **Complete** |
| VPC Flow Logs - `ATTACK-LAB-VPC` | **Complete** |
| Multi-region CloudTrail management-event logging | **Complete** |
| Route 53 VPC Resolver Query Logging - both VPCs | **Complete** |
| AWS-to-Splunk delivery resources / IAM | **Complete** |

## Current AWS environment

The public DNS authority, public web target and security-telemetry layer are active.

```text
Route 53 public DNS
        |
        +--> soclab.abdul4rehman215.tech --> dns-soc-web01
        |
        +--> public query logs --> CloudWatch --> Kinesis

SOC-LAB-VPC ------------------+
                              +--> VPC Flow Logs --> S3 --> SQS
ATTACK-LAB-VPC ---------------+

CloudTrail ----------------------> S3 --> SQS

AWS VPC Resolver Query Logs
SOC-LAB-VPC + ATTACK-LAB-VPC ---> S3 --> SQS
```

The Splunk-side collectors and the final data-quality gate are documented separately in [`../03-splunk-build/`](../03-splunk-build/).

## Build-phase ownership

The AWS security telemetry phase was implemented by **Musfira - AWS Telemetry / Cloud Engineering**. This is build ownership for the shared infrastructure and does not change the team's rotating scenario-role matrix.

Splunk-side ingestion and validation of the resulting AWS data was owned by **Sonia - Detection Engineer** and is documented in [`../03-splunk-build/06-aws-telemetry-onboarding.md`](../03-splunk-build/06-aws-telemetry-onboarding.md).

## Documents

- [`01-account-security-and-access.md`](01-account-security-and-access.md)
- [`02-vpc-subnets-and-routing.md`](02-vpc-subnets-and-routing.md)
- [`03-security-groups-and-ssm.md`](03-security-groups-and-ssm.md)
- [`04-ec2-deployment.md`](04-ec2-deployment.md)
- [`05-route53-and-domain.md`](05-route53-and-domain.md)
- [`06-nginx-https-web-server.md`](06-nginx-https-web-server.md)
- [`07-security-telemetry.md`](07-security-telemetry.md) - Route 53 logging, VPC Flow Logs, CloudTrail, Resolver Query Logging, S3/SQS and IAM handoff
- [`screenshots/`](screenshots/) - selected implementation evidence from the AWS console and validation sessions

## Evidence style

Primary screenshots are shown next to the configuration they prove. The screenshot folders keep the same files available as a compact evidence archive.

The repository records final resources, settings, problems and fixes. It keeps the final technical record concise and excludes repetitive trial-and-error output.

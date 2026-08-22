# AWS Build

This folder records what has actually been built in AWS. Architecture files explain the design; this folder proves the deployed implementation.

## Current implementation status

| AWS work | Status |
|---|---|
| IAM / MFA / budget / SSM role | Complete |
| `SOC-LAB-VPC` and `ATTACK-LAB-VPC` | Complete |
| Base subnets, IGWs and route tables | Complete |
| Baseline security groups | Complete |
| Scenario 01 EC2 deployment | Complete |
| Route 53 parent migration + child delegation | Complete |
| Public DNS + Nginx/HTTPS | Complete |
| Route 53 public authoritative query logging | Complete |
| VPC Flow Logs — both VPCs | Complete |
| Multi-region CloudTrail management logging | Complete |
| Route 53 VPC Resolver Query Logging — both VPCs | Complete |
| AWS-to-Splunk delivery resources / IAM | Complete |
| `SOC-MONITORING-NAT` + monitoring-subnet private egress | **Complete** |
| Scenario 02 `SG-DNS`, `SG-VICTIM`, `SG-SINKHOLE` | **Complete** |
| Scenario 02 resolver/victim/sinkhole EC2s | **Complete** |
| Unbound forwarding resolver + persistent victim DNS path | **Complete** |
| Private Nginx sinkhole | **Complete** |
| Unbound RPZ safe-match / controlled redirect / reset | **Complete** |

## Current AWS environment

```text
PUBLIC / SHARED
Route 53 public DNS -> dns-soc-web01
AWS telemetry -> CloudWatch/Kinesis or S3/SQS -> Splunk

PRIVATE SCENARIO 02
SOC-MONITORING-SUBNET 10.50.30.0/24
    dns-soc-resolver01 10.50.30.10
    dns-soc-victim01   10.50.30.20
    dns-soc-sinkhole01 10.50.30.30
         |
         +-> private NAT egress through SOC-MONITORING-NAT
         +-> local SOC paths to Splunk 10.50.20.10:9997
```

The Scenario 02 service path is documented in [`08-scenario-02-defender-dns.md`](08-scenario-02-defender-dns.md). Splunk-side resolver/sinkhole onboarding is in [`../03-splunk-build/07-scenario-02-dns-onboarding.md`](../03-splunk-build/07-scenario-02-dns-onboarding.md).

## Scenario-specific AWS status

| Scenario | AWS-side state |
|---|---|
| **01 — DNS Recon** | Shared foundation complete; no extra infrastructure required |
| **02 — DGA** | **Resolver/victim/sinkhole + NAT/SG/RPZ infrastructure complete** |
| **03 — Fast Flux** | Reuse Scenario 02 platform; temporary controlled destinations + short-TTL DNS changes later |
| **04 — DNS Tunneling** | Reuse Scenario 02 platform; add an authoritative endpoint only if final controlled design needs it |

Scenario 02 infrastructure completion does not mean the DGA scenario itself is complete. Baseline, simulation, detection engineering, ML, alerting, AI profile, SOC analysis and human-approved response belong in the Scenario 02 repository.

## Documents

- [`01-account-security-and-access.md`](01-account-security-and-access.md)
- [`02-vpc-subnets-and-routing.md`](02-vpc-subnets-and-routing.md)
- [`03-security-groups-and-ssm.md`](03-security-groups-and-ssm.md)
- [`04-ec2-deployment.md`](04-ec2-deployment.md)
- [`05-route53-and-domain.md`](05-route53-and-domain.md)
- [`06-nginx-https-web-server.md`](06-nginx-https-web-server.md)
- [`07-security-telemetry.md`](07-security-telemetry.md)
- [`08-scenario-02-defender-dns.md`](08-scenario-02-defender-dns.md) — private resolver/victim/sinkhole, Unbound, RPZ and final safe-state validation
- [`configs/scenario-02/`](configs/scenario-02/) — repository-safe Scenario 02 service configuration
- [`screenshots/scenario-02/`](screenshots/scenario-02/) — curated Scenario 02 infrastructure evidence `79–106` where AWS/service-side evidence applies

## Evidence style

Primary screenshots are shown next to the configuration they prove. Repetitive troubleshooting captures are not published. The technical record keeps root cause and the final fix instead.

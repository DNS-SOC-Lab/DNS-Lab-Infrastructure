# Project Roadmap

The lab is built in checkpoints. A later phase should not hide an unfinished foundation or data-quality problem.

## Build sequence

| Phase | Work | Status |
|---|---|---|
| 01 | AWS identities, MFA and budget controls | **Complete** |
| 02 | `SOC-LAB-VPC`, SOC subnets, IGW, routes and baseline security groups | **Complete** |
| 03 | `ATTACK-LAB-VPC`, attack subnet, IGW, routes and baseline security group | **Complete** |
| 04 | Launch Scenario 01 EC2 instances | **Complete** |
| 05 | Route 53 parent migration, child delegation and permanent web/recon DNS baseline | **Complete** |
| 06 | Nginx / HTTPS validation | **Complete** |
| 07 | Splunk Enterprise Docker Compose platform / Gate A | **Complete** |
| 08 | `dns-soc-web01` Universal Forwarder + Nginx data-quality validation / Gate B | **Complete** |
| 09 | Enable AWS telemetry: Route 53 public logging, VPC Flow Logs, CloudTrail and early VPC Resolver Query Logging | **Complete** |
| 10 | Bring AWS telemetry into Splunk and validate index / host / source / sourcetype / time / fields / Gate C | **Complete** |
| 11 | Build the shared Flask / LLM bridge and validate the common alert-enrichment contract | **Next** |
| 12 | Scenario 01 DNS investigation dashboard and baseline | Separate Scenario 01 repository |
| 13 | Scenario 01 reconnaissance SPL detection, tuning and alert evidence contract | Separate Scenario 01 repository |
| 14 | Scenario 01 AI profile and human-validation workflow | Separate Scenario 01 repository |
| 15 | Execute Scenario 01 and document detection -> investigation -> response -> verification | Separate Scenario 01 repository |

## Current checkpoint

The common AWS and Splunk foundation is trusted through **Gate C**.

```text
Gate A - Splunk platform
Docker + Splunk + persistence + indexes + TCP 9997
                         COMPLETE
                            |
                            v
Gate B - Web telemetry
Universal Forwarder + Nginx data + data quality
                         COMPLETE
                            |
                            v
Gate C - AWS telemetry
Route 53 + VPC Flow + CloudTrail + Resolver Query Logs
                         COMPLETE
                            |
                            v
Shared AI foundation
Flask + LLM + internal HEC return path
                           NEXT
```

The current Splunk host is `dns-soc-splunk01` on **Ubuntu 24.04 LTS** at `10.50.20.10`, running Splunk Enterprise `10.4.2`. The platform was rebuilt cleanly on the supported host OS after an earlier KV Store compatibility problem; the final KV Store state is healthy (`status=ready`, `serverVersion=8.0.26`).

## Resolver Query Logging decision

The original roadmap introduced resolver-focused visibility mainly from Scenario 02 onward. The Project Lead later chose to enable **AWS Route 53 VPC Resolver Query Logging early** during Gate C because useful existing workloads already run in both VPCs.

That decision does not redesign the later defensive DNS architecture:

- AWS VPC Resolver Query Logging is active for `SOC-LAB-VPC` and `ATTACK-LAB-VPC` now;
- `dns-soc-resolver01` and `dns-soc-victim01` are still introduced from Scenario 02 onward;
- no Route 53 inbound/outbound Resolver endpoints were created for Gate C;
- DNS Firewall and sinkhole infrastructure are still later scenario work.

## Later scenario expansion rule

- **Scenario 02:** introduce `dns-soc-resolver01`, `dns-soc-victim01` and the reusable defender-side sinkhole capability.
- **Scenario 03:** reuse the common resolver/Splunk/AI platform and add controlled Fast Flux behavior.
- **Scenario 04:** reuse the same platform and include a clear before/after sinkhole or block verification as part of containment.

Scenario-specific SPL, dashboards, attack ground truth, analyst findings and IR evidence belong in the scenario repositories, not in the shared infrastructure build folder.

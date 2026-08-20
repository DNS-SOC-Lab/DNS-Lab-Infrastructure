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
| 11 | Build the shared Flask / OpenAI bridge and validate the common alert-enrichment contract | **Complete** |
| 12 | Scenario 01 DNS investigation dashboard and baseline | **Active / separate Scenario 01 repository** |
| 13 | Scenario 01 reconnaissance SPL detection, tuning and alert evidence contract | **Active / separate Scenario 01 repository** |
| 14 | Scenario 01 AI profile and human-validation workflow | Separate Scenario 01 repository after stable alert fields |
| 15 | Execute Scenario 01 and document detection -> investigation -> response -> verification | Separate Scenario 01 repository |

## Current checkpoint

The permanent shared platform is complete.

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
Splunk webhook + Flask/OpenAI bridge + internal HTTPS HEC
                         COMPLETE
                            |
                            v
COMMON SHARED INFRASTRUCTURE
                         COMPLETE
                            |
                            v
Scenario 01 detection engineering
                  ACTIVE IN SCENARIO REPO
```

The current Splunk host is `dns-soc-splunk01` on **Ubuntu 24.04 LTS** at `10.50.20.10`, running Splunk Enterprise `10.4.2`. KV Store is healthy (`status=ready`, `serverVersion=8.0.26`). The same host now runs the second `dns-soc-ai-bridge` container on `dns-soc-internal`; bridge TCP `5000` and HEC TCP `8088` remain internal-only.

## Resolver Query Logging decision

The original roadmap introduced resolver-focused visibility mainly from Scenario 02 onward. The Project Lead later chose to enable **AWS Route 53 VPC Resolver Query Logging early** during Gate C because useful existing workloads already run in both VPCs.

That decision does not redesign the later defensive DNS architecture:

- AWS VPC Resolver Query Logging is active for `SOC-LAB-VPC` and `ATTACK-LAB-VPC` now;
- `dns-soc-resolver01` and `dns-soc-victim01` are still introduced from Scenario 02 onward;
- no Route 53 inbound/outbound Resolver endpoints were created for Gate C;
- the sinkhole/deny path is still later Scenario 02 work; DNS Firewall is not required by the base plan and is added only if a later scenario explicitly justifies it.

## Shared AI completion

Phase 11 completed the final common-infrastructure dependency:

```text
Splunk alert
    -> internal webhook
    -> dns-soc-ai-bridge
    -> OpenAI Responses API
    -> schema-controlled analyst context
    -> internal HTTPS HEC
    -> index=dns_soc_ai / dns_soc:ai:triage
    -> human validation
```

The foundation passed strong-evidence, incomplete-evidence, failure-handling and final end-to-end validation. Scenario repositories reuse it rather than creating new Flask/OpenAI/HEC stacks.

## Later scenario expansion rule

- **Scenario 01:** reuse the completed shared platform; no additional AWS infrastructure is expected.
- **Scenario 02:** introduce `dns-soc-resolver01`, `dns-soc-victim01` and the reusable defender-side sinkhole capability.
- **Scenario 03:** reuse the common resolver/Splunk/AI platform and add controlled Fast Flux behavior.
- **Scenario 04:** reuse the same platform and include a clear before/after sinkhole or block verification as part of containment.

Scenario-specific SPL, dashboards, attack ground truth, analyst findings, AI profiles and IR evidence belong in the scenario repositories, not in the shared infrastructure build folder.

## After common infrastructure completion

Future infrastructure is added only when the matching scenario starts:

| Scenario | Infrastructure stage | Planned state |
|---|---|---|
| **01 — DNS Recon** | Reuse existing AWS/Splunk/Web/DNS/AI platform | No additional scenario infrastructure expected |
| **02 — DGA** | Activate the monitoring subnet with `dns-soc-resolver01`, `dns-soc-victim01`, DNS/victim SGs and reusable sinkhole path | Planned for Scenario 02 preparation |
| **03 — Fast Flux** | Reuse Scenario 02 platform; add only temporary controlled destinations and `flux.soclab...` short-TTL DNS behavior | Planned for Scenario 03 preparation |
| **04 — DNS Tunneling** | Reuse Scenario 02 platform; add controlled tunneling namespace/behavior and only add a separate authoritative DNS endpoint if the final design requires it | Planned/conditional for Scenario 04 preparation |

The detailed future-resource plan is maintained in [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md). The scenario repositories follow [`scenario-documentation-standard.md`](scenario-documentation-standard.md).

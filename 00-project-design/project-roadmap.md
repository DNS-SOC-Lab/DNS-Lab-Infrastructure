<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

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
| 09 | Enable AWS telemetry: Route 53 public logging, VPC Flow Logs, CloudTrail and VPC Resolver Query Logging | **Complete** |
| 10 | Bring AWS telemetry into Splunk and validate index / host / source / sourcetype / time / fields / Gate C | **Complete** |
| 11 | Build the shared Flask / OpenAI bridge and validate the common alert-enrichment contract | **Complete** |
| 12 | Scenario 01 DNS investigation dashboard and detection engineering | **Complete / maintained in separate Scenario 01 repository** |
| 13 | Scenario 01 controlled exercise, AI-assisted analysis and response evidence | **Pending / separate Scenario 01 repository** |

## Parallel Scenario 02 infrastructure expansion

Scenario 02 infrastructure was built in parallel after the common platform was stable.

| Work | Status |
|---|---|
| Private NAT egress for `SOC-MONITORING-SUBNET` | **Complete** |
| `SG-DNS`, `SG-VICTIM`, `SG-SINKHOLE` and Splunk receiver access | **Complete** |
| `dns-soc-resolver01` — `10.50.30.10` | **Complete** |
| `dns-soc-victim01` — `10.50.30.20` | **Complete** |
| `dns-soc-sinkhole01` — `10.50.30.30` | **Complete** |
| Unbound forwarding resolver + persistent victim DNS path | **Complete** |
| Resolver query/reply telemetry -> `dns_soc_dns` | **Complete** |
| DNS field/data-quality validation | **Complete** |
| Private Nginx sinkhole + Splunk access-log evidence | **Complete** |
| Unbound RPZ safe-match + controlled redirect validation | **Complete** |
| Final RPZ reset to disabled-enforcement state | **Complete** |
| Scenario 02 ML | **Not started** |
| Scenario 02 dashboard/detection/alert/AI/SOC/IR exercise | **Not started** |

Implementation is documented in [`../02-aws-build/08-scenario-02-defender-dns.md`](../02-aws-build/08-scenario-02-defender-dns.md) and [`../03-splunk-build/07-scenario-02-dns-onboarding.md`](../03-splunk-build/07-scenario-02-dns-onboarding.md).

## Current checkpoint

```text
COMMON SHARED INFRASTRUCTURE
AWS + Route 53 + Web + Splunk + AWS telemetry + shared AI
                         COMPLETE
                            |
             +--------------+----------------+
             |                               |
             v                               v
Scenario 01 detection engineering     Scenario 02 defender DNS platform
COMPLETE IN SCENARIO 01 REPO          COMPLETE
                                             |
                                             v
                                      Scenario 02 baseline / detection / ML
                                      NOT STARTED
```

The current Splunk host is `dns-soc-splunk01` on Ubuntu 24.04 LTS at `10.50.20.10`, running Splunk Enterprise `10.4.2`. The shared `dns-soc-ai-bridge` remains on the same EC2 through the internal Docker network.

## DNS visibility boundary

The project now has **three** distinct DNS visibility points:

1. Route 53 public authoritative query logs — public hosted-zone queries;
2. AWS VPC Resolver Query Logs — DNS handled by AWS-provided DNS in the associated VPCs;
3. `dns-soc-resolver01` Unbound logs — team-controlled resolver query/reply/RPZ telemetry in `dns_soc_dns`.

These sources are complementary. The team-controlled resolver is now the reusable defensive DNS control for Scenario 02 onward; it does not replace the existing AWS logging.

## Shared AI completion

The common AI path remains:

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

Scenario repositories reuse this bridge and add only a scenario profile after stable detection fields exist.

## Later scenario expansion rule

- **Scenario 01:** reuse the completed shared platform.
- **Scenario 02:** defender DNS infrastructure is complete; next work is baseline, controlled DGA/high-NXDOMAIN activity, detection engineering, optional ML comparison and the full SOC/IR exercise.
- **Scenario 03:** reuse the Scenario 02 victim/resolver/sinkhole platform and add only temporary controlled Fast Flux resources/DNS behavior.
- **Scenario 04:** reuse the same defender path; add a separate authoritative DNS endpoint only if the final tunneling implementation genuinely requires it.

Scenario-specific SPL, dashboards, attack ground truth, analyst findings, AI profiles and incident-response evidence belong in the scenario repositories rather than this shared infrastructure folder.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

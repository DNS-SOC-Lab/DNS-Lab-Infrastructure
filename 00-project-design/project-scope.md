<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Project Scope

## Objective

Build a realistic, network-centric DNS security lab where a four-person team can practice the full SOC lifecycle:

**Attack Simulation → Telemetry → Splunk Detection → AI-Assisted Summary → Human Investigation → Incident Response → Containment → Verification → Documentation**

The goal is not to create a single dashboard or one successful alert. Each exercise should leave enough evidence for the team to explain what happened at the DNS, network, cloud and system levels.

## Core platform

| Area | Decision |
|---|---|
| Cloud | One AWS account, `us-east-1` |
| Domain registrar | Hostinger for `abdul4rehman215.tech` |
| Parent authoritative DNS | Route 53 public hosted zone for `abdul4rehman215.tech` |
| Public lab namespace | `soclab.abdul4rehman215.tech` |
| Child authoritative DNS | Separate Route 53 public hosted zone delegated from the parent zone |
| Public web targets | `soclab.abdul4rehman215.tech` -> `100.49.192.164`; `www.soclab.abdul4rehman215.tech` -> CNAME to the main hostname |
| Existing parent services | Preserved through the Route 53 parent zone, including website and mail-related DNS |
| SOC network | `SOC-LAB-VPC` |
| Attacker network | `ATTACK-LAB-VPC` |
| Private connection between VPCs | None |
| SIEM | Splunk Enterprise in Docker |
| Endpoint/server collection | Splunk Universal Forwarder where required |
| AWS telemetry | Route 53 public query logs, VPC Flow Logs, CloudTrail and AWS VPC Resolver Query Logs are active and validated in Splunk |
| Team-controlled DNS telemetry | Unbound query/reply/RPZ telemetry from `dns-soc-resolver01` is active in `dns_soc_dns` |
| AI | One shared Flask/OpenAI bridge is implemented on `dns-soc-splunk01`; scenario-specific profiles reuse it and remain analyst-validated |
| Static child-zone fixtures | Permanent `A`, `NS`, `SOA`, training `TXT` and `www` CNAME records |
| DNS defense | Scenario 02 defender resolver + reusable RPZ/sinkhole path is implemented and reused by later scenarios |

## Current DNS telemetry boundary

Three DNS concepts must not be confused:

- **Route 53 public authoritative query logging** records queries reaching the public child hosted zone.
- **AWS VPC Resolver Query Logging** records queries handled by the AWS-provided resolver for associated VPC workloads.
- **Team-controlled Unbound logging** records the DNS path through `dns-soc-resolver01` and provides query/reply/RPZ evidence for the private victim path.

The Scenario 02 resolver forwards normal DNS upstream to `10.50.0.2`. Its own logs are copied through rsyslog to `/var/log/dns-soc/unbound.log` and forwarded to `index=dns_soc_dns`.

DNS Firewall is not part of the locked implementation. Containment uses the team-controlled Unbound RPZ path.

## Shared versus scenario-specific infrastructure

The common platform and Scenario 02 defender DNS infrastructure are now complete:

- **Scenario 01:** reuses the common AWS/Splunk/Web/DNS/AI platform.
- **Scenario 02:** uses the implemented private resolver, victim and sinkhole in `SOC-MONITORING-SUBNET`; scenario execution and ML are separate later work.
- **Scenario 03:** reuses Scenario 02 and adds only temporary team-controlled Fast Flux destinations and DNS behavior.
- **Scenario 04:** reuses the same defender DNS path and adds a separate authoritative DNS service only if the final tunneling design genuinely needs it.

The detailed resource state is maintained in [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md). The common scenario workflow is maintained in [`scenario-documentation-standard.md`](scenario-documentation-standard.md).

## DNS authority boundary

Hostinger is the registrar, while Route 53 is authoritative:

```text
.tech registry
    |
    v
Route 53 parent zone: abdul4rehman215.tech
    |
    +-- existing parent website and mail records
    |
    +-- NS delegation for soclab
            |
            v
Route 53 child zone: soclab.abdul4rehman215.tech
            |
            +-- A -> 100.49.192.164
            +-- www CNAME -> soclab.abdul4rehman215.tech
            +-- TXT -> "DNS SOC Training Lab"
```

The public child zone stays stable. Scenario 02 DGA names are intentionally **not** pre-created; they should return real NXDOMAIN before any controlled RPZ response. The reusable sinkhole is private (`10.50.30.30`) and is not represented by a permanent public Route 53 record.

## Scope boundaries

The project focuses on DNS behavior and the network evidence around it. It may use endpoint, cloud or web telemetry when those sources help prove the DNS story, but the lab does not try to become a general-purpose attack range.

Attack simulations are limited to infrastructure and domains the team owns or is explicitly authorized to test. High-volume public attacks, public DNS reflection/amplification and uncontrolled exfiltration are outside scope.

## What the team should be able to demonstrate

By the end of the four scenarios, the project should show that the team can:

- design segmented AWS networking and reason about traffic paths;
- design and validate parent/child DNS authority and delegation;
- operate a private defender-side resolver and reusable containment path;
- onboard useful DNS, network, server and cloud telemetry into Splunk;
- baseline normal behavior before writing detections;
- build and tune SPL detections around defined threat behavior;
- compare rule-based analytics with ML only where the evidence supports it;
- investigate alerts using raw evidence rather than trusting a label;
- map observed behavior to MITRE ATT&CK without over-mapping;
- preserve evidence, contain confirmed incidents and verify the result;
- use AI as analyst assistance rather than an automated security decision-maker;
- document commands, decisions, failures, fixes and lessons learned.

## Definition of success

A scenario is complete only when the team can answer four questions with evidence:

1. **What behavior was generated?**
2. **What telemetry captured it?**
3. **Why did the detection or investigation classify it the way it did?**
4. **What changed after the response, and how was that verified?**

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

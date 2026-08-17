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
| Public web targets | `soclab.abdul4rehman215.tech` → `100.49.192.164`; `www.soclab.abdul4rehman215.tech` → CNAME to the main hostname |
| Existing parent services | Preserved through the Route 53 parent zone, including website and mail-related DNS |
| SOC network | `SOC-LAB-VPC` |
| Attacker network | `ATTACK-LAB-VPC` |
| Private connection between VPCs | None |
| SIEM | Splunk Enterprise in Docker |
| Endpoint/server collection | Splunk Universal Forwarder where required |
| AWS telemetry | Route 53 / Resolver logs, VPC Flow Logs and CloudTrail as the project reaches those stages |
| AI | Flask/LLM bridge used for alert summarization, with analyst validation |
| Static child-zone fixtures | Permanent `A`, `NS`, `SOA`, training `TXT` and `www` CNAME records |
| DNS defense | Team-controlled DNS defense and sinkhole work in later scenarios |

## DNS authority boundary

Hostinger is used as the registrar, but the authoritative DNS path is now handled by Route 53:

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

This keeps the existing parent domain services intact while giving the lab namespace its own authoritative child zone. The five-record child baseline is kept stable; later DGA, Fast Flux, tunneling and sinkhole behavior is introduced only when the relevant scenario needs it. See [`scenario-dns-plan.md`](scenario-dns-plan.md).

## Scope boundaries

The project focuses on DNS behavior and the network evidence around it. It may use endpoint, cloud or web telemetry when those sources help prove the DNS story, but the lab does not try to become a general-purpose attack range.

Attack simulations are limited to infrastructure and domains the team owns or is explicitly authorized to test. High-volume public attacks, public DNS reflection/amplification, and uncontrolled exfiltration are outside scope.

## What the team should be able to demonstrate

By the end of the four scenarios, the project should show that the team can:

- design segmented AWS networking and reason about traffic paths;
- design and validate parent/child DNS authority and delegation;
- onboard useful DNS, network, server and cloud telemetry into Splunk;
- baseline normal behavior before writing detections;
- build and tune SPL detections around defined threat behavior;
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

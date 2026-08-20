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
| AWS telemetry | Route 53 public query logs, VPC Flow Logs, CloudTrail and AWS VPC Resolver Query Logs are active and validated in Splunk |
| AI | One shared Flask/OpenAI bridge is implemented on `dns-soc-splunk01`; scenario-specific profiles reuse the same platform and remain analyst-validated |
| Static child-zone fixtures | Permanent `A`, `NS`, `SOA`, training `TXT` and `www` CNAME records |
| DNS defense | Team-controlled resolver and sinkhole capability introduced with Scenario 02 and reused by later IR scenarios |


## Current telemetry boundary

The shared infrastructure now has two different DNS visibility concepts that must not be confused:

- **Route 53 public authoritative query logging** records queries that reach the public `soclab.abdul4rehman215.tech` hosted zone.
- **Route 53 VPC Resolver Query Logging** records DNS queries handled by the AWS VPC Resolver for associated workloads in `SOC-LAB-VPC` and `ATTACK-LAB-VPC`.

The second item was enabled early during Gate C because the existing VPC workloads already provide useful DNS telemetry. It does **not** replace the team-controlled defender resolver planned for Scenario 02. `dns-soc-resolver01`, `dns-soc-victim01` and the reusable sinkhole path are still later infrastructure. DNS Firewall is not required by the locked base plan and would be introduced only if a later scenario explicitly chooses and justifies it.

## Shared versus scenario-specific infrastructure

The common platform is complete through the shared AI foundation. From this point, the lab uses a just-in-time scenario model rather than another broad infrastructure phase:

- **Scenario 01:** reuses the completed shared platform; no new scenario-specific AWS resource is currently expected.
- **Scenario 02:** adds the team-controlled resolver, victim and reusable sinkhole/deny path in `SOC-MONITORING-SUBNET`.
- **Scenario 03:** reuses Scenario 02 and adds only temporary team-controlled Fast Flux destinations and DNS behavior.
- **Scenario 04:** reuses the same defender DNS path and adds a separate authoritative DNS service only if the final tunneling design genuinely needs it.

The design details are maintained in [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md). The common scenario workflow is maintained in [`scenario-documentation-standard.md`](scenario-documentation-standard.md).

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

This keeps the existing parent domain services intact while giving the lab namespace its own authoritative child zone. The five-record child baseline is kept stable. DGA, Fast Flux and tunneling behavior is introduced only when the relevant scenario needs it; the reusable internal sinkhole capability is introduced with the Scenario 02 resolver infrastructure rather than as a public Route 53 record. See [`scenario-dns-plan.md`](scenario-dns-plan.md).

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

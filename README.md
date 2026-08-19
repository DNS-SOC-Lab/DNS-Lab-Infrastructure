# DNS Attack, Detection & Response Lab - Infrastructure

**AWS · Splunk Enterprise · DNS Security · MITRE ATT&CK · Incident Response · AI-Assisted Analysis**

This repository contains the shared infrastructure and platform design for a four-person DNS-focused SOC lab. It records the AWS network, compute, DNS authority, public web target, Splunk foundation and later shared AI integration that support the separate attack-scenario repositories.

The lab runs in **AWS us-east-1 (N. Virginia)** with a deliberately separated attacker VPC and SOC VPC. Public DNS is split into a Route 53 parent zone and a delegated Route 53 child zone for the lab namespace.

## Architecture at a glance

```mermaid
flowchart TB
    Registrar[Hostinger<br/>Domain registrar]
    Internet((Internet / .tech DNS hierarchy))

    Parent[Route 53 Parent Hosted Zone<br/>abdul4rehman215.tech]
    Existing[Existing parent services<br/>Website + mail-related DNS]
    Child[Route 53 Child Hosted Zone<br/>soclab.abdul4rehman215.tech]
    ChildStatic[Permanent child records<br/>A + NS + SOA + TXT + www CNAME]

    subgraph ATTACK[ATTACK-LAB-VPC · 10.60.0.0/16]
        AS[ATTACK-PUBLIC-SUBNET<br/>10.60.10.0/24]
        A[dns-attack01<br/>10.60.10.10]
        AS --> A
    end

    subgraph SOC[SOC-LAB-VPC · 10.50.0.0/16]
        TS[SOC-TARGET-SUBNET<br/>10.50.10.0/24]
        SS[SOC-SIEM-SUBNET<br/>10.50.20.0/24]
        MS[SOC-MONITORING-SUBNET<br/>10.50.30.0/24]
        W[dns-soc-web01<br/>10.50.10.10<br/>Nginx + HTTPS]
        S[dns-soc-splunk01<br/>10.50.20.10<br/>Splunk Enterprise 10.4.2<br/>Docker Compose]
        TS --> W
        SS --> S
        MS -.-> M[Scenario 02 onward<br/>resolver / victim / sinkhole]
    end

    Registrar -. registrar nameservers .-> Parent
    Internet --> Parent
    Parent --> Existing
    Parent -->|NS delegation: soclab| Child
    Child --> ChildStatic
    ChildStatic -->|soclab / www| W
    A --> Internet
    W -. next UF TCP 9997 .-> S

    X{{No VPC peering / no private route between attacker and SOC VPCs}}
```

Hostinger remains the registrar. The parent domain is authoritative in Route 53, and the parent zone delegates `soclab.abdul4rehman215.tech` to a separate Route 53 child zone. The child zone has a stable five-record baseline: A, NS, SOA, a training TXT fixture and `www` CNAME. Both web hostnames resolve to the public Nginx target. The attacker reaches the lab through the public Internet rather than through a private route into the SOC VPC.

## Four scenarios

The common infrastructure in this repository supports four scenario repositories maintained separately by the team.

| Scenario | Focus | MITRE ATT&CK | Main learning goal |
|---|---|---|---|
| 01 | DNS Reconnaissance & Enumeration | T1590.002 | Detect abnormal DNS record enumeration and investigate follow-up activity |
| 02 | DGA + High NXDOMAIN | T1568.002 | Identify generated-domain behavior, introduce the defender resolver path and establish reusable sinkhole capability |
| 03 | Fast Flux DNS | T1568.001 | Correlate changing DNS answers, TTL behavior and destination changes |
| 04 | DNS Tunneling | T1071.004 / T1572 | Detect suspicious encoded DNS behavior and prove containment through the defender-controlled DNS path |

MITRE mappings describe the behavior the team intends to simulate and are refined if the final implementation differs from the plan.

## Team model

The team rotates through four roles so every member practices more than one part of the SOC lifecycle.

| Scenario | Project Lead | SOC Analyst | Detection Engineer | IR / Defender |
|---|---|---|---|---|
| DNS Recon | Abdul-Rehman | Musfira | Sonia | Lubaba |
| DGA | Musfira | Sonia | Lubaba | Abdul-Rehman |
| Fast Flux | Sonia | Lubaba | Abdul-Rehman | Musfira |
| DNS Tunneling | Lubaba | Abdul-Rehman | Musfira | Sonia |

The Project Lead also operates the authorized simulation for that scenario and records ground-truth timing. The SOC Analyst remains the human decision-maker even when AI-assisted summaries are used.

## Current build status

| Area | Status |
|---|---|
| Project design | Complete / maintained as the shared design baseline |
| AWS identity, MFA, budget and SSM role | Complete |
| VPCs, subnets, IGWs and route tables | Complete |
| Baseline security groups | Complete |
| Scenario 01 EC2 deployment | Complete |
| Route 53 parent migration and child delegation | Complete |
| Public DNS validation and static child-zone fixtures | Complete |
| Nginx / HTTPS for main + `www` hostnames | Complete |
| Splunk Enterprise platform / Gate A | **Complete** |
| Five project indexes + 30-day retention | **Complete** |
| Splunk receiver TCP `9997` | **Complete** |
| Web Universal Forwarder + Nginx/Linux data quality | **Next** |
| AWS security telemetry onboarding | Planned |
| Shared AI foundation | Planned after Web/AWS data-quality gates |
| Scenario-specific detections and exercises | Maintained in separate scenario repositories |

The current checkpoint is **trusted telemetry onboarding**. The Splunk platform is ready; the next implementation step is the Universal Forwarder on `dns-soc-web01`, followed by AWS telemetry and data-quality validation.

## Repository map

- [`00-project-design/`](00-project-design/) - scope, roles, scenario model, DNS scenario plan and roadmap
- [`01-network-architecture/`](01-network-architecture/) - VPC blueprint, CIDRs, DNS authority design, controls and traffic flows
- [`02-aws-build/`](02-aws-build/) - implemented AWS configuration and validation evidence
- [`03-splunk-build/`](03-splunk-build/) - implemented Splunk platform, data structure, operations, evidence and later data onboarding
- [`04-ai-integration/`](04-ai-integration/) - shared AI-assisted alert summarization design and later implementation

The four attack scenarios are maintained in separate repositories. This infrastructure repository keeps the common architecture and build record so the same foundation does not have to be duplicated across every scenario.

## Documentation rule

The repository separates **design** from **implementation**. Architecture files explain how the lab is intended to work. Build files record what was actually configured and how it was validated. Scenario repositories contain scenario-specific preparation, execution, evidence, analysis and response.

> This lab is for controlled security training on infrastructure and domains owned by, or explicitly authorized for, the team.

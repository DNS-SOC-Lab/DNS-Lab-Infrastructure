<img
  src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=220&section=header&text=DNS%20Attack%20Detection%20Response%20Lab&fontSize=36&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=AWS%20Splunk%20Enterprise%20DNS%20Security%20SOC%20Engineering&descSize=17&descAlignY=58&descColor=00F5FF"
  width="100%"
  alt="DNS Attack Detection and Response Lab"
/>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=3000&pause=1000&color=00F5FF&center=true&vCenter=true&repeat=true&width=900&height=70&lines=4+DNS+Scenarios+%7C+4+Rotating+SOC+Roles;Detect+%E2%86%92+Investigate+%E2%86%92+Respond+%E2%86%92+Verify" alt="Project summary animation" />

![AWS](https://img.shields.io/badge/AWS-us--east--1-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-Enterprise-000000?style=for-the-badge&logo=splunk&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![DNS](https://img.shields.io/badge/DNS-Security-00B8D9?style=for-the-badge)
![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-E34F26?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Assisted-7B2CBF?style=for-the-badge)

<br/>

![Stars](https://img.shields.io/github/stars/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)
![Forks](https://img.shields.io/github/forks/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)
![Repo Size](https://img.shields.io/github/repo-size/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)
![License](https://img.shields.io/github/license/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)
![Issues](https://img.shields.io/github/issues/DNSentinel-Lab/DNS-Lab-Infrastructure?style=flat-square)

**Shared infrastructure and engineering record for a four-person, DNS-focused SOC lab built around AWS, Splunk Enterprise, controlled DNS attack simulations, detection engineering, threat hunting, incident response and AI-assisted analyst context.**

[Project at a Glance](#-project-at-a-glance) · [Architecture](#-architecture-at-a-glance) · [Telemetry](#-security-telemetry-pipeline) · [Status](#-project-status) · [Team](#-team--rotating-roles) · [Repository](#-repository-navigation)

</div>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🎯 Project at a Glance

One shared SOC platform supports **four DNS security scenarios**. The infrastructure stays common where possible; scenario-specific resources are added only when a scenario genuinely needs them.

| Scenario | Security focus | MITRE ATT&CK | What the team practices |
|---|---|---|---|
| 🔎 **01 — DNS Reconnaissance & Enumeration** | Abnormal DNS record enumeration and follow-up activity | `T1590.002` | Public DNS visibility, detection, investigation and evidence correlation |
| 🧬 **02 — DGA + High NXDOMAIN** | Generated-domain behavior and abnormal NXDOMAIN activity | `T1568.002` | Defender-controlled resolution, baselining, detection/ML and containment path |
| 🔄 **03 — Fast Flux DNS** | Rapidly changing DNS answers and short-TTL behavior | `T1568.001` | DNS answer/TTL correlation and destination-change analysis |
| 🛰️ **04 — DNS Tunneling** | Controlled encoded DNS behavior | `T1071.004` / `T1572` where the implemented behavior fits | Suspicious query-pattern detection, investigation and response verification |

> MITRE mappings describe the behavior the team intends to simulate. Scenario implementation and evidence remain in separate scenario repositories.

<div align="center">

<img src="https://img.shields.io/badge/Scenarios-4-00F5FF?style=for-the-badge" alt="4 scenarios" />
<img src="https://img.shields.io/badge/Rotating_Roles-4-FF6B6B?style=for-the-badge" alt="4 rotating roles" />
<img src="https://img.shields.io/badge/Splunk_Indexes-5-66BB6A?style=for-the-badge" alt="5 Splunk indexes" />
<img src="https://img.shields.io/badge/Shared_AI-1_Foundation-7B2CBF?style=for-the-badge" alt="Shared AI foundation" />

</div>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🏗️ Architecture at a Glance

This view is intentionally **scenario-neutral**. It shows the complete project model without duplicating subnet, registrar, private-IP, NAT, RPZ or Docker implementation details.

```mermaid
flowchart TB
    subgraph SC[Four DNS Security Scenarios]
        S1[01 · DNS Recon]
        S2[02 · DGA + NXDOMAIN]
        S3[03 · Fast Flux]
        S4[04 · DNS Tunneling]
    end

    S1 --> PUB[Public DNS / Web Surface]
    S2 --> DEF[Victim / Defender DNS Path]
    S3 --> DEF
    S4 --> DEF

    PUB --> TEL[Security Telemetry<br/>DNS · Web · Network · AWS · Host]
    DEF --> TEL

    TEL --> SPL[Splunk Enterprise]
    SPL --> AI[AI-Assisted Alert Summary]
    SPL --> SOC[SOC Analysis & Threat Hunting]
    AI --> SOC
    SOC --> IR[Incident Response / Defense]
    IR -. Block / Sinkhole / Verify .-> DEF
```

The detailed network, DNS authority, trust boundaries, CIDRs, security groups and traffic paths live in [`01-network-architecture/`](01-network-architecture/). The registrar/delegation chain is documented specifically in [`01-network-architecture/dns-authority-and-delegation.md`](01-network-architecture/dns-authority-and-delegation.md).

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 📡 Security Telemetry Pipeline

Splunk is the central evidence and analysis layer. The project intentionally combines public DNS, network, cloud, web and defender-controlled DNS telemetry instead of treating one source as the whole investigation.

```mermaid
flowchart LR
    WEB[Web / Nginx] -->|UF · 9997| SPL[Splunk Enterprise]
    DNS[Unbound + Sinkhole] -->|UF · 9997| SPL
    R53[Route 53 Public DNS] -->|CloudWatch → Kinesis| SPL
    VPC[VPC Flow Logs] -->|S3 → SQS| SPL
    CT[CloudTrail] -->|S3 → SQS| SPL
    RQ[Resolver Query Logs] -->|S3 → SQS| SPL

    SPL --> IDX[dns_soc_aws · dns_soc_web · dns_soc_dns]
    SPL -->|Internal webhook| AIB[Shared AI Bridge]
    AIB --> OAI[OpenAI API]
    OAI --> AIB
    AIB -->|Internal HTTPS HEC| AIDX[dns_soc_ai]
```

The AWS collection layer uses the supported Splunk Add-on for AWS `8.2.1`. Live implementation recorded the following source identities:

| Telemetry | Destination index | Actual sourcetype |
|---|---|---|
| Route 53 public authoritative query logs | `dns_soc_aws` | `aws:kinesis` |
| VPC Flow Logs | `dns_soc_aws` | `aws:cloudwatchlogs:vpcflow` |
| CloudTrail | `dns_soc_aws` | `aws:cloudtrail` |
| Route 53 Resolver Query Logs | `dns_soc_aws` | `aws:s3` |
| Nginx access telemetry | `dns_soc_web` | `dns_soc:nginx:access` |
| Team-controlled Unbound resolver | `dns_soc_dns` | `unbound:dns` |
| Private sinkhole Nginx access | `dns_soc_web` | `nginx:access` |

> Detailed onboarding, source validation and field-quality evidence are maintained in [`03-splunk-build/`](03-splunk-build/).

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🚦 Project Status

The root README tracks only the **high-level shared-platform and scenario state**. Detailed implementation checkpoints belong in the relevant build folders and the project roadmap.

| Area | Current state |
|---|---|
| 🧭 Project design baseline | ✅ Complete / maintained |
| ☁️ Shared AWS network, identity, routing and access | ✅ Complete |
| 🌐 Route 53 authority, public DNS, Nginx and HTTPS | ✅ Complete |
| 🔎 Splunk Enterprise platform + five project indexes | ✅ Complete |
| 📡 Web + AWS security telemetry | ✅ Complete |
| 🤖 Shared AI foundation | ✅ Complete |
| 🛡️ Common shared infrastructure | ✅ Complete |
| 🔎 Scenario 01 detection engineering | ✅ Complete — maintained in separate Scenario 01 repository |
| 🧑‍💻 Scenario 01 official SOC / IR exercise | ⚪ Pending — maintained in separate Scenario 01 repository |
| 🧬 Scenario 02 defender DNS infrastructure + Splunk onboarding | ✅ Complete |
| 🧬 Scenario 02 detection engineering / ML / exercise | ⚪ Not started in this repository baseline |
| 🔄 Scenario 03 Fast Flux resources | ⚪ Planned when Scenario 03 begins |
| 🛰️ Scenario 04 tunneling-specific resources | ⚪ Conditional / planned when Scenario 04 begins |

Scenario-specific detections and exercises are maintained in the team's separate [scenario repositories](https://github.com/orgs/DNSentinel-Lab/repositories).

For chronological implementation detail, see [`00-project-design/project-roadmap.md`](00-project-design/project-roadmap.md) and [`00-project-design/scenario-infrastructure-roadmap.md`](00-project-design/scenario-infrastructure-roadmap.md).

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 👥 Team & Rotating Roles

The four-role rotation model was designed so each member practices every major SOC role once across the four core scenarios. The model was **designed and proposed by [Lubaba](https://github.com/lubaba1513-pixel)**.

| Scenario | Project Lead / Simulation | SOC Analyst / Hunter | Detection Engineer | IR / Defender |
|---|---|---|---|---|
| 01 — DNS Recon | [Abdul-Rehman](https://github.com/abdul4rehman215) | [Musfira](https://github.com/MUSFIRA-ZAFAR) | [Sonia](https://github.com/sonia11mansha415) | [Lubaba](https://github.com/lubaba1513-pixel) |
| 02 — DGA + NXDOMAIN | Musfira | Sonia | Lubaba | Abdul-Rehman |
| 03 — Fast Flux | Sonia | Lubaba | Abdul-Rehman | Musfira |
| 04 — DNS Tunneling | Lubaba | Abdul-Rehman | Musfira | Sonia |

```text
Simulation → Telemetry → Detection → AI Assistance → SOC Investigation → IR / Defense → Verification → Documentation
```

See [`00-project-design/team-roles.md`](00-project-design/team-roles.md) for the responsibilities, AI decision boundary and parallel working model.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🗂️ Repository Navigation

| Area | What you will find |
|---|---|
| 🧭 [`00-project-design/`](00-project-design/) | Scope, four-scenario model, roles, roadmaps and documentation standard |
| 🌐 [`01-network-architecture/`](01-network-architecture/) | VPC blueprint, CIDRs, DNS authority, trust boundaries, security groups and traffic flows |
| ☁️ [`02-aws-build/`](02-aws-build/) | Implemented AWS configuration, telemetry and Scenario 02 defender-DNS platform |
| 🔎 [`03-splunk-build/`](03-splunk-build/) | Splunk platform, indexes, Web/AWS/DNS onboarding, validation and operations |
| 🤖 [`04-ai-integration/`](04-ai-integration/) | Shared AI bridge, schemas, HEC/webhook path, validation and operating evidence |
| 🤝 [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow and repository expectations |

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🧠 Engineering Areas Demonstrated

| Area | Practical work represented in this repository |
|---|---|
| **AWS Networking** | Multi-VPC design, subnets, routing, security groups, SSM-oriented administration and controlled trust boundaries |
| **DNS Engineering** | Route 53 authority/delegation, public DNS, defender-controlled resolution, Unbound, RPZ and sinkhole path |
| **Splunk Engineering** | Docker deployment, indexes, retention, Universal Forwarder, AWS add-on, HEC, source validation and data-quality checks |
| **Security Telemetry** | DNS, Nginx, VPC Flow, CloudTrail, Route 53 public queries and Resolver Query Logs |
| **Detection Engineering** | Scenario-specific detection hypotheses, SPL validation, tuning boundaries and MITRE discipline |
| **SOC Operations** | Analyst triage, threat hunting, evidence correlation, human validation and documentation |
| **Incident Response** | Containment design, DNS deny/sinkhole path, verification and response evidence |
| **AI Integration** | Shared Flask/LLM bridge that provides structured analyst assistance without replacing human judgement |

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 📚 Documentation Model

This repository deliberately separates **design**, **implementation** and **scenario evidence**:

- **Design documents** explain how the lab is intended to work and why decisions were made.
- **Build documents** record what was actually configured and how it was validated.
- **Troubleshooting documents** keep useful root causes and final fixes instead of repetitive trial-and-error history.
- **Scenario repositories** contain scenario-specific preparation, execution, detection, analysis, response and evidence.

The common 20-part scenario workflow, networking view, MITRE discipline and dashboard engineering standard are defined in [`00-project-design/scenario-documentation-standard.md`](00-project-design/scenario-documentation-standard.md).

> [!IMPORTANT]
> This lab is for **controlled security training** on infrastructure and domains owned by, or explicitly authorized for, the team.

<div align="center">

### DNSentinel Lab
**Build the telemetry. Prove the detection. Investigate the evidence. Verify the response.**

[⬆ Back to top](README.md)

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,12,19,24,30&height=120&section=footer" width="100%" alt="footer" />

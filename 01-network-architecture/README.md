<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,12,19&height=135&section=header&text=Network%20Architecture&fontSize=34&fontColor=ffffff&animation=fadeIn&desc=VPCs%20%7C%20DNS%20Authority%20%7C%20Trust%20Boundaries%20%7C%20Traffic%20Flow&descSize=15&descAlignY=68" width="100%" alt="Network Architecture" />

[🏠 Repository Home](../README.md) · [🧭 Project Design](../00-project-design/README.md) · **🌐 Network Architecture** · [☁️ AWS Build](../02-aws-build/README.md)

This folder is the **network and DNS blueprint** for the lab. It explains how traffic moves, how the public namespace is delegated, why the attacker and SOC environments are separated, and how the defender-controlled DNS path fits into the locked design.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 🗺️ Architecture Documents

| Document | Purpose |
|---|---|
| 🏗️ [`base-network.md`](base-network.md) | Overall AWS network design and trust boundaries |
| 🧮 [`cidr-plan.md`](cidr-plan.md) | VPC, subnet and assigned address plan |
| 🔐 [`security-groups.md`](security-groups.md) | Baseline and Scenario 02 service exposure / SG-to-SG access |
| 🌍 [`dns-authority-and-delegation.md`](dns-authority-and-delegation.md) | Registrar, parent zone, child zone and public DNS delegation |
| 🔀 [`traffic-flow.md`](traffic-flow.md) | Management, DNS, public target, logging, defender DNS and response paths |
| 🧩 [`diagrams/`](diagrams/) | Editable Mermaid source used by architecture documentation |

## 🔐 Trust Boundary at a Glance

```mermaid
flowchart LR
    A[ATTACK-LAB-VPC] -->|Public DNS / Internet only| P[Public Lab Surface]
    P --> S[SOC-LAB-VPC]
    A -. No peering / no private route .- S
    V[Victim] --> R[Defender DNS Resolver]
    R --> U[Upstream DNS]
    S --> SPL[Splunk]
```

Implementation evidence stays in [`../02-aws-build/`](../02-aws-build/); Splunk-side data onboarding stays in [`../03-splunk-build/`](../03-splunk-build/).

## 🛡️ Scenario Platform State

`SOC-MONITORING-SUBNET` is active and hosts the Scenario 02 defender DNS platform:

| Host | Address | Role |
|---|---:|---|
| `dns-soc-resolver01` | `10.50.30.10` | Unbound resolver / defender DNS |
| `dns-soc-victim01` | `10.50.30.20` | Controlled victim endpoint |
| `dns-soc-sinkhole01` | `10.50.30.30` | Private sinkhole target |

The subnet remains private and uses `SOC-MONITORING-NAT` for outbound package/management egress. No VPC peering or attacker-to-SOC private route was introduced.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

[🧭 Previous: Project Design](../00-project-design/README.md) · [🏠 Repository Home](../README.md) · [☁️ Next: AWS Build](../02-aws-build/README.md)

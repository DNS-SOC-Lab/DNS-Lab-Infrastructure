# Network Architecture

This folder is the blueprint for the lab network and DNS authority model. It explains **how traffic is supposed to move**, how the public namespace is delegated, and why the attacker and SOC environments are separated.

| Document | Purpose |
|---|---|
| [`base-network.md`](base-network.md) | Overall AWS network design and trust boundaries |
| [`cidr-plan.md`](cidr-plan.md) | VPC, subnet and reserved address plan |
| [`security-groups.md`](security-groups.md) | Baseline service exposure and SG-to-SG access model |
| [`dns-authority-and-delegation.md`](dns-authority-and-delegation.md) | Registrar, parent zone, child zone and public DNS delegation design |
| [`traffic-flow.md`](traffic-flow.md) | Management, DNS, public target, logging and scenario traffic paths |
| [`diagrams/`](diagrams/) | Editable Mermaid source used by the architecture documentation |

The implementation evidence for the currently built AWS resources, Route 53 zones and AWS security telemetry is kept separately in [`../02-aws-build/`](../02-aws-build/). Splunk-side Web/AWS data onboarding is documented in [`../03-splunk-build/`](../03-splunk-build/).

## Later scenario activation

The base network remains locked. Future scenario resources reuse the existing CIDRs and `SOC-MONITORING-SUBNET`; they do not introduce VPC peering or a new parallel network. The future resource sequence is documented in [`../00-project-design/scenario-infrastructure-roadmap.md`](../00-project-design/scenario-infrastructure-roadmap.md).

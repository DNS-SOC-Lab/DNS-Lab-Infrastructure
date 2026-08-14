# Network Architecture

This folder is the blueprint for the lab network. It explains **how traffic is supposed to move** and why the attacker and SOC environments are separated.

| Document | Purpose |
|---|---|
| [`base-network.md`](base-network.md) | Overall AWS network design and trust boundaries |
| [`cidr-plan.md`](cidr-plan.md) | VPC, subnet and reserved address plan |
| [`security-groups.md`](security-groups.md) | Baseline service exposure and SG-to-SG access model |
| [`traffic-flow.md`](traffic-flow.md) | Management, public target, logging and scenario traffic paths |
| [`diagrams/`](diagrams/) | Editable Mermaid source used by the architecture documentation |

The implementation evidence for the currently built VPCs, subnets, IGWs and route tables is kept separately in [`../02-aws-build/`](../02-aws-build/).

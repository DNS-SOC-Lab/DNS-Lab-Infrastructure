# Network Architecture

This folder is the blueprint for the lab network and DNS authority model. It explains how traffic moves, how the public namespace is delegated, why the attacker and SOC environments are separated, and how the Scenario 02 defender DNS path now fits into the locked network.

| Document | Purpose |
|---|---|
| [`base-network.md`](base-network.md) | Overall AWS network design and trust boundaries |
| [`cidr-plan.md`](cidr-plan.md) | VPC, subnet and assigned address plan |
| [`security-groups.md`](security-groups.md) | Baseline and Scenario 02 service exposure / SG-to-SG access |
| [`dns-authority-and-delegation.md`](dns-authority-and-delegation.md) | Registrar, parent zone, child zone and public DNS delegation |
| [`traffic-flow.md`](traffic-flow.md) | Management, DNS, public target, logging, defender DNS and response paths |
| [`diagrams/`](diagrams/) | Editable Mermaid source used by the architecture documentation |

Implementation evidence is kept separately in [`../02-aws-build/`](../02-aws-build/) and Splunk-side data onboarding in [`../03-splunk-build/`](../03-splunk-build/).

## Scenario platform state

`SOC-MONITORING-SUBNET` is no longer only reserved. It now hosts the Scenario 02 defender DNS platform:

```text
10.50.30.10  dns-soc-resolver01
10.50.30.20  dns-soc-victim01
10.50.30.30  dns-soc-sinkhole01
```

The subnet remains private and uses `SOC-MONITORING-NAT` for outbound package/management egress. No VPC peering or attacker-to-SOC private route was introduced.

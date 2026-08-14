# CIDR and Address Plan

The two VPC CIDRs do not overlap. Subnet ranges are intentionally simple so the team can identify a system's role from its address during investigations.

## VPCs

| VPC | CIDR | Purpose |
|---|---|---|
| `SOC-LAB-VPC` | `10.50.0.0/16` | Target, SIEM and monitoring/defense services |
| `ATTACK-LAB-VPC` | `10.60.0.0/16` | Authorized attack/simulation environment |

## Subnets

| VPC | Subnet | CIDR | Route type | Purpose |
|---|---|---|---|---|
| SOC | `SOC-TARGET-SUBNET` | `10.50.10.0/24` | Public | Public-facing lab target |
| SOC | `SOC-SIEM-SUBNET` | `10.50.20.0/24` | Public | Splunk / AI services with restricted inbound access |
| SOC | `SOC-MONITORING-SUBNET` | `10.50.30.0/24` | Private | Later DNS, victim and defense components |
| Attack | `ATTACK-PUBLIC-SUBNET` | `10.60.10.0/24` | Public | Authorized attack host |

## Reserved private addresses

These addresses are part of the architecture plan and are assigned only when the corresponding system is built.

| Address | Planned role |
|---|---|
| `10.50.10.10` | Web target |
| `10.50.20.10` | Splunk SOC |
| `10.50.30.10` | DNS resolver / defender component |
| `10.50.30.20` | Scenario victim endpoint |
| `10.50.30.30` | Sinkhole endpoint / service if implemented separately |
| `10.60.10.10` | Attack host |

The monitoring range is documented here because it is part of the locked network architecture, even though those later scenario systems are not part of the current AWS deployment yet.

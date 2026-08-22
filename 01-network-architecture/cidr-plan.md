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
| SOC | `SOC-TARGET-SUBNET` | `10.50.10.0/24` | Public | Public Web target + public monitoring NAT placement |
| SOC | `SOC-SIEM-SUBNET` | `10.50.20.0/24` | Public/restricted | Splunk / AI services with restricted inbound access |
| SOC | `SOC-MONITORING-SUBNET` | `10.50.30.0/24` | Private + NAT egress | Defender resolver, victim and sinkhole |
| Attack | `ATTACK-PUBLIC-SUBNET` | `10.60.10.0/24` | Public | Authorized attack host |

## Assigned private addresses

| Address | Deployed role | State |
|---|---|---|
| `10.50.10.10` | `dns-soc-web01` | Deployed |
| `10.50.20.10` | `dns-soc-splunk01` | Deployed |
| `10.50.30.10` | `dns-soc-resolver01` | **Deployed** |
| `10.50.30.20` | `dns-soc-victim01` | **Deployed** |
| `10.50.30.30` | `dns-soc-sinkhole01` | **Deployed** |
| `10.60.10.10` | `dns-attack01` | Deployed |

## Monitoring subnet egress

`SOC-MONITORING-SUBNET` remains private. Its route table uses `SOC-MONITORING-NAT` for `0.0.0.0/0`, while `10.50.0.0/16` stays local.

This supports package updates/management without assigning public IPv4 addresses to the Scenario 02 hosts.

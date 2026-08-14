# Base Network Architecture

## Design objective

Keep the attacker network logically separate from the SOC network while still allowing realistic public-facing DNS and web interaction. Internal SOC communication stays inside `SOC-LAB-VPC`; the attacker does not receive a private route to `10.50.0.0/16`.

## VPC layout

```mermaid
flowchart TB
    Internet((Internet))
    DNS[Route 53 Public DNS<br/>soclab.abdul4rehman215.tech]

    subgraph AVPC[ATTACK-LAB-VPC · 10.60.0.0/16]
        ASubnet[ATTACK-PUBLIC-SUBNET<br/>10.60.10.0/24]
        Attack[Authorized Attack Host]
        ASubnet --> Attack
    end

    subgraph SVPC[SOC-LAB-VPC · 10.50.0.0/16]
        Target[SOC-TARGET-SUBNET<br/>10.50.10.0/24]
        SIEM[SOC-SIEM-SUBNET<br/>10.50.20.0/24]
        Monitoring[SOC-MONITORING-SUBNET<br/>10.50.30.0/24]
        Web[Public Web Target]
        Splunk[Splunk Enterprise]
        Target --> Web
        SIEM --> Splunk
        Monitoring -.-> Future[Later scenarios:<br/>DNS / Victim / Defense Components]
    end

    Attack --> Internet
    Internet --> DNS
    DNS --> Web
    Web --> Splunk

    X{{No VPC peering / no private route between VPCs}}
```

## Trust boundaries

### Public attack boundary

`ATTACK-LAB-VPC` is a separate address space with its own Internet Gateway and public route table. The attack host reaches public lab services through the Internet. It does not route directly to SOC private addresses.

### Public target boundary

`SOC-TARGET-SUBNET` is where intentionally public lab services are placed. Exposure is controlled by service-specific security groups rather than opening the entire VPC.

### SIEM boundary

`SOC-SIEM-SUBNET` contains Splunk and the AI bridge as they are deployed. Splunk Web is restricted to the team rather than exposed as a general public service. Log ingestion ports are allowed only from approved sources.

### Monitoring boundary

`SOC-MONITORING-SUBNET` uses the private SOC route table. It is reserved for later DNS/victim/defense components that should not be directly reachable from the Internet.

## Routing principle

```text
SOC public subnets     -> 0.0.0.0/0 -> SOC-LAB-IGW
SOC monitoring subnet -> local VPC route only
Attack public subnet  -> 0.0.0.0/0 -> ATTACK-LAB-IGW
```

No VPC peering, Transit Gateway or cross-VPC private route is part of the base design.

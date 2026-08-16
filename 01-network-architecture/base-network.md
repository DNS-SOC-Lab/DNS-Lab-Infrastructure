# Base Network Architecture

## Design objective

Keep the attacker network logically separate from the SOC network while still allowing realistic public-facing DNS and web interaction. Internal SOC communication stays inside `SOC-LAB-VPC`; the attacker does not receive a private route to `10.50.0.0/16`.

Public DNS is also separated by responsibility: Hostinger remains the registrar, Route 53 is authoritative for the parent domain, and a separate Route 53 child zone serves the SOC lab namespace.

## VPC and public DNS layout

```mermaid
flowchart TB
    Registrar[Hostinger<br/>Registrar]
    Internet((Internet / .tech))
    Parent[Route 53 Parent Zone<br/>abdul4rehman215.tech]
    Child[Route 53 Child Zone<br/>soclab.abdul4rehman215.tech]
    Existing[Existing parent services<br/>A: 2.57.91.91<br/>mail DNS preserved]

    subgraph AVPC[ATTACK-LAB-VPC · 10.60.0.0/16]
        ASubnet[ATTACK-PUBLIC-SUBNET<br/>10.60.10.0/24]
        Attack[dns-attack01<br/>10.60.10.10]
        ASubnet --> Attack
    end

    subgraph SVPC[SOC-LAB-VPC · 10.50.0.0/16]
        Target[SOC-TARGET-SUBNET<br/>10.50.10.0/24]
        SIEM[SOC-SIEM-SUBNET<br/>10.50.20.0/24]
        Monitoring[SOC-MONITORING-SUBNET<br/>10.50.30.0/24]
        Web[dns-soc-web01<br/>10.50.10.10<br/>EIP 100.49.192.164]
        Splunk[dns-soc-splunk01<br/>10.50.20.10]
        Target --> Web
        SIEM --> Splunk
        Monitoring -.-> Future[Later scenario-specific<br/>DNS / victim / defense components]
    end

    Registrar -. registrar nameservers .-> Parent
    Internet --> Parent
    Parent --> Existing
    Parent -->|NS delegation for soclab| Child
    Child -->|A 100.49.192.164| Web
    Attack --> Internet
    Web --> Splunk

    X{{No VPC peering / no private route between VPCs}}
```

The DNS authority chain is documented in more detail in [`dns-authority-and-delegation.md`](dns-authority-and-delegation.md).

## Trust boundaries

### Public attack boundary

`ATTACK-LAB-VPC` is a separate address space with its own Internet Gateway and public route table. The attack host reaches public lab services through the Internet. It does not route directly to SOC private addresses.

### Public DNS boundary

The parent and child Route 53 zones have separate authoritative nameserver sets. The parent zone owns `abdul4rehman215.tech` and delegates only `soclab.abdul4rehman215.tech` to the child zone. This creates a visible DNS authority boundary without changing the VPC separation model.

### Public target boundary

`SOC-TARGET-SUBNET` is where intentionally public lab services are placed. `soclab.abdul4rehman215.tech` resolves to the Elastic IP associated with `dns-soc-web01`. Exposure is controlled by service-specific security groups rather than opening the entire VPC.

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

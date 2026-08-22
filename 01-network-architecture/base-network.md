<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 01 Network Architecture](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Base Network Architecture

The lab uses two non-overlapping VPCs and no private route between them.

```text
ATTACK-LAB-VPC  10.60.0.0/16
    ATTACK-PUBLIC-SUBNET 10.60.10.0/24
        dns-attack01 10.60.10.10

SOC-LAB-VPC     10.50.0.0/16
    SOC-TARGET-SUBNET     10.50.10.0/24
        dns-soc-web01     10.50.10.10
        SOC-MONITORING-NAT (public NAT)

    SOC-SIEM-SUBNET       10.50.20.0/24
        dns-soc-splunk01  10.50.20.10

    SOC-MONITORING-SUBNET 10.50.30.0/24  private
        dns-soc-resolver01 10.50.30.10
        dns-soc-victim01   10.50.30.20
        dns-soc-sinkhole01 10.50.30.30
```

## Trust boundaries

- The attack VPC and SOC VPC do not use VPC peering, Transit Gateway or a private cross-VPC route.
- The public Web target is intentionally reachable through the Internet on 80/443.
- Splunk Web is restricted to approved team source addresses; administration uses SSM.
- The Scenario 02 resolver and sinkhole are private-only.
- `SG-DNS` accepts DNS only from the victim security group.
- `SG-SINKHOLE` accepts HTTP only from the victim security group.
- Universal Forwarders use the VPC-local path to `10.50.20.10:9997`.

## Routing

### SOC public subnets

`SOC-TARGET-SUBNET` and `SOC-SIEM-SUBNET` use the SOC public route table and Internet Gateway where the current design requires public reachability.

### SOC monitoring subnet

`SOC-MONITORING-SUBNET` is explicitly associated with `SOC-PRIVATE-RT`:

```text
10.50.0.0/16 -> local
0.0.0.0/0    -> SOC-MONITORING-NAT
```

`SOC-MONITORING-NAT` is in the public `SOC-TARGET-SUBNET` in `us-east-1c`.

The resolver's normal DNS path does not depend on the NAT:

```text
10.50.30.20 -> 10.50.30.10:53 -> 10.50.0.2 -> DNS authority
```

## Public DNS authority

Hostinger remains the registrar. Route 53 hosts the parent zone and delegates `soclab.abdul4rehman215.tech` to the child hosted zone. The public child zone remains separate from the private Scenario 02 RPZ/sinkhole control.

## Scenario 02 defender path

```text
Victim 10.50.30.20
    |
    | UDP/TCP 53
    v
Resolver 10.50.30.10 / Unbound
    |
    +--> AWS VPC Resolver 10.50.0.2 -> normal DNS
    |
    +--> resolver logs -> UF -> Splunk 10.50.20.10:9997
    |
    +--> RPZ local data when deliberately enabled
             |
             v
        Sinkhole 10.50.30.30:80
             |
             +--> Nginx access log -> UF -> Splunk
```

The final RPZ state keeps enforcement disabled until a later human-approved exercise response.

See [`diagrams/base-network.mmd`](diagrams/base-network.mmd) and [`diagrams/scenario-02-defender-dns.mmd`](diagrams/scenario-02-defender-dns.mmd).

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 01 Network Architecture](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

# VPC, Subnets and Routing

**Status:** Implemented  
**Implementation owner:** [_Abdul-Rehman_](https://github.com/abdul4rehman215)  
**Region:** `us-east-1`

## Objective

Build the network foundation manually instead of relying on the default VPC. The attacker and SOC environments use non-overlapping address spaces and do not have a private route between them.

## VPC design

| VPC | CIDR | Purpose |
|---|---|---|
| `SOC-LAB-VPC` | `10.50.0.0/16` | SOC, target and monitoring resources |
| `ATTACK-LAB-VPC` | `10.60.0.0/16` | Separate attack/simulation environment |

![SOC lab VPC](screenshots/network-foundation/soc-lab-vpc.png)

*`SOC-LAB-VPC` provides the `10.50.0.0/16` address space used by the SOC side of the lab.*

![Attack lab VPC](screenshots/network-foundation/attack-lab-vpc.png)

*`ATTACK-LAB-VPC` uses a separate `10.60.0.0/16` range so the attacker environment does not overlap the SOC network.*

## Subnet layout

| Subnet | CIDR | VPC | Routing purpose |
|---|---|---|---|
| `SOC-TARGET-SUBNET` | `10.50.10.0/24` | SOC | Public target subnet |
| `SOC-SIEM-SUBNET` | `10.50.20.0/24` | SOC | Public SIEM subnet with restricted service exposure |
| `SOC-MONITORING-SUBNET` | `10.50.30.0/24` | SOC | Private monitoring/defense subnet |
| `ATTACK-PUBLIC-SUBNET` | `10.60.10.0/24` | Attack | Public attack/simulation subnet |

![Configured subnets](screenshots/network-foundation/subnets.png)

*The subnet inventory confirms the planned segmentation inside both VPCs.*

## Internet gateways

Each VPC has its own Internet Gateway:

- `SOC-LAB-IGW` → `SOC-LAB-VPC`
- `ATTACK-LAB-IGW` → `ATTACK-LAB-VPC`

![Internet gateways](screenshots/network-foundation/internet-gateways.png)

*Separate Internet Gateways preserve the two-VPC design while allowing the intended public subnets to reach the Internet.*

## SOC public routing

`SOC-PUBLIC-RT` contains the VPC-local route and a default route through `SOC-LAB-IGW`:

```text
10.50.0.0/16 -> local
0.0.0.0/0    -> SOC-LAB-IGW
```

![SOC public routes](screenshots/network-foundation/soc-public-routes.png)

*The default route makes the associated SOC target and SIEM subnets Internet-routable.*

The route table is associated with:

- `SOC-TARGET-SUBNET`
- `SOC-SIEM-SUBNET`

![SOC public subnet associations](screenshots/network-foundation/soc-public-associations.png)

*Only the intended public SOC subnets are associated with the public route table.*

## SOC private routing

The original baseline `SOC-PRIVATE-RT` contained only the VPC-local route. During the Scenario 02 defender-DNS build, the monitoring subnet received controlled outbound egress through a public NAT Gateway while remaining private:

```text
10.50.0.0/16 -> local
0.0.0.0/0    -> SOC-MONITORING-NAT
```

`SOC-MONITORING-NAT` is deployed in `SOC-TARGET-SUBNET` in `us-east-1c`. It supports package/management egress for the private resolver/victim/sinkhole hosts; it does not turn them into public services.

The historical baseline screenshot below records the route table before Scenario 02 activation:

![SOC private routes](screenshots/network-foundation/soc-private-routes.png)

It remains associated with:

- `SOC-MONITORING-SUBNET`

![SOC private subnet association](screenshots/network-foundation/soc-private-associations.png)

Current Scenario 02 route/NAT evidence is in [`08-scenario-02-defender-dns.md`](08-scenario-02-defender-dns.md).

## Attacker routing

`ATTACK-PUBLIC-RT` contains:

```text
10.60.0.0/16 -> local
0.0.0.0/0    -> ATTACK-LAB-IGW
```

![Attack public routes](screenshots/network-foundation/attack-public-routes.png)

*The attacker subnet receives Internet access through the attacker VPC's own Internet Gateway.*

The route table is associated with:

- `ATTACK-PUBLIC-SUBNET`

![Attack subnet association](screenshots/network-foundation/attack-public-associations.png)

*The attack host remains in its own VPC and public subnet rather than sharing the SOC network.*

## VPC separation

No VPC peering, Transit Gateway or custom `10.60.0.0/16 <-> 10.50.0.0/16` route is configured. The attacker therefore does not receive private network access to `10.50.0.0/16`; scenario traffic must use intentionally exposed public lab services.

## Result

The implemented network matches the locked design: two isolated VPCs, explicit subnet segmentation, separate Internet Gateways, public routing only where intended, and a private monitoring subnet now used by the Scenario 02 resolver/victim/sinkhole platform. `SOC-MONITORING-SUBNET` uses `SOC-PRIVATE-RT` with `0.0.0.0/0` through `SOC-MONITORING-NAT`; the three Scenario 02 EC2s remain private.

## Evidence index

- [SOC VPC](screenshots/network-foundation/soc-lab-vpc.png)
- [Attack VPC](screenshots/network-foundation/attack-lab-vpc.png)
- [Subnets](screenshots/network-foundation/subnets.png)
- [Internet Gateways](screenshots/network-foundation/internet-gateways.png)
- [SOC public routes](screenshots/network-foundation/soc-public-routes.png)
- [SOC public subnet associations](screenshots/network-foundation/soc-public-associations.png)
- [SOC private routes](screenshots/network-foundation/soc-private-routes.png)
- [SOC private subnet association](screenshots/network-foundation/soc-private-associations.png)
- [Attack public routes](screenshots/network-foundation/attack-public-routes.png)
- [Attack subnet association](screenshots/network-foundation/attack-public-associations.png)

# VPC, Subnets and Routing

**Status:** Implemented  
**Implementation owner:** Abdul-Rehman  
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

`SOC-PRIVATE-RT` contains only the VPC-local route:

```text
10.50.0.0/16 -> local
```

![SOC private routes](screenshots/network-foundation/soc-private-routes.png)

*The monitoring route table has no `0.0.0.0/0` Internet Gateway route.*

It is associated with:

- `SOC-MONITORING-SUBNET`

![SOC private subnet association](screenshots/network-foundation/soc-private-associations.png)

*The monitoring subnet is kept on the private route table instead of inheriting the public SOC routing path.*

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

The implemented network matches the locked design: two isolated VPCs, explicit subnet segmentation, separate Internet Gateways, public routing only where intended, and a private monitoring subnet reserved for later scenario requirements.

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

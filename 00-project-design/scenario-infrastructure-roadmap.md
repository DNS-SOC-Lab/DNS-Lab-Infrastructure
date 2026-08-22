<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Scenario Infrastructure Roadmap

**Status:** Scenario 02 defender DNS infrastructure complete; Scenario 03–04 additions remain just-in-time.

The shared AWS/Splunk/Web/DNS/AI platform is not rebuilt for each scenario. New infrastructure is added only when the scenario needs a real new network/service behavior.

## Shared foundation already complete

- `SOC-LAB-VPC` — `10.50.0.0/16`
- `ATTACK-LAB-VPC` — `10.60.0.0/16`
- Route 53 parent + delegated `soclab` child zone
- `dns-soc-web01` + Nginx/HTTPS + Web UF
- `dns-soc-splunk01` + Splunk Enterprise + project indexes
- Route 53 public query logs
- VPC Flow Logs
- CloudTrail
- AWS VPC Resolver Query Logs
- shared `dns-soc-ai-bridge`
- `dns-attack01`

## Scenario 01 — DNS Reconnaissance

No additional infrastructure is required. Scenario 01 uses the existing public DNS, public Web target, AWS telemetry, Splunk and shared AI bridge.

## Scenario 02 — DGA + High NXDOMAIN

**Infrastructure: COMPLETE**

### Implemented private hosts

| Host | Address | Subnet | Purpose |
|---|---|---|---|
| `dns-soc-resolver01` | `10.50.30.10` | `SOC-MONITORING-SUBNET` | Unbound defender resolver, RPZ and resolver telemetry |
| `dns-soc-victim01` | `10.50.30.20` | `SOC-MONITORING-SUBNET` | Controlled client for later DGA/high-NXDOMAIN generation |
| `dns-soc-sinkhole01` | `10.50.30.30` | `SOC-MONITORING-SUBNET` | Reusable private Nginx containment/evidence endpoint |

The roles remain separate. Splunk is not used as the DNS resolver, and the victim is not co-hosted with the resolver.

### Private egress

Created `SOC-MONITORING-NAT` in the public `SOC-TARGET-SUBNET` (`us-east-1c`). `SOC-PRIVATE-RT` now provides:

```text
10.50.0.0/16 -> local
0.0.0.0/0    -> SOC-MONITORING-NAT
```

This lets the private Scenario 02 hosts install packages and reach required external management endpoints without public IPv4 addresses.

Normal DNS forwarding is separate and uses AWS VPC Resolver `10.50.0.2`.

### Security groups

```text
SG-DNS
  UDP/TCP 53 <- SG-VICTIM

SG-VICTIM
  no inbound application service

SG-SINKHOLE
  TCP 80 <- SG-VICTIM

SG-SPLUNK
  TCP 9997 <- SG-DNS
  TCP 9997 <- SG-VICTIM   (reserved; victim UF not installed yet)
  TCP 9997 <- SG-SINKHOLE
```

DNS `53` is not exposed publicly.

### Resolver path

```text
Victim 10.50.30.20
       |
       v
Unbound 10.50.30.10
       |
       v
AWS VPC Resolver 10.50.0.2
       |
       v
Route 53 / Internet DNS
```

Unbound logs queries/replies, forwards to `10.50.0.2`, and now includes RPZ support through the `respip iterator` module chain.

### Resolver telemetry

```text
Unbound -> syslog -> rsyslog filtered file
        -> /var/log/dns-soc/unbound.log
        -> Splunk UF -> TCP 9997
        -> index=dns_soc_dns / sourcetype=unbound:dns
```

Validated fields include `event_type`, `client_ip`, `qname`, `qtype`, `rcode`, `response_time`, `cache_flag` and `response_size` where the event provides them.

### Sinkhole path

```text
Unbound RPZ
   -> controlled local-data answer 10.50.30.30
   -> dns-soc-sinkhole01 / Nginx
   -> /var/log/nginx/access.log
   -> Splunk UF
   -> index=dns_soc_web / sourcetype=nginx:access
```

The RPZ path was tested first in disabled/log-only behavior, then with one controlled redirect, then reset to disabled enforcement. The reusable control remains available for future human-approved response testing.

### Completed infrastructure documents

- [`../02-aws-build/08-scenario-02-defender-dns.md`](../02-aws-build/08-scenario-02-defender-dns.md)
- [`../03-splunk-build/07-scenario-02-dns-onboarding.md`](../03-splunk-build/07-scenario-02-dns-onboarding.md)
- [`../01-network-architecture/diagrams/scenario-02-defender-dns.mmd`](../01-network-architecture/diagrams/scenario-02-defender-dns.mmd)

### Not part of infrastructure completion

The following remain in the Scenario 02 repository and are not claimed complete here:

- normal baseline;
- controlled DGA/high-NXDOMAIN simulation;
- dashboard/hunting;
- rule-based DGA detection and tuning;
- scheduled alert;
- optional Isolation Forest comparison;
- Scenario 02 AI profile;
- SOC investigation;
- human-approved response exercise and final evidence chain.

## Scenario 03 — Fast Flux

Reuse the completed Scenario 02 resolver/victim/sinkhole platform.

Only add what Fast Flux genuinely requires:

- team-controlled temporary destination endpoints if not already available;
- temporary short-TTL `flux.soclab...` A records;
- controlled answer rotation;
- resolver + VPC Flow correlation;
- cleanup/reset after the exercise.

No new VPC, Splunk server, AI bridge or second sinkhole is expected.

## Scenario 04 — DNS Tunneling

Reuse the Scenario 02 defender DNS platform.

Potential additional infrastructure is conditional:

- if the final controlled tunneling simulation can be represented through the existing resolver/public DNS path, reuse it;
- if the exercise genuinely requires an authoritative server that receives encoded labels, deploy one controlled endpoint/delegation at Scenario 04 preparation time;
- reuse the existing RPZ/sinkhole path for human-approved containment verification.

Do not create a permanent authoritative tunnel service before the scenario needs it.

## Infrastructure discipline

For every new scenario resource:

1. record the reason it is needed;
2. keep addressing and SG rules inside the locked network plan;
3. validate service and telemetry before detection engineering;
4. preserve repository-safe configuration/evidence;
5. reset temporary DNS/containment changes after the exercise;
6. never publish credentials, API keys, private keys or sensitive account details.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 00 Project Design](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

# Scenario DNS Plan

This file separates the permanent public DNS foundation from scenario DNS behavior and the now-completed private defender DNS platform.

For EC2/security-group/network details, see [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md).

## Permanent child-zone baseline

The Route 53 child hosted zone `soclab.abdul4rehman215.tech` keeps five permanent record sets:

| Name | Type | Value | TTL | Purpose |
|---|---|---|---:|---|
| `soclab.abdul4rehman215.tech` | A | `100.49.192.164` | 300 | Main public web target |
| `soclab.abdul4rehman215.tech` | NS | Four Route 53 child nameservers | 172800 | Child-zone authority |
| `soclab.abdul4rehman215.tech` | SOA | Route 53-managed SOA | 900 | Child-zone authority metadata |
| `soclab.abdul4rehman215.tech` | TXT | `"DNS SOC Training Lab"` | 300 | Controlled reconnaissance fixture |
| `www.soclab.abdul4rehman215.tech` | CNAME | `soclab.abdul4rehman215.tech.` | 300 | Secondary public web hostname |

## Scenario 01 — DNS Reconnaissance

No additional public DNS record is required. The existing A/NS/SOA/TXT/CNAME baseline is sufficient for record enumeration and HTTPS follow-up.

## Scenario 02 — DGA / High NXDOMAIN

**Infrastructure status:** Complete.  
**Scenario simulation/detection status:** Not started.

Do **not** create random DGA records in Route 53.

Controlled names will conceptually use:

```text
<generated-label>.dga.soclab.abdul4rehman215.tech
```

Those names normally do not exist, producing real `NXDOMAIN` through the implemented path:

```text
dns-soc-victim01
10.50.30.20
      |
      v
dns-soc-resolver01 / Unbound
10.50.30.10
      |
      v
AWS VPC Resolver 10.50.0.2
      |
      v
Route 53 authority / Internet DNS
      |
      v
NXDOMAIN when the generated name does not exist
```

This supports later metrics such as:

- NXDOMAIN count and ratio;
- unique names;
- query rate;
- label length/randomness;
- repeated client behavior;
- query type and time pattern.

### Reusable RPZ/sinkhole path

Scenario 02 infrastructure also implemented a private sinkhole at `10.50.30.30` and an Unbound RPZ policy.

Normal/safe state:

```text
controlled generated/test name
        -> Unbound
        -> normal upstream result / NXDOMAIN
```

Approved containment state during a future exercise:

```text
controlled name/pattern
        -> Unbound RPZ match
        -> 10.50.30.30
        -> private Nginx sinkhole
        -> Splunk evidence
```

The infrastructure test proved this path once and then restored `rpz-action-override: disabled`. That test proves the control works; it is **not** the Scenario 02 incident-response exercise.

## Scenario 03 — Fast Flux DNS

Scenario 03 reuses the Scenario 02 resolver/victim/sinkhole platform but needs a temporary public DNS change because controlled Fast Flux behavior requires changing address answers and a short TTL.

Planned namespace:

```text
flux.soclab.abdul4rehman215.tech
```

At Scenario 03 preparation time:

1. provision or identify only team-controlled public endpoints;
2. create a controlled A RRset;
3. use a deliberately short scenario TTL;
4. rotate only those controlled addresses;
5. capture DNS-answer and network-flow evidence;
6. remove/reset the temporary record after the exercise.

Do not use random third-party Internet addresses to imitate Fast Flux.

## Scenario 04 — DNS Tunneling

Do **not** create a normal static Route 53 A record just to reserve the tunneling name.

Planned namespace:

```text
tunnel.soclab.abdul4rehman215.tech
```

The final design must be chosen when the scenario is prepared. Reuse the Scenario 02 resolver/victim/sinkhole platform. Add a separate authoritative DNS endpoint/delegation only if the controlled tunneling simulation genuinely needs to receive and interpret the encoded queries.

The traffic must contain harmless lab-generated data only.

## DNS cleanup rule

Temporary scenario DNS changes must be documented with:

- what was added or changed;
- expected TTL/behavior;
- exact scenario purpose;
- before/after validation;
- reset/removal state after the exercise.

The permanent child-zone baseline stays stable unless a project-level change is deliberately approved.

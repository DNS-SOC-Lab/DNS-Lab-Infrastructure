# Scenario DNS Plan

This file separates the **permanent public DNS foundation** from DNS behavior that is created only when a later scenario needs it.

The goal is to keep Route 53 stable between exercises while still documenting exactly what DNS work remains for DGA, Fast Flux, DNS Tunneling and sinkhole/containment testing.

## Permanent child-zone baseline

The Route 53 child hosted zone `soclab.abdul4rehman215.tech` now contains five permanent record sets:

| Name | Type | Value | TTL | Purpose |
|---|---|---|---:|---|
| `soclab.abdul4rehman215.tech` | A | `100.49.192.164` | 300 | Main public web target |
| `soclab.abdul4rehman215.tech` | NS | Four Route 53 child nameservers | 172800 | Child-zone authority |
| `soclab.abdul4rehman215.tech` | SOA | Route 53-managed SOA | 900 | Child-zone authority metadata |
| `soclab.abdul4rehman215.tech` | TXT | `"DNS SOC Training Lab"` | 300 | Controlled reconnaissance fixture |
| `www.soclab.abdul4rehman215.tech` | CNAME | `soclab.abdul4rehman215.tech.` | 300 | Secondary public web hostname |

The main hostname and `www` alias are both intended to be supported by Nginx and by the public TLS certificate.

## Scenario 01 - DNS Reconnaissance

No additional Route 53 record is required before the first scenario.

The permanent child zone already gives the exercise useful authoritative data:

- A record for the public web target;
- NS and SOA authority information;
- TXT training fixture;
- `www` CNAME that leads back to the main web target.

The authorized simulation can also query record types that are intentionally not configured, such as AAAA or MX. A missing record type at an existing name is still useful reconnaissance behavior even when it returns no data.

The web alias also supports a realistic DNS-to-web follow-up path:

```text
DNS enumeration
      |
      +-- soclab A / NS / SOA / TXT
      +-- www CNAME
      |
      v
HTTPS follow-up
      |
      v
Nginx access log
      |
      v
Splunk correlation
```

## Scenario 02 - DGA / High NXDOMAIN

Do **not** pre-create random DGA records in Route 53.

The scenario needs many generated names that do not exist so the defender can measure NXDOMAIN behavior, query volume, label length/randomness and unique-name counts.

A controlled pattern can use names conceptually under:

```text
<generated-label>.dga.soclab.abdul4rehman215.tech
```

The exact generator and client path are implemented in the Scenario 02 environment. The public child zone should not be filled with those generated names.

## Scenario 03 - Fast Flux DNS

This scenario requires a later **temporary DNS change** because real Fast Flux behavior needs controlled changing address answers and a short TTL.

Planned namespace:

```text
flux.soclab.abdul4rehman215.tech
```

At Scenario 03 preparation time:

1. provision or identify only team-controlled public endpoints;
2. create a controlled A RRset for `flux.soclab.abdul4rehman215.tech`;
3. use a deliberately short scenario TTL;
4. rotate the controlled addresses according to the scenario plan;
5. capture DNS-answer and network-flow evidence;
6. remove or reset the temporary record after the exercise.

Do not use random third-party Internet addresses to imitate Fast Flux.

## Scenario 04 - DNS Tunneling

Do **not** create a normal static Route 53 A record now just to reserve the tunneling name.

Planned namespace:

```text
tunnel.soclab.abdul4rehman215.tech
```

The useful telemetry in this scenario comes from the future team-controlled DNS resolver / DNS service path, where harmless encoded labels and query patterns can be observed and forwarded to Splunk.

The exact authoritative or forwarding behavior is decided when the resolver component is implemented. Route 53 is changed only if the final Scenario 04 design actually requires a public delegation or record.

## Sinkhole / containment

Sinkholing belongs to the defender-controlled resolver path, not the permanent public Route 53 baseline. The capability is introduced with the Scenario 02 resolver/victim infrastructure and then reused by later response exercises. Scenario 04 requires the clearest before/after containment proof.

The planned sinkhole address remains:

```text
10.50.30.30
```

The intended response proof is:

```text
Before containment
Victim -> DNS resolver -> suspicious controlled destination

After containment
Victim -> DNS resolver -> 10.50.30.30 sinkhole
```

That gives the incident-response team a measurable before/after result without turning the public child zone into the containment mechanism. Scenario 02 establishes the capability; Scenario 03 may reuse it when useful; Scenario 04 explicitly demonstrates sinkhole/block containment and verification.

## Change-control rule

The five-record child-zone baseline is treated as the stable public DNS foundation.

Later scenario DNS changes must be:

- tied to a specific scenario;
- created only when the scenario design requires them;
- limited to team-controlled infrastructure;
- documented with the expected TTL and behavior;
- validated before the simulation;
- removed or reset after the scenario when they are temporary.

This keeps the public web/DNS foundation predictable while allowing later scenarios to introduce the DNS behavior they actually need.

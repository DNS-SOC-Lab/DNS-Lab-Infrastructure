# Scenario-Specific Infrastructure Roadmap

**Status:** Planned design reference — resources are created only when the matching scenario reaches preparation.

The shared AWS, DNS, Web, Splunk and AI foundation is complete. The lab does **not** enter another large common-infrastructure build. Future AWS and DNS work is deliberately small, scenario-specific and added just in time.

This document answers one practical question:

> **When a scenario starts, what infrastructure still has to be built, changed or temporarily enabled?**

The implementation record still belongs in [`../02-aws-build/`](../02-aws-build/) only after the resource really exists. Scenario-specific dashboards, SPL, simulations, analyst findings and incident-response evidence remain in the separate scenario repositories.

## Shared foundation reused by every scenario

The following components are already available and should not be rebuilt for each exercise:

- `SOC-LAB-VPC` — `10.50.0.0/16`;
- `ATTACK-LAB-VPC` — `10.60.0.0/16`;
- no VPC peering and no private attacker-to-SOC route;
- `dns-attack01` — `10.60.10.10`;
- `dns-soc-web01` — `10.50.10.10`, Nginx/HTTPS and Universal Forwarder;
- `dns-soc-splunk01` — `10.50.20.10`, Splunk Enterprise `10.4.2`;
- Route 53 parent/child authority for `soclab.abdul4rehman215.tech`;
- Route 53 public authoritative query logs;
- VPC Flow Logs for both existing VPCs;
- CloudTrail;
- AWS VPC Resolver Query Logging for both existing VPCs;
- the shared `dns-soc-ai-bridge`, validated through Splunk webhook -> OpenAI -> internal HEC -> `dns_soc_ai`.

## Scenario infrastructure summary

| Scenario | Shared foundation reused | Additional infrastructure / change | Lifetime |
|---|---|---|---|
| **01 — DNS Reconnaissance** | Existing attacker, Route 53, Web/Nginx, Splunk, AWS telemetry and AI | **No new scenario-specific AWS infrastructure expected** | Existing foundation |
| **02 — DGA + High NXDOMAIN** | Splunk, AWS telemetry, monitoring subnet, AI | `dns-soc-resolver01`, `dns-soc-victim01`, DNS/victim security groups, defender DNS logging, reusable sinkhole capability | Persistent shared expansion for Scenarios 02–04 |
| **03 — Fast Flux** | Scenario 02 resolver/victim/sinkhole platform | Temporary `flux.soclab...` DNS behavior, short TTL, multiple team-controlled destination endpoints/IPs if required | Temporary / reset after exercise |
| **04 — DNS Tunneling** | Scenario 02 resolver/victim/sinkhole platform | Controlled `tunnel.soclab...` behavior; optional authoritative DNS endpoint only if the final exercise genuinely requires it | Mostly temporary / scenario-controlled |

## Scenario 01 — DNS Reconnaissance & Enumeration

### Infrastructure decision

**No new scenario-specific EC2, VPC, subnet or DNS server is expected.**

Scenario 01 intentionally proves that the shared foundation is already enough to run a complete SOC exercise:

```text
dns-attack01
    |
    | public DNS reconnaissance
    v
Route 53 child hosted zone
    |
    +--> Route 53 public query telemetry
    |
    +--> discovered public web target
              |
              +--> Nginx / Universal Forwarder
              +--> VPC Flow Logs
              v
            Splunk
              |
              v
        Shared AI bridge
```

The scenario repository owns dashboard engineering, baseline, detection logic, tuning, alerting, AI profile, simulation, SOC analysis and response evidence.

### Infrastructure checkpoint before Scenario 01

- Shared AI foundation complete and health-tested.
- Existing Web and AWS telemetry still fresh in Splunk.
- No additional Route 53 records beyond the stable public baseline unless the scenario design explicitly changes.

## Scenario 02 — DGA + High NXDOMAIN

Scenario 02 is the **last major permanent infrastructure expansion currently planned**.

### Planned systems

| Component | Planned location | Purpose |
|---|---|---|
| `dns-soc-resolver01` | `10.50.30.10` | Team-controlled recursive/forwarding DNS path and defender-visible query logging |
| `dns-soc-victim01` | `10.50.30.20` | Controlled client that produces DGA-style DNS behavior |
| Sinkhole service / endpoint | `10.50.30.30` | Reusable defender containment target if implemented as a separate service |

All three addresses are already reserved in [`../01-network-architecture/cidr-plan.md`](../01-network-architecture/cidr-plan.md).

### AWS / network work to perform at Scenario 02 preparation

- launch the resolver and victim EC2 systems in `SOC-MONITORING-SUBNET`;
- create the DNS/victim security groups only when the systems are deployed;
- allow DNS TCP/UDP `53` only along the intended client → resolver path;
- keep the resolver from becoming an Internet-facing open recursive resolver;
- configure SSM/administration without adding unnecessary public management exposure;
- determine the controlled package/update egress method for the private monitoring subnet;
- install and configure the approved resolver software, expected to be BIND or Unbound after the final implementation choice;
- forward useful resolver telemetry into Splunk;
- point `dns-soc-victim01` at the team-controlled resolver;
- establish the reusable sinkhole/deny capability and prove a before/after DNS response path.

### Important egress decision

`SOC-MONITORING-SUBNET` currently has only the local VPC route. That is intentional. Before the Scenario 02 hosts are deployed, the team must choose the minimum controlled method required for administration, package updates and any approved upstream DNS behavior.

Possible designs can be evaluated at that time, but this roadmap does **not** preselect a NAT gateway, public address or endpoint architecture before the real requirement is known.

### DGA DNS rule

Do not fill Route 53 with generated records. Names such as:

```text
<generated-label>.dga.soclab.abdul4rehman215.tech
```

should normally remain nonexistent so NXDOMAIN ratio, unique-name volume and label behavior can be measured from real DNS events.

## Scenario 03 — Fast Flux DNS

Scenario 03 should **reuse Scenario 02 infrastructure**, not build another monitoring platform.

### Temporary additions

At scenario preparation time:

1. provision or identify a small set of **team-controlled** reachable endpoints/IP addresses;
2. create the temporary `flux.soclab.abdul4rehman215.tech` A RRset;
3. use the short TTL approved for the exercise;
4. rotate only the controlled addresses according to the test plan;
5. preserve Route 53/Resolver telemetry and VPC Flow evidence showing the client's follow-up destinations;
6. remove or reset temporary records/endpoints after the exercise.

The exact number and type of endpoints are intentionally deferred until Scenario 03. The scenario needs enough controlled address churn to prove the behavior; it does not need a new VPC or a large fleet.

### Safety / realism rule

Never use unrelated third-party public IP addresses to imitate Fast Flux. The DNS answers and destination infrastructure must remain team-controlled.

## Scenario 04 — DNS Tunneling

Scenario 04 again reuses the resolver, victim, Splunk and sinkhole path created for Scenario 02.

### Planned additions

- use the controlled namespace `tunnel.soclab.abdul4rehman215.tech`;
- generate only harmless synthetic data inside DNS labels/queries;
- ensure the client DNS path traverses the defender-visible resolver;
- collect DNS structure/frequency plus endpoint/network context;
- reuse the sinkhole/block path for clear before/after containment evidence.

### Conditional authoritative service

A separate authoritative DNS endpoint is **not automatically required**.

It should be added only if the final Scenario 04 design needs genuine authoritative request/response behavior that cannot be demonstrated through the existing controlled DNS path. If added, it must be team-controlled, narrowly scoped to the lab namespace and documented as Scenario 04 infrastructure.

No real sensitive data is moved during the exercise.

## Scenario infrastructure change-control rule

Every future infrastructure addition must follow this sequence:

```text
Scenario requirement
      ↓
Design / security decision
      ↓
Build only the minimum resource
      ↓
Validate networking + telemetry
      ↓
Run scenario
      ↓
Keep reusable resources OR remove temporary resources
      ↓
Record the actual implementation in 02-aws-build/
```

For every scenario-specific AWS change, record:

- resource names and purpose;
- VPC/subnet/security-group placement;
- DNS changes and TTLs;
- telemetry path into Splunk;
- whether the resource is permanent, reusable or temporary;
- validation evidence;
- cleanup/reset action where applicable.

## Expected later AWS build documents

These filenames are **future placeholders in the roadmap only**. They should not be created until the implementation exists:

```text
02-aws-build/
├── 08-scenario-02-defender-dns.md
├── 09-scenario-03-fast-flux-infrastructure.md
└── 10-scenario-04-tunneling-infrastructure.md
```

Scenario 01 does not currently need a new AWS build file because its infrastructure already exists.

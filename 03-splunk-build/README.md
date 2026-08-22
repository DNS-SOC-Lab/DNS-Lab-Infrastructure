# Splunk Build

**Status:** Gates A, B and C complete; shared AI return path complete; Scenario 02 resolver/sinkhole onboarding complete.  
**Splunk implementation / validation owner:** [_Sonia_](https://github.com/sonia11mansha415) — Detection Engineer

This folder records the deployed Splunk Enterprise platform on `dns-soc-splunk01`, Web telemetry, AWS telemetry, and the completed Scenario 02 resolver/sinkhole data-quality path.

Scenario-specific dashboards, detections, tuning, attack ground truth, ML models, analyst findings and IR evidence stay in the separate scenario repositories.

## Current platform

| Item | Implemented state |
|---|---|
| EC2 host | `dns-soc-splunk01` — `10.50.20.10` |
| Host OS | Ubuntu 24.04 LTS |
| Splunk image | `splunk/splunk:10.4.2` |
| KV Store | healthy / ready |
| Splunk Web | TCP `8000`, restricted by `SG-SPLUNK` |
| UF receiver | TCP `9997`, private source SGs only |
| Splunk Add-on for AWS | `8.2.1` |
| HEC `8088` | internal Docker path for AI bridge; not host-published |
| Public SSH | none; SSM administration |
| Persistent volumes | `dns-soc-splunk-etc`, `dns-soc-splunk-var` |

## Project indexes

| Index | Intended data | Current state |
|---|---|---|
| `dns_soc_web` | Public Web + private sinkhole Nginx telemetry | **Active / validated** |
| `dns_soc_linux` | Selected Linux security/system telemetry | Reserved until real source is onboarded |
| `dns_soc_aws` | Route 53, VPC Flow, CloudTrail, AWS Resolver Query Logs | **Active / validated** |
| `dns_soc_dns` | Team-controlled Unbound resolver telemetry | **Active / Scenario 02 validated** |
| `dns_soc_ai` | Shared AI triage/enrichment | **Active / validated** |

All indexes retain the existing 30-day lab policy.

## Completed data paths

```text
Gate B
Web Nginx -> UF -> 10.50.20.10:9997 -> dns_soc_web

Gate C
AWS telemetry -> Splunk Add-on for AWS -> dns_soc_aws

Scenario 02 resolver
Unbound -> rsyslog filtered file -> UF -> 10.50.20.10:9997
        -> dns_soc_dns / unbound:dns

Scenario 02 sinkhole
Nginx access.log -> UF -> 10.50.20.10:9997
                 -> dns_soc_web / nginx:access

Shared AI
Splunk alert -> internal bridge -> OpenAI -> internal HEC -> dns_soc_ai
```

## Scenario 02 resolver data now available

Validated identity:

```text
index      = dns_soc_dns
host       = dns-soc-resolver01
source     = /var/log/dns-soc/unbound.log
sourcetype = unbound:dns
```

Persistent real fields:

```text
event_type
client_ip
qname
qtype
rcode
response_time
cache_flag
response_size
```

`transport` is not claimed from the current Unbound text log. RPZ match/action context is present in raw events but has not been promoted to an invented normalized field.

Sinkhole identity:

```text
index      = dns_soc_web
host       = dns-soc-sinkhole01
source     = /var/log/nginx/access.log
sourcetype = nginx:access
```

See [`07-scenario-02-dns-onboarding.md`](07-scenario-02-dns-onboarding.md).

## Detection boundary

`dns_soc_dns` is ready for Scenario 02 baseline and detection engineering, but no DGA threshold or alert logic belongs in this shared infrastructure repository. The dedicated Scenario 02 repository must derive its thresholds from normal baseline and controlled DGA/high-NXDOMAIN behavior.

## Documents

- [`01-platform-deployment.md`](01-platform-deployment.md) — platform / Gate A
- [`02-data-structure-and-validation.md`](02-data-structure-and-validation.md) — indexes and all validated source identities
- [`03-backup-recovery-and-operations.md`](03-backup-recovery-and-operations.md) — persistence and operations
- [`04-troubleshooting-and-lessons.md`](04-troubleshooting-and-lessons.md) — platform root-cause lessons
- [`05-web-forwarder-onboarding.md`](05-web-forwarder-onboarding.md) — Web UF / Gate B
- [`06-aws-telemetry-onboarding.md`](06-aws-telemetry-onboarding.md) — AWS inputs / Gate C
- [`07-scenario-02-dns-onboarding.md`](07-scenario-02-dns-onboarding.md) — Unbound resolver + sinkhole UF and field validation
- [`forwarders/`](forwarders/) — repository-safe UF configuration
- [`validation/validation-searches.spl`](validation/validation-searches.spl) — onboarding/data-quality SPL, not scenario detection SPL
- [`screenshots/scenario-02/`](screenshots/scenario-02/) — curated Scenario 02 Splunk evidence

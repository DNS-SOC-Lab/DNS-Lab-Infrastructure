# Splunk Data Structure & Validation

## Design rule

Project telemetry is separated by purpose before ingestion starts. The lab does not use `main` as a catch-all project index.

A source is not considered onboarded only because events are visible. Every onboarding step must validate:

```text
index
host
source
sourcetype
timestamp
useful fields
```

## Project indexes

| Index | Purpose | Max size | Retention |
|---|---|---:|---:|
| `dns_soc_web` | Nginx access/error telemetry | 5 GiB | 30 days |
| `dns_soc_linux` | Selected Linux security/system telemetry | 5 GiB | 30 days |
| `dns_soc_aws` | Route 53, VPC Flow Logs, CloudTrail and later applicable AWS DNS telemetry | 15 GiB | 30 days |
| `dns_soc_dns` | Team-controlled resolver DNS data | 10 GiB | 30 days |
| `dns_soc_ai` | AI triage/enrichment returned to Splunk | 5 GiB | 30 days |

The final validation search returned all five indexes with `frozenTimePeriodInSecs=2592000`.

```spl
| rest splunk_server=local /services/data/indexes
| search title=dns_soc_*
| table title maxTotalDataSizeMB frozenTimePeriodInSecs
| sort title
```

![Project index configuration](screenshots/platform/65-splunk-custom-indexes.png)

## Web and Linux naming

The next onboarding phase uses the following stable identities.

| Data | Index | Planned sourcetype | Host | Source |
|---|---|---|---|---|
| Nginx access | `dns_soc_web` | `dns_soc:nginx:access` | `dns-soc-web01` | `/var/log/nginx/soclab_access.log` |
| Nginx error | `dns_soc_web` | `dns_soc:nginx:error` | `dns-soc-web01` | `/var/log/nginx/soclab_error.log` |
| Linux security/system | `dns_soc_linux` | Finalize from the real source used | `dns-soc-web01` | Real file/journal source only |

The Linux source must match what Ubuntu actually provides. The project does not create a fake `/var/log/auth.log` simply to satisfy an input path. If journald is the useful source, the collection method is documented when Gate B is implemented.

## AWS sourcetypes

AWS data goes to `dns_soc_aws`, but the project does **not** invent custom AWS sourcetype names before the real collection method exists.

When Route 53, VPC Flow Logs and CloudTrail are enabled and connected to Splunk, the team records the actual sourcetypes produced by the chosen supported input/add-on and validates them against sample events.

## Resolver data

`dns_soc_dns` is reserved for the team-controlled defender resolver introduced from Scenario 02 onward. The final sourcetype is chosen after BIND/Unbound and its log format are actually implemented.

The intended host identity is:

```text
host=dns-soc-resolver01
```

## AI data

The shared AI foundation later returns enrichment to:

```text
index=dns_soc_ai
sourcetype=dns_soc:ai:triage
```

The AI output is supporting context only. Raw DNS/network/server events remain the evidence source used by the SOC Analyst.

## Gate B — Web Forwarder validation

After the Universal Forwarder is installed on `dns-soc-web01`, generate fresh successful and failed web requests and validate the data in Splunk.

Suggested checks:

```spl
index=dns_soc_web host=dns-soc-web01 earliest=-15m
| stats count min(_time) as firstSeen max(_time) as lastSeen values(source) as sources values(sourcetype) as sourcetypes by host
| convert ctime(firstSeen) ctime(lastSeen)
```

```spl
index=dns_soc_web host=dns-soc-web01 earliest=-15m
| stats count by source sourcetype
```

```spl
index=dns_soc_linux host=dns-soc-web01 earliest=-15m
| stats count min(_time) as firstSeen max(_time) as lastSeen values(source) as sources values(sourcetype) as sourcetypes by host
| convert ctime(firstSeen) ctime(lastSeen)
```

Gate B should not pass until the team can show:

- fresh Nginx `200` and controlled `404` activity;
- expected `dns_soc_web` / `dns_soc_linux` placement;
- `host=dns-soc-web01`;
- correct source paths;
- expected sourcetypes;
- accurate event time;
- useful parsed fields for later investigation.

## Gate C — AWS telemetry validation

After AWS logging is enabled, validate each data family independently before building Scenario 01 detection logic.

| Data source | Main SOC value |
|---|---|
| Route 53 public query logs | Authoritative DNS reconnaissance evidence |
| VPC Flow Logs | L3/L4 network-flow context around public/server activity |
| CloudTrail | AWS API/control-plane changes |
| Resolver Query Logs, when applicable | Internal victim/resolver DNS activity in later stages |

The Detection Engineer records the real `index`, `host`, `source`, `sourcetype`, `_time` behavior and fields for each source. Dashboard/detection work starts only after this data-quality gate passes.

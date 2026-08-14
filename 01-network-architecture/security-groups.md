# Security Group Design

Security Groups are the primary service-level control in the base lab. The design starts with the minimum communication needed for the current stage and adds ports only when a scenario requires them.

## `SG-WEB`

Public target security group.

| Direction | Protocol / Port | Source / Destination | Reason |
|---|---|---|---|
| Inbound | TCP 80 | `0.0.0.0/0` | Public HTTP / redirect path |
| Inbound | TCP 443 | `0.0.0.0/0` | Public HTTPS target |
| Inbound | SSH 22 | None in baseline | Administration uses SSM where possible |
| Outbound | Required egress | As implemented | Updates, logging and application needs |

## `SG-SPLUNK`

SIEM access and log-receiver security group.

| Direction | Protocol / Port | Source | Reason |
|---|---|---|---|
| Inbound | TCP 8000 | Team public IPs only | Splunk Web |
| Inbound | TCP 9997 | Approved source SGs such as `SG-WEB` | Splunk Universal Forwarder ingestion |
| Inbound | TCP 8088 | Not public | HEC, enabled only when the internal design needs it |
| Inbound | TCP 8089 | Not public | Splunk management interface |
| Inbound | SSH 22 | None in baseline | Prefer SSM |

The Flask/LLM bridge is intended to communicate with Splunk internally rather than exposing its application port to the Internet.

## `SG-ATTACKER`

The attack host does not need a public inbound management port in the base design.

| Direction | Baseline | Reason |
|---|---|---|
| Inbound | No unnecessary inbound rules | Use SSM for administration |
| Outbound | DNS and web traffic required by the scenario, plus management/update access | Keep the attack path explicit |

## Later scenario controls

DNS/victim security groups are added when those systems are actually deployed. The architecture principle is already fixed: DNS port 53 must never become an Internet-facing open recursive resolver, and victim access should be source-specific rather than `0.0.0.0/0`.

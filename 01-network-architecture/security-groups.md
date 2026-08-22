# Security Group Design

Security Groups are the primary service-level network control. Ports are added only for real service paths.

## `SG-WEB`

| Direction | Protocol / Port | Source / Destination | Reason |
|---|---|---|---|
| Inbound | TCP 80 | `0.0.0.0/0` | Public HTTP / redirect path |
| Inbound | TCP 443 | `0.0.0.0/0` | Public HTTPS target |
| Inbound | SSH 22 | None | Administration uses SSM |

## `SG-SPLUNK`

| Direction | Protocol / Port | Source | Reason |
|---|---|---|---|
| Inbound | TCP 8000 | Approved team public IPs only | Splunk Web |
| Inbound | TCP 9997 | `SG-WEB`, `SG-DNS`, `SG-VICTIM`, `SG-SINKHOLE` | Private Universal Forwarder receiver |
| Inbound | TCP 8088 | No public rule | HEC is internal-only for the AI bridge |
| Inbound | TCP 8089 | No public rule | Splunk management interface |
| Inbound | SSH 22 | None | SSM administration |

`SG-VICTIM -> 9997` is reserved for a future victim forwarder path. No victim UF was installed during the Scenario 02 infrastructure build.

## `SG-ATTACKER`

No unnecessary public inbound management rule. The attack host uses SSM and scenario-required outbound paths.

## `SG-DNS`

| Direction | Protocol / Port | Source | Reason |
|---|---|---|---|
| Inbound | UDP 53 | `SG-VICTIM` | Victim DNS queries |
| Inbound | TCP 53 | `SG-VICTIM` | TCP DNS fallback/queries |

There is no `0.0.0.0/0` DNS rule. The resolver is not an Internet-facing recursive resolver.

## `SG-VICTIM`

No inbound application service is required for Scenario 02.

The victim uses outbound DNS to `10.50.30.10`, private HTTP to the sinkhole during validation/response, VPC-local Splunk receiver access only if a forwarder is later enabled, and NAT egress where management/package access requires it.

## `SG-SINKHOLE`

| Direction | Protocol / Port | Source | Reason |
|---|---|---|---|
| Inbound | TCP 80 | `SG-VICTIM` | Private RPZ containment HTTP evidence |

The sinkhole has no public IP and no public inbound service.

## Security rule

The Scenario 02 defender DNS design relies on private addressing, SG-to-SG rules and SSM. A victim host-firewall rule to prevent deliberate direct AWS DNS bypass was discussed during planning but was **not implemented**, so it is not part of the deployed control set.

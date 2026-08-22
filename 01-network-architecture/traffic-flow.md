# Traffic Flow

The lab has separate paths for public DNS, public scenario activity, SOC administration, Web telemetry, AWS telemetry, the completed defender-controlled DNS path and the shared AI bridge.

## Public DNS resolution path

```mermaid
sequenceDiagram
    participant C as Public Client / Resolver
    participant P as Route 53 Parent Zone
    participant D as Route 53 Child Zone
    participant W as dns-soc-web01

    C->>P: Query / delegation lookup for soclab.abdul4rehman215.tech
    P-->>C: NS referral to child Route 53 nameservers
    C->>D: Query soclab A / TXT / NS or www CNAME
    D-->>C: Authoritative DNS response
    C->>W: Optional HTTP / HTTPS follow-up
```

## Scenario 01 public path

```text
dns-attack01 -> Internet -> Route 53 child authority -> optional public Web follow-up
                                                    -> Nginx UF -> Splunk
```

No attacker-to-SOC private route exists.

## Team management path

```text
Team browser -> Internet -> Splunk Web :8000
                         -> approved team sources only

Team admin   -> AWS Systems Manager -> EC2
             -> no public SSH required
```

## Web telemetry path

```text
dns-soc-web01
   -> Splunk Universal Forwarder
   -> VPC-local TCP 9997
   -> dns-soc-splunk01
   -> index=dns_soc_web
```

## AWS telemetry paths

```text
Route 53 public query logs -> CloudWatch -> Kinesis -> Splunk
VPC Flow Logs              -> S3 -> SQS -> Splunk
CloudTrail                 -> S3 -> SQS -> Splunk
AWS Resolver Query Logs    -> S3 -> SQS -> Splunk
                                              |
                                              v
                                      index=dns_soc_aws
```

Public authoritative DNS logs and AWS VPC Resolver Query Logs are different visibility points and are not expected to contain identical events.

## Completed Scenario 02 normal DNS path

```mermaid
sequenceDiagram
    participant V as dns-soc-victim01 / 10.50.30.20
    participant R as dns-soc-resolver01 / Unbound / 10.50.30.10
    participant A as AWS VPC Resolver / 10.50.0.2
    participant D as DNS authority

    V->>R: DNS query UDP/TCP 53
    R->>A: Forward normal DNS
    A->>D: Resolve authoritative data
    D-->>A: Answer / NXDOMAIN
    A-->>R: Result
    R-->>V: Result
```

Normal victim applications use the Ubuntu local stub (`127.0.0.53`), whose validated upstream is `10.50.30.10`.

## Resolver telemetry path

```text
Unbound
  -> syslog
  -> rsyslog filter
  -> /var/log/dns-soc/unbound.log
  -> Resolver UF
  -> 10.50.20.10:9997
  -> index=dns_soc_dns / sourcetype=unbound:dns
```

## RPZ/sinkhole response path

Safe default:

```text
victim query -> Unbound RPZ match -> match logged -> enforcement disabled -> normal upstream result
```

Controlled response when deliberately enabled:

```text
victim query
    -> Unbound RPZ
    -> A 10.50.30.30
    -> dns-soc-sinkhole01:80
    -> Nginx access log
    -> Sinkhole UF
    -> index=dns_soc_web / sourcetype=nginx:access
```

The infrastructure test proved this once and then restored disabled enforcement. Future scenario containment still requires a human decision.

## Monitoring-subnet egress

```text
dns-soc-resolver01 / victim / sinkhole
    -> SOC-PRIVATE-RT 0.0.0.0/0
    -> SOC-MONITORING-NAT in SOC-TARGET-SUBNET
    -> SOC-LAB-IGW
    -> Internet
```

This path supports package/management egress and does not make the three hosts public.

## Shared AI path

```text
Splunk scheduled alert
    -> internal webhook
    -> dns-soc-ai-bridge
    -> OpenAI Responses API
    -> internal HTTPS HEC
    -> index=dns_soc_ai
    -> human SOC validation
```

AI output is advisory; raw telemetry remains the evidence source.

## Scenario 03 and 04 reuse

Scenario 03 and 04 reuse the Scenario 02 victim/resolver/sinkhole path. They do not introduce a new VPC or attacker-to-SOC private route.

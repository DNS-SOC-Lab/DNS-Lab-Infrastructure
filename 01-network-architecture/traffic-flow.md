# Traffic Flow

The lab has separate paths for public DNS, public scenario activity, SOC administration, Web telemetry, AWS telemetry and later defender-controlled DNS work.

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

The parent zone owns the delegation. The child zone owns the lab A record, the `www` CNAME and the training TXT fixture. Both web hostnames ultimately reach `dns-soc-web01`.

## Scenario 01 public path

```mermaid
sequenceDiagram
    participant A as dns-attack01
    participant I as Internet
    participant P as Route 53 Parent DNS
    participant C as Route 53 Child DNS
    participant W as dns-soc-web01
    participant S as Splunk

    A->>I: Authorized public DNS enumeration
    I->>P: Resolve lab namespace authority
    P-->>I: Refer soclab to child nameservers
    I->>C: Query child DNS records
    C-->>A: DNS responses
    A->>I: Optional HTTPS follow-up
    I->>W: Public web traffic
    W-->>S: Nginx telemetry through UF TCP 9997
```

The attack host reaches the public namespace without a private route into `SOC-LAB-VPC`. This preserves the intended network boundary while still creating useful DNS, web and VPC-flow evidence.

## Team management path

```text
Team browser -> Internet -> Splunk Web :8000
                         -> restricted to approved team source IPs

Team admin   -> AWS Systems Manager -> EC2
             -> no general-purpose public SSH required
```

## Completed Web telemetry path

```mermaid
flowchart LR
    W[dns-soc-web01<br/>10.50.10.10]
    UF[Splunk Universal Forwarder]
    S[dns-soc-splunk01<br/>10.50.20.10]
    I[index=dns_soc_web]

    W --> UF
    UF -->|SOC VPC private route<br/>TCP 9997| S
    S --> I
```

The project monitors the required Nginx files rather than all of `/var/log`. Controlled successful and failed HTTP requests were generated only to validate data onboarding; they are not treated as the Scenario 01 attack simulation.

## Completed AWS telemetry paths

```mermaid
flowchart LR
    R53[Route 53 public query logs] --> CW[CloudWatch Logs]
    CW --> K[Kinesis Data Stream]
    K --> S[Splunk AWS Add-on]

    VF[VPC Flow Logs<br/>SOC + ATTACK VPCs] --> S3A[S3]
    S3A --> QA[SQS]
    QA --> S

    CT[CloudTrail] --> S3B[S3]
    S3B --> QB[SQS]
    QB --> S

    RQ[Route 53 Resolver Query Logs<br/>SOC + ATTACK VPCs] --> S3C[S3]
    S3C --> QC[SQS]
    QC --> S

    S --> IDX[index=dns_soc_aws]
```

The real Splunk sourcetypes are documented in [`../03-splunk-build/06-aws-telemetry-onboarding.md`](../03-splunk-build/06-aws-telemetry-onboarding.md).

## Public authoritative DNS vs VPC Resolver logging

These are different visibility points:

```text
Public Internet query
    -> Route 53 authoritative nameserver
    -> public Route 53 query log

EC2 workload using AWS-provided DNS
    -> VPC Resolver
    -> Resolver Query Log
```

A direct query explicitly sent to a Route 53 authoritative nameserver may bypass the VPC Resolver, so the two log families are not expected to contain identical activity.

## Later defender-controlled DNS path

Scenario 02 introduces a team-controlled resolver inside the monitoring subnet:

```text
dns-soc-victim01
        |
        | DNS :53
        v
dns-soc-resolver01
        |
        +--> upstream DNS
        |
        +--> defender-side query logs -> Splunk
        |
        +--> later sinkhole / block decision
```

That later path is separate from the AWS VPC Resolver Query Logging already enabled during Gate C.

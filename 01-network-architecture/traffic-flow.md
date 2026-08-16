# Traffic Flow

The lab has separate traffic paths for public DNS resolution, public scenario activity, SOC access, log ingestion and later defensive DNS work.

## Public DNS resolution path

```mermaid
sequenceDiagram
    participant C as Public Client / Resolver
    participant P as Route 53 Parent Zone
    participant D as Route 53 Child Zone
    participant W as dns-soc-web01

    C->>P: Query / delegation lookup for soclab.abdul4rehman215.tech
    P-->>C: NS referral to child Route 53 nameservers
    C->>D: Query soclab.abdul4rehman215.tech A
    D-->>C: 100.49.192.164
    C->>W: HTTP / HTTPS to public web target
```

The parent zone owns the delegation. The child zone owns the lab A record.

## Scenario 01 public path

```mermaid
sequenceDiagram
    participant A as Attack Host
    participant I as Internet
    participant P as Route 53 Parent DNS
    participant C as Route 53 Child DNS
    participant W as Web Target
    participant S as Splunk

    A->>I: Authorized DNS enumeration
    I->>P: Resolve lab namespace authority
    P-->>I: Refer soclab to child nameservers
    I->>C: Query child DNS records
    C-->>A: DNS responses
    A->>I: Optional HTTP / HTTPS follow-up
    I->>W: Public web traffic
    W-->>S: Web/server logs via approved ingestion path
```

The attack host reaches the public namespace and web target without a private route to the SOC VPC.

## Team management path

```text
Team browser -> Internet -> Splunk Web :8000
                         -> restricted to team source IPs

Team admin   -> AWS Systems Manager -> EC2
             -> no general-purpose public SSH required
```

## Log path

```mermaid
flowchart LR
    W[Web / Linux Logs] --> UF[Splunk Universal Forwarder]
    UF -->|TCP 9997| S[Splunk Enterprise]
    AWS[AWS Telemetry] -. later onboarding .-> S
    DNS[DNS Telemetry] -. later onboarding .-> S
    S --> D[Search / Dashboard / Detection]
```

## Later defensive DNS path

Later scenarios introduce a team-controlled resolver inside the monitoring subnet. At that stage the victim's DNS path changes from direct upstream resolution to a defender-visible path that can be logged and, after an IR decision, sinkholed or denied.

That later path is documented here as architecture only; its AWS/system implementation is added to the build folders when it exists.

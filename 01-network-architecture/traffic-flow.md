# Traffic Flow

The lab has separate traffic paths for public scenario activity, SOC access, log ingestion and later defensive DNS work.

## Scenario 01 public path

```mermaid
sequenceDiagram
    participant A as Attack Host
    participant I as Internet
    participant R as Route 53 Public DNS
    participant W as Web Target
    participant S as Splunk

    A->>I: DNS enumeration requests
    I->>R: Query lab namespace
    R-->>A: DNS responses
    A->>I: Optional HTTPS follow-up
    I->>W: TCP 443
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
    DNS[DNS Telemetry] -. later scenarios .-> S
    S --> D[Search / Dashboard / Detection]
```

## Later defensive DNS path

Later scenarios introduce a team-controlled resolver inside the monitoring subnet. At that stage the victim's DNS path changes from direct upstream resolution to a defender-visible path that can be logged and, after an IR decision, sinkholed or denied.

That later path is documented here as architecture only; its AWS/system implementation is added to the build folders when it exists.

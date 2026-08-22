<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 02 Aws Build](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# AWS Security Telemetry

**Status:** Implemented and validated  
**Implementation owner:** [_Musfira_](https://github.com/MUSFIRA-ZAFAR) - AWS Telemetry / Cloud Engineering  
**Region:** `us-east-1`  
**Splunk destination index:** `dns_soc_aws`

## Objective

Enable the AWS-side logging needed for DNS and cloud investigation, then hand the data to the supported Splunk AWS Add-on.

The final AWS telemetry families are:

1. Route 53 public authoritative query logs;
2. VPC Flow Logs for both existing VPCs;
3. CloudTrail management events;
4. Route 53 VPC Resolver Query Logs for both existing VPCs.

The AWS build stops at delivery infrastructure. Splunk inputs, sourcetypes and field validation are documented in [`../03-splunk-build/06-aws-telemetry-onboarding.md`](../03-splunk-build/06-aws-telemetry-onboarding.md).

---


## Shared S3 / SQS handoff model

The S3-based collectors use dedicated Standard queues so one telemetry family cannot block another. The queues use a **5-minute visibility timeout** and a DLQ with **maximum receives = 5**.

| Telemetry | S3 notification | Main queue | DLQ |
|---|---|---|---|
| VPC Flow Logs | `dns-soc-vpc-flow-to-sqs` | `dns-soc-vpc-flow-sqs` | `dns-soc-vpc-flow-dlq` |
| CloudTrail | `dns-soc-cloudtrail-to-sqs` | `dns-soc-cloudtrail-sqs` | `dns-soc-cloudtrail-dlq` |
| Resolver Query Logs | `dns-soc-resolver-to-sqs` | `dns-soc-resolver-sqs` | `dns-soc-resolver-dlq` |

Each S3 event notification is prefix-scoped to the relevant log family. Splunk-side processing behavior and the signature-validation correction are documented in [`../03-splunk-build/06-aws-telemetry-onboarding.md`](../03-splunk-build/06-aws-telemetry-onboarding.md).

---

## 1. Route 53 public authoritative query logging

This telemetry records DNS queries that reach the public authoritative hosted zone:

```text
soclab.abdul4rehman215.tech
        |
        v
Route 53 public query logging
        |
        v
CloudWatch Logs
/aws/route53/soclab.abdul4rehman215.tech
        |
        v
Kinesis Data Stream
dns-soc-route53-stream
        |
        v
Splunk AWS Add-on
```

### Query logging configuration

The child hosted zone was connected to the CloudWatch log group `/aws/route53/soclab.abdul4rehman215.tech`.

![Route 53 public query logging configuration](screenshots/security-telemetry/route53-query-logging-config.png)

*The Route 53 configuration links the public child hosted zone to its CloudWatch Logs destination.*

### CloudWatch -> Kinesis

A CloudWatch Logs subscription named `dns-soc-route53-to-kinesis` sends the Route 53 log stream to Kinesis.

![Route 53 CloudWatch subscription](screenshots/security-telemetry/route53-cloudwatch-subscription.png)

*The log group shows an active subscription filter after the Kinesis delivery path was connected.*

The data stream is:

```text
dns-soc-route53-stream
```

The CloudWatch delivery role uses the project inline policy `DNS-SOC-CWL-Kinesis-PutRecord`.

![Route 53 Kinesis stream](screenshots/security-telemetry/route53-kinesis-stream.png)

*The stream is active in `us-east-1` and is the supported handoff point used by the Splunk Kinesis input.*

CloudWatch Logs uses the project delivery role:

```text
DNS-SOC-CWL-to-Kinesis-Role
```

![CloudWatch to Kinesis delivery role](screenshots/security-telemetry/route53-kinesis-delivery-role.png)

*The role exists specifically for the CloudWatch Logs -> Kinesis delivery path.*

The Splunk EC2 role was also given read access to the Kinesis stream through `DNS-SOC-Splunk-Kinesis-Read`.

![Splunk Kinesis read policy](screenshots/security-telemetry/splunk-ec2-kinesis-read-policy.png)

*The `DNS-SOC-EC2-SSM-Role` includes the additional customer policy needed by the Splunk AWS collector.*

### Result

Route 53 public query logs now reach Splunk through:

```text
Route 53 -> CloudWatch Logs -> Kinesis -> Splunk
```

This is authoritative-DNS visibility. It is different from VPC Resolver Query Logging later in this file.

---

## 2. VPC Flow Logs

Flow logging was enabled for **both** project VPCs because both contain workloads that are useful during investigation.

| VPC | Flow log | Traffic | Aggregation | Destination |
|---|---|---|---|---|
| `SOC-LAB-VPC` | `dns-soc-flow-soc` | All | 1 minute | S3 |
| `ATTACK-LAB-VPC` | `dns-soc-flow-attack` | All | 1 minute | S3 |

The AWS default flow-log record format and plain-text file format are used.

### SOC VPC

![SOC VPC Flow Log active](screenshots/security-telemetry/vpc-flow-soc-active.png)

*The SOC flow log is active and delivers all traffic to the shared AWS log bucket.*

### Attacker VPC

![Attack VPC Flow Log active](screenshots/security-telemetry/vpc-flow-attack-active.png)

*The attacker flow log uses the same format and destination, giving network context from the simulation side as well.*

### S3 delivery

The shared bucket is:

```text
dns-soc-aws-logs-388096320287
```

VPC Flow Log objects are written under:

```text
vpc-flow/AWSLogs/388096320287/vpcflowlogs/us-east-1/...
```

![VPC Flow Log files in S3](screenshots/security-telemetry/vpc-flow-s3-delivery.png)

*Multiple compressed flow-log files prove that AWS delivery to S3 is working before Splunk collection is considered.*

### SQS handoff

S3 object-created notifications for the `vpc-flow/` prefix feed:

```text
dns-soc-vpc-flow-sqs
    +-- DLQ: dns-soc-vpc-flow-dlq
```

The Splunk EC2 role has the SQS receive/delete/visibility permissions and S3 `GetObject` access required for that path through the inline policy `DNS-SOC-Splunk-VPC-Flow-Read`.

Final flow:

```text
SOC-LAB-VPC + ATTACK-LAB-VPC
        -> VPC Flow Logs
        -> S3
        -> SQS
        -> Splunk AWS Add-on
```

---

## 3. CloudTrail

The trail is:

```text
dns-soc-cloudtrail
```

Implemented settings:

| Setting | Value |
|---|---|
| Home region | `us-east-1` |
| Multi-region trail | Yes |
| Organization trail | No |
| Management events | Enabled |
| Read events | Enabled |
| Write events | Enabled |
| Data events | Not enabled for this phase |
| Insights | Disabled |
| S3 bucket | `dns-soc-aws-logs-388096320287` |
| Prefix | `cloudtrail` |

![CloudTrail trail logging](screenshots/security-telemetry/cloudtrail-trail-logging.png)

*The trail is in the `Logging` state, uses the shared S3 bucket and records multi-region management activity.*

S3 object-created notifications for the prefix:

```text
cloudtrail/AWSLogs/388096320287/CloudTrail/
```

feed:

```text
dns-soc-cloudtrail-sqs
    +-- DLQ: dns-soc-cloudtrail-dlq
```

The Splunk EC2 role has SQS and S3 read permissions scoped to this collection path through `DNS-SOC-Splunk-CloudTrail-Read`.

Final flow:

```text
CloudTrail -> S3 -> SQS -> Splunk AWS Add-on
```

---

## 4. Route 53 VPC Resolver Query Logging

### Why it was enabled early

The original scenario roadmap introduced defender-side resolver visibility mainly from Scenario 02 onward. The Project Lead later chose to enable **AWS VPC Resolver Query Logging during Gate C** because the current `SOC-LAB-VPC` and `ATTACK-LAB-VPC` already contain active workloads that generate useful DNS queries.

The logging configuration is named `dns-soc-resolver-query-logs` and is associated with both existing VPCs.

This did **not** create:

- `dns-soc-resolver01`;
- `dns-soc-victim01`;
- Route 53 inbound Resolver endpoints;
- Route 53 outbound Resolver endpoints;
- DNS Firewall;
- sinkhole infrastructure.

Those remain later scenario work.

### S3 destination

Resolver Query Logs use the same shared bucket. AWS creates the standard path:

```text
AWSLogs/388096320287/vpcdnsquerylogs/<vpc-id>/YYYY/MM/DD/...
```

No custom prefix was required in the console workflow.

![Resolver Query Log S3 delivery](screenshots/security-telemetry/resolver-query-log-s3-delivery.png)

*Resolver log files are present under the AWS `vpcdnsquerylogs` hierarchy, proving the AWS-side destination is working.*

S3 notifications for:

```text
AWSLogs/388096320287/vpcdnsquerylogs/
```

feed:

```text
dns-soc-resolver-sqs
    +-- DLQ: dns-soc-resolver-dlq
```

The prefix sits above the VPC-ID folder so the same queue can receive Resolver Query Logs from both associated VPCs. The Splunk EC2 role uses `DNS-SOC-Splunk-Resolver-Read` for the required S3/SQS access.

Final flow:

```text
SOC-LAB-VPC + ATTACK-LAB-VPC
        -> AWS VPC Resolver Query Logging
        -> S3
        -> SQS
        -> Splunk AWS Add-on
```

### Important visibility boundary

Public Route 53 query logging and Resolver Query Logging answer different questions:

```text
public query log
    = who queried our public authoritative zone?

resolver query log
    = what DNS did an associated VPC workload ask the AWS VPC Resolver to resolve?
```

A direct DNS query sent explicitly to a public authoritative nameserver may not use the VPC Resolver, so the two datasets are not expected to match one-for-one.

---

## 5. AWS-side completion state

| Telemetry family | AWS source active | Delivery destination ready | Splunk handoff ready |
|---|---|---|---|
| Route 53 public authoritative | Yes | CloudWatch + Kinesis | Yes |
| VPC Flow Logs | Yes - both VPCs | S3 + SQS | Yes |
| CloudTrail | Yes | S3 + SQS | Yes |
| Route 53 Resolver Query Logs | Yes - both VPCs | S3 + SQS | Yes |

The final evidence that these sources are searchable with useful fields belongs to Splunk Gate C and is recorded in [`../03-splunk-build/06-aws-telemetry-onboarding.md`](../03-splunk-build/06-aws-telemetry-onboarding.md).

## Evidence index

- [Route 53 query logging configuration](screenshots/security-telemetry/route53-query-logging-config.png)
- [Route 53 CloudWatch subscription](screenshots/security-telemetry/route53-cloudwatch-subscription.png)
- [Route 53 Kinesis stream](screenshots/security-telemetry/route53-kinesis-stream.png)
- [CloudWatch to Kinesis role](screenshots/security-telemetry/route53-kinesis-delivery-role.png)
- [Splunk Kinesis read policy](screenshots/security-telemetry/splunk-ec2-kinesis-read-policy.png)
- [SOC VPC Flow Log](screenshots/security-telemetry/vpc-flow-soc-active.png)
- [Attack VPC Flow Log](screenshots/security-telemetry/vpc-flow-attack-active.png)
- [VPC Flow Log S3 delivery](screenshots/security-telemetry/vpc-flow-s3-delivery.png)
- [CloudTrail logging](screenshots/security-telemetry/cloudtrail-trail-logging.png)
- [Resolver Query Log S3 delivery](screenshots/security-telemetry/resolver-query-log-s3-delivery.png)

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 02 Aws Build](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

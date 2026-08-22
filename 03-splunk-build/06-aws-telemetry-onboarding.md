<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 03 Splunk Build](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# AWS Telemetry Onboarding in Splunk

**Status:** Gate C complete  
**Splunk onboarding / validation owner:** [_Sonia_](https://github.com/sonia11mansha415) — Detection Engineer  
**AWS source implementation:** [_Musfira_](https://github.com/MUSFIRA-ZAFAR) — AWS Telemetry / Cloud Engineering  
**Splunk Add-on for AWS:** `8.2.1`  
**Destination index:** `dns_soc_aws`

## Objective

Bring the completed AWS logging sources into Splunk, record the sourcetypes that actually arrive, and prove the fields are useful before any Scenario 01 detection is written.

The AWS-side resources are documented in [`../02-aws-build/07-security-telemetry.md`](../02-aws-build/07-security-telemetry.md).

## AWS account configuration

The Splunk Add-on for AWS uses the EC2 instance role already attached to `dns-soc-splunk01`:

```text
DNS-SOC-EC2-SSM-Role
```

The add-on autodiscovers the role, so no long-lived static AWS access key is required in the repository.

The installed add-on version is `8.2.1`.

![Splunk Add-on for AWS installed](screenshots/aws-telemetry/aws-add-on-8.2.1-installed.png)

*The add-on input page records version 8.2.1 before the project inputs were created.*

## Final input set

![Four AWS inputs active](screenshots/aws-telemetry/aws-add-on-four-inputs-active.png)

*All four project inputs are active, use the EC2 IAM role, target `dns_soc_aws` and expose the real sourcetypes used by the running configuration.*

| Input | Collection path | Actual sourcetype |
|---|---|---|
| `route53-public-query-logs` | CloudWatch Logs -> Kinesis -> Splunk | `aws:kinesis` |
| `vpc-flow-logs` | VPC Flow Logs -> S3 -> SQS -> Splunk | `aws:cloudwatchlogs:vpcflow` |
| `cloudtrail-logs` | CloudTrail -> S3 -> SQS -> Splunk | `aws:cloudtrail` |
| `resolver-query-logs` | Resolver Query Logs -> S3 -> SQS -> Splunk Custom Data Type | `aws:s3` |

The project intentionally does **not** rename these AWS sourcetypes just to make them look cleaner. The repository records what the supported input produced.

For the three direct S3 -> SQS inputs, the common settings are:

```text
region                        = us-east-1
Force using DLQ               = enabled
SQS batch size                = 10
Signature Validate All Events = disabled
Private Endpoints             = disabled
```

The signature setting is important because these queues receive **direct S3 event notifications**, not SNS-wrapped messages.

---

## 1. Route 53 public authoritative query logs

### Input

```text
name                    = route53-public-query-logs
input type              = Kinesis
stream                  = dns-soc-route53-stream
record format           = CloudWatchLogs
encoding                = gzip
initial stream position = TRIM_HORIZON
index                   = dns_soc_aws
sourcetype              = aws:kinesis
```

### Validation

A fresh query was generated and the resulting event was searched in `dns_soc_aws`.

![Route 53 data in Splunk](screenshots/aws-telemetry/69-aws-route53-data-in-splunk.png)

*The event shows the real Kinesis sourcetype and a Route 53 raw record containing the query name/type, result, protocol and event time.*

![Route 53 NXDOMAIN sample](screenshots/aws-telemetry/route53-nxdomain-sample.png)

*The supporting sample proves that controlled nonexistent-name queries also produce `NXDOMAIN` result context in the authoritative dataset.*

Validated useful content includes:

- queried name;
- query type;
- result context (`NOERROR`, `NXDOMAIN` when generated);
- event time;
- protocol;
- AWS/source context present in the raw record.

This source answers the public-authority question: **what DNS queries reached our hosted zone?**

---

## 2. VPC Flow Logs

### Input

```text
name        = vpc-flow-logs
input type  = SQS-Based S3
S3 decoder  = VPC Flow Logs
queue       = dns-soc-vpc-flow-sqs
index       = dns_soc_aws
sourcetype  = aws:cloudwatchlogs:vpcflow
```

Both project VPCs are present in the flow data.

### Processing issue and fix

The direct collection design is:

```text
S3 -> SQS -> Splunk
```

The first input attempt had **Signature Validate All Events** enabled. Direct S3 event notifications do not contain the SNS signature fields that this check expects, so Splunk repeatedly received the SQS messages but did not complete/delete them.

The internal log showed:

```text
Invalid signature version None
Unable to verify signature
```

![VPC SQS signature validation error](screenshots/troubleshooting/vpc-sqs-signature-validation-error.png)

The fix was to leave **Signature Validate All Events unchecked** for this direct S3 -> SQS input. No SNS layer was added because the existing S3 -> SQS architecture is valid for the project.

After the change, queued objects were processed successfully.

### Data-quality validation

The final search normalized the available VPC fields into investigation-friendly names:

```spl
index=dns_soc_aws sourcetype="aws:cloudwatchlogs:vpcflow"
| eval source_ip=coalesce(src_ip,src),
       destination_ip=coalesce(dest_ip,dest),
       source_port=src_port,
       destination_port=dest_port,
       flow_start=start_time,
       flow_end=end_time
| table _time source_ip destination_ip source_port destination_port protocol action vpcflow_action packets bytes flow_start flow_end
| head 20
```

![VPC Flow data in Splunk](screenshots/aws-telemetry/70-aws-vpc-flow-data-in-splunk.png)

*Real events show source/destination addresses, ports, protocol, allowed/blocked context, AWS `ACCEPT/REJECT`, packet/byte counts and flow start/end times.*

Both VPCs were also proven separately by their flow-log source IDs before Gate C was closed.

---

## 3. CloudTrail

### Input

```text
name        = cloudtrail-logs
input type  = SQS-Based S3
S3 decoder  = CloudTrail
queue       = dns-soc-cloudtrail-sqs
index       = dns_soc_aws
sourcetype  = aws:cloudtrail
```

### Processing issue and fix

CloudTrail uses the same direct S3 -> SQS architecture, so the first attempt showed the same signature-validation symptom:

```text
This message does not have a valid SNS Signature
Invalid signature version None
Unable to verify signature
```

![CloudTrail SQS signature validation error](screenshots/troubleshooting/cloudtrail-sqs-signature-validation-error.png)

The same correction was applied: **Signature Validate All Events unchecked** for the direct S3 -> SQS input.

### Data-quality validation

```spl
index=dns_soc_aws sourcetype="aws:cloudtrail"
| table _time eventName eventSource sourceIPAddress userIdentity.type userIdentity.arn awsRegion errorCode errorMessage
| head 20
```

![CloudTrail data in Splunk](screenshots/aws-telemetry/71-aws-cloudtrail-data-in-splunk.png)

*Real events expose API name, AWS service, source context, identity type/ARN, region and result/error context.*

![CloudTrail source summary](screenshots/aws-telemetry/cloudtrail-source-summary.png)

*The supporting summary shows the multi-region CloudTrail S3 sources being consumed with the same `aws:cloudtrail` sourcetype.*

The trail is multi-region, so events from AWS services outside `us-east-1` can legitimately appear in the dataset.

---

## 4. Route 53 Resolver Query Logs

### Input

```text
name        = resolver-query-logs
input type  = SQS-Based S3 / Custom Data Type
S3 decoder  = Custom Logs
queue       = dns-soc-resolver-sqs
index       = dns_soc_aws
sourcetype  = aws:s3
```

The signature-validation option was left unchecked from the start because this input also uses direct S3 -> SQS delivery.

### Why `aws:s3` is correct here

The add-on does not provide a dedicated Route 53 Resolver Query Log decoder in this design. The project therefore uses the Custom Data Type path and records the real `aws:s3` sourcetype.

The Resolver events are JSON, so `spath` is used to expose the AWS fields:

```spl
index=dns_soc_aws sourcetype="aws:s3"
| spath
| table _time query_timestamp vpc_id srcaddr srcids.instance query_name query_type rcode answers region
| head 20
```

![Resolver Query Logs in Splunk](screenshots/aws-telemetry/72-aws-resolver-data-in-splunk.png)

*The Resolver events prove query timestamp, VPC ID, originating client address, EC2 instance context, queried name/type, response code and region. Answer data is used only when AWS provides it in the event.*

![Resolver source summary](screenshots/aws-telemetry/resolver-source-summary.png)

*The supporting source view proves the `vpcdnsquerylogs` S3 objects are being indexed as `aws:s3`.*

This source answers a different question from public Route 53 logging: **what DNS did workloads in the associated VPCs ask the AWS VPC Resolver to resolve?**

The data remains in `dns_soc_aws`. The separate `dns_soc_dns` index is now active for the implemented team-controlled Unbound resolver and is documented in [`07-scenario-02-dns-onboarding.md`](07-scenario-02-dns-onboarding.md).

---

## 5. Final Gate C validation

The final combined search classified all four AWS telemetry families without relying on planned names:

```spl
index=dns_soc_aws
| eval telemetry=case(
    sourcetype="aws:kinesis","Route 53 Public Authoritative",
    sourcetype="aws:cloudwatchlogs:vpcflow","VPC Flow Logs",
    sourcetype="aws:cloudtrail","CloudTrail",
    sourcetype="aws:s3" AND like(source,"%vpcdnsquerylogs%"),"Route 53 Resolver Query Logs"
)
| where isnotnull(telemetry)
| stats count min(_time) as first max(_time) as last by telemetry sourcetype
| convert ctime(first) ctime(last)
| sort telemetry
```

![Final AWS data-quality validation](screenshots/aws-telemetry/73-aws-data-quality-validation.png)

*The final view shows real event counts and first/last event times for Route 53 public logging, VPC Flow Logs, CloudTrail and Resolver Query Logs.*

## Gate C result

| Requirement | Result |
|---|---|
| Route 53 public authoritative logs searchable | Passed |
| VPC Flow Logs searchable from both VPCs | Passed |
| CloudTrail management events searchable | Passed |
| Resolver Query Logs searchable | Passed |
| All four families in `index=dns_soc_aws` | Passed |
| Actual sourcetypes recorded | Passed |
| Source-specific useful fields validated | Passed |
| Combined data-quality evidence captured | Passed |

**Gate C is complete.**

The shared AI foundation has since been completed in [`../04-ai-integration/`](../04-ai-integration/). Common infrastructure is complete, and Scenario 01 detection engineering is active in the dedicated Scenario 01 repository.

## Evidence index

- [`aws-add-on-8.2.1-installed.png`](screenshots/aws-telemetry/aws-add-on-8.2.1-installed.png)
- [`aws-add-on-four-inputs-active.png`](screenshots/aws-telemetry/aws-add-on-four-inputs-active.png)
- [`69-aws-route53-data-in-splunk.png`](screenshots/aws-telemetry/69-aws-route53-data-in-splunk.png)
- [`route53-nxdomain-sample.png`](screenshots/aws-telemetry/route53-nxdomain-sample.png)
- [`70-aws-vpc-flow-data-in-splunk.png`](screenshots/aws-telemetry/70-aws-vpc-flow-data-in-splunk.png)
- [`vpc-flow-both-vpcs-summary.png`](screenshots/aws-telemetry/vpc-flow-both-vpcs-summary.png)
- [`71-aws-cloudtrail-data-in-splunk.png`](screenshots/aws-telemetry/71-aws-cloudtrail-data-in-splunk.png)
- [`cloudtrail-source-summary.png`](screenshots/aws-telemetry/cloudtrail-source-summary.png)
- [`72-aws-resolver-data-in-splunk.png`](screenshots/aws-telemetry/72-aws-resolver-data-in-splunk.png)
- [`resolver-source-summary.png`](screenshots/aws-telemetry/resolver-source-summary.png)
- [`73-aws-data-quality-validation.png`](screenshots/aws-telemetry/73-aws-data-quality-validation.png)

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 03 Splunk Build](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

# Splunk Troubleshooting & Lessons

The final platform is stable. This file records only engineering problems that changed how the team built or validated the platform. Repetitive commands and intermediate trial-and-error output are intentionally excluded.

The format is simple:

```text
problem -> evidence -> root cause -> correction -> verification -> lesson
```

## 1. Initial one-off container was not durable enough

**Problem**

The first working Splunk container used `splunk/splunk:latest`, `RestartPolicy=no` and Docker-created anonymous volumes. Splunk itself ran, but the deployment was not reproducible across host/container lifecycle events.

![Initial one-off container state](screenshots/troubleshooting/legacy-container-state.png)

**Correction**

The final platform moved to:

```text
splunk/splunk:10.4.2
Docker Compose
restart: unless-stopped
named external volumes
private host bindings for 8000 / 9997
repository-safe config files
```

**Lesson**

A successful `docker run` is not the same as a durable SIEM platform. Version pinning, persistence, restart behavior and recovery need to exist before real telemetry is trusted.

## 2. Host restart exposed the missing restart policy

After an EC2 stop/start cycle, Docker returned but the original container stayed stopped because its restart policy was `no`. Splunk Web therefore had no listener on TCP `8000`.

The final `unless-stopped` policy was validated with both a normal Compose restart and a Docker daemon restart.

**Lesson**

Recovery behavior should be tested, not assumed from a healthy first boot.

## 3. Splunk CLI checks require the correct container user

Early CLI checks produced permission warnings around Splunk runtime/PID files when run under the wrong container identity.

The reliable health check is:

```bash
docker exec -u splunk dns-soc-splunk \
  /opt/splunk/bin/splunk status
```

**Lesson**

A permission warning from an administrative shell command is not automatically evidence that Splunk data is corrupt. Re-run the check using the account expected by the containerized application before escalating the issue.

## 4. Provisioning restart loop / internal HEC API `401`

**Problem**

During Compose provisioning, Splunk itself started but the container repeatedly exited when the image's provisioning workflow reached an internal HEC API check and received HTTP `401 Unauthorized`.

![Provisioning restart loop evidence](screenshots/troubleshooting/hec-401-provisioning-loop.png)

**Correction**

The team stopped the restart loop, preserved both named volumes and backups, then reconciled the protected bootstrap/admin credential with Splunk's stored admin state. The repository keeps only the safe environment example.

HEC remains **not host-published**. It is now used only through the internal Docker path by the completed shared AI integration.

**Lesson**

Identify the exact failing task before deleting data or rebuilding. Splunk had already reached its management service; the failure was authenticated provisioning rather than disk, RAM or Docker networking.

## 5. Receiver exposure was tightened before final acceptance

TCP `9997` is a forwarder receiver, not a public service. A broad temporary rule was replaced with:

```text
SG-WEB -> SG-SPLUNK TCP 9997
```

Splunk Web TCP `8000` remains limited to approved team source addresses.

**Lesson**

Application health, Docker port publishing and AWS security-group controls all need to agree.

## 6. Index retention was verified explicitly

The project indexes were created before log onboarding, but retention initially reflected a longer default. All five indexes were corrected to the intended 30-day lab policy:

```text
frozenTimePeriodInSecs = 2592000
```

**Lesson**

Index creation is not finished when the names appear. Size and retention should be checked before production-like data arrives.

## 7. Ubuntu 26.04 / KV Store compatibility led to a clean host rebuild

**Problem**

The first Splunk EC2 host was built on Ubuntu 26.04. The platform could run, but the later AWS/Kinesis work exposed an unhealthy legacy KV Store/MongoDB state. Continuing on that host would have made the AWS Add-on checkpoint unreliable.

The original host screenshot is retained only as historical evidence:

![Legacy Ubuntu 26 host preflight](screenshots/troubleshooting/legacy-55-ubuntu26-host-preflight.png)

**Root cause / decision**

The project needed a supported, predictable host foundation for Splunk `10.4.2` and KV Store. Rather than trying to force the old database path to work, the team rebuilt `dns-soc-splunk01` cleanly on **Ubuntu 24.04 LTS**.

The rebuild kept the architecture stable:

```text
same instance role
same private IP: 10.50.20.10
same SG model
same 100 GiB storage target
same Splunk 10.4.2 image
same named-volume / receiver / index design
```

**Verification**

The rebuilt platform passed Gate A again and KV Store reported:

```text
status        : ready
serverVersion : 8.0.26
```

AWS Add-on `8.2.1` was then installed and the EC2 IAM role was successfully autodiscovered.

**Lesson**

When a core state service is unhealthy on an unsupported host combination, a clean supported rebuild can be safer and easier to explain than layering fixes onto an uncertain base.

## 8. Route 53 data initially landed outside the project index

**Problem**

The Route 53 Kinesis input successfully collected data, but the first events were not placed in the intended project index.

**Correction**

The input destination was corrected to:

```text
index=dns_soc_aws
```

Fresh Route 53 events were generated after the change and validated there with the real `aws:kinesis` sourcetype.

**Lesson**

Collection success and data placement are separate checks. An input is not complete until index, source, sourcetype and time behavior are all correct.

## 9. Direct S3 -> SQS inputs failed SNS signature validation

This was the main Gate C ingestion issue for both VPC Flow Logs and CloudTrail.

### What the pipeline showed

AWS delivery was healthy. The queue metrics showed messages being sent and received, while successful deletion remained at zero.

![VPC SQS processing stall](screenshots/troubleshooting/vpc-sqs-processing-stall.png)

*The VPC queue metrics narrow the fault to Splunk-side message processing rather than AWS delivery.*

![CloudTrail SQS processing stall](screenshots/troubleshooting/cloudtrail-sqs-processing-stall.png)

*CloudTrail showed the same receive-without-delete pattern.*

```text
source service -> S3        working
S3 -> SQS                   working
Splunk polling SQS          working
message deletion            not happening
```

The Splunk internal log showed:

```text
Invalid signature version None
Unable to verify signature
```

### VPC Flow evidence

![VPC SQS signature validation error](screenshots/troubleshooting/vpc-sqs-signature-validation-error.png)

### CloudTrail evidence

![CloudTrail SQS signature validation error](screenshots/troubleshooting/cloudtrail-sqs-signature-validation-error.png)

**Root cause**

The project uses direct:

```text
S3 -> SQS -> Splunk
```

The input option **Signature Validate All Events** expected SNS signature fields, but direct S3 notifications do not provide an SNS signature wrapper.

**Correction**

The option was disabled for the direct S3 -> SQS inputs. No SNS layer was added. Resolver Query Logging was created with the setting disabled from the start.

**Verification**

After the change:

- SQS messages were processed successfully;
- VPC Flow Logs appeared as `aws:cloudwatchlogs:vpcflow`;
- CloudTrail appeared as `aws:cloudtrail`;
- final Gate C data-quality searches passed.

**Lesson**

When SQS messages are received but never deleted, check the collector's internal processing log before changing AWS delivery architecture.

## 10. Shared AI HEC path required HTTPS

**Problem**

The scheduled synthetic alert reached the AI bridge and the OpenAI request succeeded, but the bridge failed when returning the result to Splunk:

```text
AI bridge -> Splunk HEC
ConnectionResetError: [Errno 104] Connection reset by peer
```

**Evidence / isolation**

Scheduler logs proved the saved search ran successfully. Bridge logs proved the webhook and OpenAI processing also succeeded. That narrowed the failure to the final HEC hop.

A direct protocol test showed the active HEC listener accepted:

```text
https://dns-soc-splunk:8088/services/collector/event
```

and not the HTTP URL initially configured.

**Correction**

The bridge environment was updated to use internal HTTPS HEC. Because the current Splunk internal certificate is not trusted inside the bridge container, the lab currently uses:

```text
SPLUNK_HEC_VERIFY_TLS=false
```

The traffic is still encrypted on the host-local Docker network; certificate verification remains a future hardening item.

**Verification**

The next scheduled synthetic alert completed the full path and produced structured events in:

```text
index=dns_soc_ai
sourcetype=dns_soc:ai:triage
```

**Lesson**

When a multi-stage integration fails, validate each hop independently. Scheduler success, webhook receipt, OpenAI success and HEC success are separate checks.

## Final outcome

The corrections above did not change the core project design. They improved the implementation until it matched the intended operating model:

```text
supported host
    -> reproducible Compose service
    -> healthy KV Store
    -> named persistence
    -> controlled network exposure
    -> stable restart behavior
    -> validated indexes / retention
    -> trusted Web telemetry
    -> trusted AWS telemetry
```

Only concise, useful engineering evidence is kept in the repository. Historical screenshots are clearly labelled when they no longer represent the current deployed state.

## Scenario 02 — dedicated Unbound log handoff

### Symptom

Real Unbound query/reply events were visible in system logging, but the first rsyslog rule did not create `/var/log/dns-soc/unbound.log`.

### Root cause

The output file ownership did not let the `syslog` writer create/write the file while still allowing the Splunk forwarder to read it.

### Final fix

The file was pre-created with:

```text
owner = syslog
group = splunkfwd
mode  = 0640
```

and the final rsyslog `omfile` action uses the same ownership. This gives a narrow Unbound-only input instead of monitoring all of `/var/log/syslog`.

### Data-quality lesson

Do not declare a source onboarded after only seeing raw events. Scenario 02 validated index, host, source, sourcetype, time, core DNS fields and reply metrics before the resolver dataset was considered ready.

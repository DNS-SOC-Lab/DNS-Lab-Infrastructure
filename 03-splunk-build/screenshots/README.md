<!-- dns-soc-nav:start -->
[🏠 Repository Home](../../README.md) · [📁 03 Splunk Build](../README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Splunk Screenshot Evidence

This folder contains the selected public evidence for the completed Splunk platform and telemetry gates.

The evidence is organized by what it proves rather than by the order screenshots were originally captured.

## Gate A — platform evidence

The current host is Ubuntu 24.04 LTS. The old `55-splunk-host-preflight.png` came from the first Ubuntu 26.04 host, so it has been moved to the troubleshooting section and is no longer presented as current-state evidence.

| # | File | What it proves |
|---|---|---|
| 56 | [`platform/56-docker-engine-compose-validation.png`](platform/56-docker-engine-compose-validation.png) | Docker/Compose runtime validation |
| 57 | [`platform/57-docker-storage-baseline.png`](platform/57-docker-storage-baseline.png) | Docker root and filesystem headroom |
| 58 | [`platform/58-splunk-image-and-compose-ready.png`](platform/58-splunk-image-and-compose-ready.png) | Pinned image, sanitized Compose settings and named volumes |
| 59 | [`platform/59-splunk-container-startup.png`](platform/59-splunk-container-startup.png) | Compose service startup |
| 60 | [`platform/60-splunk-container-health.png`](platform/60-splunk-container-health.png) | Splunk service health and local Web response |
| 61 | [`platform/61-splunk-web-access.png`](platform/61-splunk-web-access.png) | Splunk Web reachable |
| 62 | [`platform/62-sg-splunk-access-control.png`](platform/62-sg-splunk-access-control.png) | Restricted TCP `8000` and SG-to-SG receiver control |
| 63 | [`platform/63-splunk-9997-receiver.png`](platform/63-splunk-9997-receiver.png) | Receiver endpoint available on `10.50.20.10:9997` |
| 64 | [`platform/64-splunk-port-exposure-validation.png`](platform/64-splunk-port-exposure-validation.png) | `8000/9997` published; `8088/8089` not host-published |
| 65 | [`platform/65-splunk-custom-indexes.png`](platform/65-splunk-custom-indexes.png) | Five project indexes and 30-day retention |
| 66 | [`platform/66-splunk-restart-validation.png`](platform/66-splunk-restart-validation.png) | Normal restart returns healthy |
| 66b | [`platform/66b-docker-daemon-restart-recovery.png`](platform/66b-docker-daemon-restart-recovery.png) | Docker daemon restart recovers Splunk |
| 67 | [`platform/67-splunk-persistence-recreate.png`](platform/67-splunk-persistence-recreate.png) | Configuration survives container recreation |
| 68 | [`platform/68-splunk-backup-baseline.png`](platform/68-splunk-backup-baseline.png) | Persistent-volume backup validation |

The current Ubuntu 24.04 / KV Store state is documented in [`../01-platform-deployment.md`](../01-platform-deployment.md) and the rebuild lesson in [`../04-troubleshooting-and-lessons.md`](../04-troubleshooting-and-lessons.md). A current 24.04 host-preflight image is not included; the historical 26.04 screenshot is not relabelled as current evidence.

## Gate B — Web Universal Forwarder evidence

| # | File | What it proves |
|---|---|---|
| 51 | [`web-forwarder/51-splunk-uf-installed.png`](web-forwarder/51-splunk-uf-installed.png) | Universal Forwarder service is installed/running on `dns-soc-web01` |
| 52 | [`web-forwarder/52-web-forwarder-target.png`](web-forwarder/52-web-forwarder-target.png) | Active destination is `10.50.20.10:9997` |
| 53 | [`web-forwarder/53-nginx-logs-in-splunk.png`](web-forwarder/53-nginx-logs-in-splunk.png) | Real Nginx event in `dns_soc_web` with host/source/sourcetype/raw data |
| - | [`web-forwarder/nginx-source-summary.png`](web-forwarder/nginx-source-summary.png) | Nginx source/sourcetype summary |

Screenshot `54` is intentionally not claimed because a separate Linux security source has not been independently validated in the current build record.

## Gate C — AWS telemetry evidence

| # | File | What it proves |
|---|---|---|
| 69 | [`aws-telemetry/69-aws-route53-data-in-splunk.png`](aws-telemetry/69-aws-route53-data-in-splunk.png) | Route 53 public authoritative data in `dns_soc_aws` with `aws:kinesis` |
| 70 | [`aws-telemetry/70-aws-vpc-flow-data-in-splunk.png`](aws-telemetry/70-aws-vpc-flow-data-in-splunk.png) | Flow IPs, ports, protocol, action, packets/bytes and start/end fields |
| 71 | [`aws-telemetry/71-aws-cloudtrail-data-in-splunk.png`](aws-telemetry/71-aws-cloudtrail-data-in-splunk.png) | CloudTrail API, identity, source, region and result/error context |
| 72 | [`aws-telemetry/72-aws-resolver-data-in-splunk.png`](aws-telemetry/72-aws-resolver-data-in-splunk.png) | Resolver query, VPC, client/instance, response code and region fields |
| 73 | [`aws-telemetry/73-aws-data-quality-validation.png`](aws-telemetry/73-aws-data-quality-validation.png) | All four AWS telemetry families have real events and timestamps |

Supporting screenshots:

- [`aws-telemetry/aws-add-on-8.2.1-installed.png`](aws-telemetry/aws-add-on-8.2.1-installed.png) — installed add-on version
- [`aws-telemetry/aws-add-on-four-inputs-active.png`](aws-telemetry/aws-add-on-four-inputs-active.png) — four active project inputs and their real sourcetypes
- [`aws-telemetry/route53-nxdomain-sample.png`](aws-telemetry/route53-nxdomain-sample.png) — controlled `NXDOMAIN` result in Route 53 public logging
- [`aws-telemetry/vpc-flow-both-vpcs-summary.png`](aws-telemetry/vpc-flow-both-vpcs-summary.png) — both VPC Flow Log sources present
- [`aws-telemetry/cloudtrail-source-summary.png`](aws-telemetry/cloudtrail-source-summary.png) — multi-region CloudTrail source summary
- [`aws-telemetry/resolver-source-summary.png`](aws-telemetry/resolver-source-summary.png) — Resolver `vpcdnsquerylogs` S3 source summary

## Troubleshooting evidence

| File | Why it is kept |
|---|---|
| [`troubleshooting/legacy-container-state.png`](troubleshooting/legacy-container-state.png) | Shows why the first one-off container was replaced |
| [`troubleshooting/hec-401-provisioning-loop.png`](troubleshooting/hec-401-provisioning-loop.png) | Captures the provisioning failure behind the restart loop |
| [`troubleshooting/legacy-55-ubuntu26-host-preflight.png`](troubleshooting/legacy-55-ubuntu26-host-preflight.png) | Historical first-host evidence; not current OS proof |
| [`troubleshooting/vpc-sqs-signature-validation-error.png`](troubleshooting/vpc-sqs-signature-validation-error.png) | Direct S3 -> SQS input rejected because SNS signature validation was enabled |
| [`troubleshooting/cloudtrail-sqs-signature-validation-error.png`](troubleshooting/cloudtrail-sqs-signature-validation-error.png) | Same direct S3 -> SQS signature issue on CloudTrail |
| [`troubleshooting/vpc-sqs-processing-stall.png`](troubleshooting/vpc-sqs-processing-stall.png) | SQS metrics show messages received but not deleted before the fix |
| [`troubleshooting/cloudtrail-sqs-processing-stall.png`](troubleshooting/cloudtrail-sqs-processing-stall.png) | CloudTrail queue shows the same processing stall pattern |

The public troubleshooting record stays short and focuses on root cause and fix rather than repetitive intermediate output.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../../README.md) · [📁 03 Splunk Build](../README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

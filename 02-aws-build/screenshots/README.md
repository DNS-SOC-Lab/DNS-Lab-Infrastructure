# AWS Screenshot Evidence

Screenshots in this folder are selected implementation evidence for the AWS build.

- `account-security/` - IAM identities, password policy, administrator group, budget and SSM role evidence
- `network-foundation/` - VPC, subnet, IGW, route-table and security-group evidence
- `ec2-deployment/` - launch configuration, Elastic IP, SSM validation and final Scenario 01 instance inventory
- `route53-domain/` - parent DNS migration, child hosted zone, delegation, authoritative tests, public resolver validation and static child records
- `nginx-https/` - web preflight, Nginx configuration, certificate, redirect, TLS, renewal and web-log validation
- `security-telemetry/` - Route 53 logging, Kinesis handoff, VPC Flow Logs, CloudTrail and Route 53 Resolver Query Log delivery evidence

Primary screenshots are displayed inline in the relevant technical documents so a reader can understand the configuration without opening every image manually.

## Security telemetry evidence

| File | What it proves |
|---|---|
| [`security-telemetry/route53-query-logging-config.png`](security-telemetry/route53-query-logging-config.png) | Public child hosted zone query logging points to the Route 53 CloudWatch log group |
| [`security-telemetry/route53-cloudwatch-subscription.png`](security-telemetry/route53-cloudwatch-subscription.png) | CloudWatch log group has an active subscription after the Kinesis handoff was configured |
| [`security-telemetry/route53-kinesis-stream.png`](security-telemetry/route53-kinesis-stream.png) | `dns-soc-route53-stream` is active |
| [`security-telemetry/route53-kinesis-delivery-role.png`](security-telemetry/route53-kinesis-delivery-role.png) | CloudWatch-to-Kinesis delivery role was created |
| [`security-telemetry/splunk-ec2-kinesis-read-policy.png`](security-telemetry/splunk-ec2-kinesis-read-policy.png) | Splunk EC2 role has the additional Kinesis read permission |
| [`security-telemetry/vpc-flow-soc-active.png`](security-telemetry/vpc-flow-soc-active.png) | `dns-soc-flow-soc` is active |
| [`security-telemetry/vpc-flow-attack-active.png`](security-telemetry/vpc-flow-attack-active.png) | `dns-soc-flow-attack` is active |
| [`security-telemetry/vpc-flow-s3-delivery.png`](security-telemetry/vpc-flow-s3-delivery.png) | Flow log `.log.gz` files are arriving in S3 |
| [`security-telemetry/cloudtrail-trail-logging.png`](security-telemetry/cloudtrail-trail-logging.png) | `dns-soc-cloudtrail` is actively logging |
| [`security-telemetry/resolver-query-log-s3-delivery.png`](security-telemetry/resolver-query-log-s3-delivery.png) | Resolver Query Log files are arriving under the standard `vpcdnsquerylogs` S3 path |

Credential material, MFA QR codes, private keys and raw secrets are intentionally not part of the evidence set.

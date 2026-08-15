# Project Roadmap

The lab is built in checkpoints. A later phase should not hide an unfinished foundation problem.

## Build sequence

| Phase | Work | Status |
|---|---|---|
| 01 | AWS identities, MFA and budget controls | Complete |
| 02 | `SOC-LAB-VPC`, SOC subnets, IGW, routes and baseline security groups | Complete |
| 03 | `ATTACK-LAB-VPC`, attack subnet, IGW, routes and baseline security group | Complete |
| 04 | Launch Scenario 01 EC2 instances | Complete |
| 05 | Route 53 hosted zone and `soclab.abdul4rehman215.tech` delegation | **Next** |
| 06 | Nginx / HTTPS validation | Planned |
| 07 | Splunk Enterprise Docker deployment | Planned |
| 08 | Web/server log forwarding into Splunk | Planned |
| 09 | AWS telemetry: Route 53 / Resolver as applicable, VPC Flow Logs, CloudTrail | Planned |
| 10 | Validate indexes, sourcetypes, timestamps and useful fields | Planned |
| 11 | DNS SOC dashboard / investigation views | Planned |
| 12 | Scenario 01 SPL detection and tuning | Planned |
| 13 | Flask / LLM bridge | Planned |
| 14 | AI summary returned to Splunk | Planned |
| 15 | Prepare attacker tooling and exercise prerequisites | Planned |
| 16 | Execute Scenario 01 and document the complete lifecycle | Planned |

After Scenario 01 is stable, later scenario folders drive their own infrastructure additions instead of rebuilding the entire lab.

## Current checkpoint

AWS account access, the base network and the Scenario 01 EC2 compute layer are established and documented. The next checkpoint is Route 53 and delegation of the lab subdomain before the web-service and Splunk application layers are configured.

# Project Roadmap

The lab is built in checkpoints. A later phase should not hide an unfinished foundation or data-quality problem.

## Build sequence

| Phase | Work | Status |
|---|---|---|
| 01 | AWS identities, MFA and budget controls | Complete |
| 02 | `SOC-LAB-VPC`, SOC subnets, IGW, routes and baseline security groups | Complete |
| 03 | `ATTACK-LAB-VPC`, attack subnet, IGW, routes and baseline security group | Complete |
| 04 | Launch Scenario 01 EC2 instances | Complete |
| 05 | Route 53 parent migration, child delegation and permanent web/recon DNS baseline | Complete |
| 06 | Nginx / HTTPS validation | Complete |
| 07 | Splunk Enterprise Docker Compose platform / Gate A | **Complete** |
| 08 | `dns-soc-web01` Universal Forwarder + Nginx/Linux data-quality validation | **Next** |
| 09 | Enable AWS telemetry: Route 53 public query logging, VPC Flow Logs and CloudTrail | Planned |
| 10 | Bring AWS telemetry into Splunk and validate index / host / source / sourcetype / time / fields | Planned |
| 11 | Build the shared Flask / LLM bridge and validate the common alert-enrichment contract | Planned |
| 12 | Scenario 01 DNS investigation dashboard and baseline | Planned |
| 13 | Scenario 01 reconnaissance SPL detection, tuning and alert evidence contract | Planned |
| 14 | Scenario 01 AI profile and human-validation workflow | Planned |
| 15 | Execute Scenario 01 and document detection → investigation → response → verification | Planned |

After Scenario 01 is stable, later scenario repositories drive their own infrastructure additions instead of rebuilding the common AWS/Splunk foundation.

## Current checkpoint

The shared infrastructure platform is ready through **Splunk Gate A**. AWS networking, public DNS authority, Nginx/HTTPS and the Splunk Enterprise Docker Compose deployment are complete and validated. Splunk uses persistent named volumes, restricted Web access, a private receiver on TCP `9997`, explicit project indexes and tested backup/recreate procedures.

The next checkpoint is **trusted web/server telemetry**:

```text
dns-soc-web01
    |
    | Splunk Universal Forwarder
    | Nginx access/error + selected real Linux security source
    v
10.50.20.10:9997
    |
    v
Splunk data-quality validation
```

Only after the web data is trusted does the project move to AWS telemetry. The shared AI foundation is built after the Web/AWS data-quality gates so it can consume stable alert fields instead of influencing the telemetry or detection design.

## Later scenario expansion rule

- **Scenario 02:** introduce `dns-soc-resolver01`, `dns-soc-victim01` and the reusable defender-side sinkhole capability.
- **Scenario 03:** reuse the common resolver/Splunk/AI platform and add controlled Fast Flux behavior.
- **Scenario 04:** reuse the same platform and include a clear before/after sinkhole or block verification as part of containment.

Scenario-specific SPL, dashboards, attack ground truth, analyst findings and IR evidence belong in the scenario repositories, not in the shared infrastructure build folder.

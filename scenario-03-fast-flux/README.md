# Scenario 03 — Fast Flux DNS

**Status:** Planned  
**MITRE ATT&CK:** T1568.001 — Dynamic Resolution: Fast Flux DNS

## Objective

Use the controlled lab namespace to produce a domain whose answers change across multiple IP addresses with short TTL behavior, then investigate the DNS and network evidence together.

## Planned detection focus

- one hostname returning multiple/changing IP addresses;
- unusually short TTLs;
- answer churn across time windows;
- distinct destination count;
- follow-up network connections to the returned addresses;
- correlation between DNS answers and VPC/network flow evidence.

## Team for Scenario 03

| Role | Member |
|---|---|
| Project Lead / Attack Simulation | Sonia |
| SOC Analyst | Lubaba |
| Detection Engineer | Abdul-Rehman |
| IR / Defender | Musfira |

The scenario should end with evidence showing not only that the DNS answer changed, but whether the monitored client actually attempted connections to the rotating infrastructure.

# Scenario 02 — DGA + High NXDOMAIN Activity

**Status:** Planned  
**MITRE ATT&CK:** T1568.002 — Dynamic Resolution: Domain Generation Algorithms

## Objective

Generate harmless, controlled DNS requests that resemble domain-generation behavior and determine whether the SOC can detect the pattern without treating every NXDOMAIN response as malicious.

## Planned detection focus

- NXDOMAIN ratio over time;
- domain/subdomain length and randomness;
- query volume and distinct-name count;
- repeated client behavior;
- process/client context where endpoint telemetry is available;
- comparison with the normal DNS baseline.

## Team for Scenario 02

| Role | Member |
|---|---|
| Project Lead / Attack Simulation | Musfira |
| SOC Analyst | Sonia |
| Detection Engineer | Lubaba |
| IR / Defender | Abdul-Rehman |

## Planned response learning

This scenario is a natural place to introduce team-controlled DNS containment. If the investigation confirms the simulated behavior, the defender can test a sinkhole/deny decision inside the owned lab namespace and prove the victim's subsequent DNS behavior changes as expected.

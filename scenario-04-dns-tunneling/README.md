# Scenario 04 — DNS Tunneling

**Status:** Planned  
**MITRE ATT&CK:** T1071.004 — Application Layer Protocol: DNS; T1572 where the implemented tunnel behavior fits

## Objective

Generate only harmless, synthetic test data inside DNS labels/queries and determine whether the SOC can identify the pattern using DNS structure, frequency and endpoint/network context.

## Planned detection focus

- long or encoded-looking labels;
- high-entropy/random-looking subdomains;
- unusual TXT/A query behavior;
- query length and frequency;
- repeated parent domain;
- relationship between the client/process and DNS activity;
- network evidence before and after containment.

## Team for Scenario 04

| Role | Member |
|---|---|
| Project Lead / Attack Simulation | Lubaba |
| SOC Analyst | Abdul-Rehman |
| Detection Engineer | Musfira |
| IR / Defender | Sonia |

## Safety boundary

The test data must be synthetic and non-sensitive. The exercise is about detection and response behavior, not moving real data out of the environment.

## Planned response

After human confirmation, the IR/Defender role can isolate the source and/or apply the team-controlled DNS containment method. Splunk should then show the difference between pre-containment and post-containment behavior.

# Scenario 01 — DNS Reconnaissance & Enumeration

**Status:** Planned  
**MITRE ATT&CK:** T1590.002 — Gather Victim Network Information: DNS

## Objective

Generate authorized DNS reconnaissance against the lab namespace and determine whether the SOC can distinguish normal DNS activity from a source enumerating multiple record types in a short period.

## Planned behavior

The simulation focuses on controlled queries such as A, AAAA, MX, NS and TXT records, plus authority/recursion observations where relevant. If the public A record is discovered, the scenario may include a follow-up HTTPS request to the lab web target so the analyst can correlate DNS reconnaissance with web activity.

## Detection hypothesis

A single ordinary lookup should not become a high-confidence alert. Suspicion increases when one source requests several record types and/or many names in a short window, especially when the pattern is followed by interaction with the discovered service.

## Team for Scenario 01

| Role | Member |
|---|---|
| Project Lead / Attack Simulation | Abdul-Rehman |
| SOC Analyst | Musfira |
| Detection Engineer | Sonia |
| IR / Defender | Lubaba |

## Evidence the team should produce

- baseline DNS activity before the simulation;
- exact simulation commands and timestamps kept as ground truth;
- DNS query evidence and source identity;
- Splunk search/detection output;
- alert and AI-assisted summary once integrated;
- SOC conclusion based on raw evidence;
- IR decision and any approved restriction/containment;
- verification showing the response had the intended effect;
- tuning notes and lessons learned.

## Analyst questions

The investigation should be able to answer:

- Who queried the lab and from what public source?
- Which names and record types were requested?
- How many queries occurred and over what time window?
- Was the activity expected or authorized?
- Did the same source interact with the web target afterward?
- Which evidence supports the MITRE mapping and final disposition?

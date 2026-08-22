<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 04 Ai Integration](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Validation, Failure Handling & Operations

**Status:** Complete  
**Implementation owner:** [_Musfira_](https://github.com/MUSFIRA-ZAFAR) — **Shared AI Integration**

The shared bridge was validated with synthetic Splunk alerts before any scenario-specific AI profile was added.

## Validation 1 — strong evidence

Synthetic alert ID:

```text
AI-SYNTH-STRONG-001
```

The supplied evidence included concentrated DNS activity, several record types, NXDOMAIN context and follow-up HTTPS paths.

The resulting Splunk AI event contained the required structured fields, including network/OSI context, observed indicators, framework suggestions, missing evidence, response considerations and confidence.

![Structured AI result in Splunk](screenshots/77-ai-summary-in-splunk.png)

*The result is indexed in `dns_soc_ai`, uses `dns_soc:ai:triage`, and explicitly requires human validation.*

![Security-context detail](screenshots/ai-security-context-detail.png)

*The strong test shows Layer 7 DNS/application context, related network/transport layers, observed indicators, response considerations and an evidence-based summary.*

### Analyst lesson from the strong test

The AI suggested `T1595 — Active Scanning` for the synthetic evidence. The Scenario 01 project design later expects the analyst to evaluate `T1590.002 — Gather Victim Network Information: DNS` against the real detection evidence.

That difference is useful proof of the intended control:

```text
AI framework mapping = suggestion
human analyst + raw evidence = source of truth
```

## Validation 2 — incomplete evidence

Synthetic alert ID:

```text
AI-SYNTH-INCOMPLETE-001
```

Only a queried domain and small query count were supplied.

Observed behavior:

- `confidence = low`;
- Cyber Kill Chain stage = `Uncertain`;
- MITRE technique fields = `Uncertain` in the final comparison;
- the model requested source/client, query-type, response, timing and network/follow-up evidence;
- no unsupported source/process/network facts were invented;
- `human_validation_required = true`.

## Human validation

The strong and incomplete tests were compared side by side. Human review passed because the strong case produced useful context while the weak case reduced confidence and asked for missing evidence instead of forcing a conclusion.

![Final strong-vs-incomplete comparison](screenshots/78-ai-foundation-end-to-end-validation.png)

*The final comparison shows different confidence behavior, OSI context, framework suggestions/uncertainty and the mandatory human-validation flag.*

## Validation 3 — failure handling

A deliberately invalid direct payload contained only:

```text
alert_id
alert_name
```

The bridge returned:

```text
HTTP 400
schema_validation_failed
```

The corresponding Splunk search returned **0 events** for `FAIL-TEST-001`.

This proves malformed input is rejected before normal AI/HEC processing and does not create a bad triage event.

## Troubleshooting lessons that changed the implementation

### `docker exec` heredoc produced no output

The first manual HEC test omitted `-i`, so the Python heredoc never reached the container. Adding `docker exec -i` fixed the test without changing Splunk.

### Webhook allow-list file permission

The default container user could not write `/opt/splunk/etc/system/local/alert_actions.conf`. The file was written as root, then ownership was returned to `splunk:splunk` and permissions restricted.

### Scheduled search succeeded but end-to-end flow did not

Scheduler logs proved the search itself was healthy. This separated scheduler behavior from alert-action/webhook troubleshooting and avoided changing a working schedule unnecessarily.

### HEC connection reset after successful OpenAI processing

Bridge logs showed:

```text
OpenAI processing  -> success
AI result          -> success
HEC delivery       -> Connection reset by peer
```

Protocol testing showed the active HEC listener required HTTPS. Updating `SPLUNK_HEC_URL` from HTTP to HTTPS resolved the delivery failure.

### Internal HEC certificate warning

The current lab uses encrypted HEC with certificate verification disabled because the bridge does not trust the internal/self-signed Splunk certificate. This is an accepted lab setting and a future hardening item, not an application failure.

## Validation 4 — first real scenario consumer: Scenario 01

After the shared AI foundation had passed its synthetic strong/incomplete tests, Scenario 01 became the first real detection consumer to validate the common contract end to end.

The Scenario 01 Detection Engineer first stabilized the human-facing detection and alert evidence. The final scheduled alert then supplied the bridge-compatible result fields:

```text
alert_id
alert_name
scenario
severity
event_time
source
evidence_json
```

A fresh controlled Scenario 01 DNS-reconnaissance validation produced this path:

```text
Route 53 authoritative telemetry
        -> Kinesis
        -> Splunk detection v1.0
        -> scheduled alert
        -> native Webhook
        -> bridge normalization
        -> OpenAI structured response (HTTP 200)
        -> internal HTTPS HEC
        -> index=dns_soc_ai / sourcetype=dns_soc:ai:triage
```

The first webhook attempt reached the bridge but returned HTTP 400 because the Scenario 01 result row did not yet match the shared schema. The correction was made at the scenario evidence-contract boundary rather than by rebuilding the shared bridge or changing the working network path.

The returned event is nested under `alert.*` and `ai.*`, and retains:

```text
human_validation_required = true
```

That validation proves the shared foundation can accept a real scenario alert while preserving the architecture rule:

```text
scenario detection decides when the alert fires
AI receives structured evidence afterward
human analyst remains the source of truth
```

Detailed Scenario 01 detection logic, screenshots, troubleshooting and payload mapping belong in the separate `Scenario-01-DNS-Recon` repository; this shared repository records only the common-platform handoff result.

## Routine health checks

Container state:

```bash
cd /opt/dns-soc-splunk
sudo docker compose ps
```

Bridge logs:

```bash
sudo docker compose logs --tail 100 ai-bridge
```

Recent AI events:

```spl
index=dns_soc_ai sourcetype="dns_soc:ai:triage"
| sort - _time
| head 20
```

The reusable SPL used for foundation testing is stored in [`validation/`](validation/).

## Completion gate

The shared AI foundation is complete because:

```text
OpenAI API access                         PASS
bridge container health                   PASS
Splunk container health                   PASS
native Splunk webhook normalization       PASS
strong-evidence structured output         PASS
incomplete-evidence uncertainty behavior  PASS
internal HTTPS HEC return path            PASS
AI event searchable in dns_soc_ai         PASS
basic invalid-schema failure handling     PASS
human validation                          PASS
```

The common infrastructure build is therefore complete. Scenario-specific AI work now consists only of profile/payload mapping after each detection has stable fields.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 04 Ai Integration](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

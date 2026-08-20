# AI Architecture & Security Boundary

**Status:** Complete  
**Implementation owner:** **Musfira — Shared AI Integration**

## Design goal

Add AI-assisted alert triage without changing the trusted telemetry architecture, creating another EC2 instance, or exposing a new public service.

The bridge runs beside Splunk on the existing `dns-soc-splunk01` host.

```text
dns-soc-splunk01
|
+-- dns-soc-splunk
|   +-- 8000 host-published on 10.50.20.10
|   +-- 9997 host-published on 10.50.20.10
|   +-- 8088 internal HEC
|   +-- 8089 internal management
|
+-- dns-soc-ai-bridge
    +-- 5000 internal only

Both containers -> dns-soc-internal
```

## Network boundary

| Path | Exposure | Decision |
|---|---|---|
| Splunk Web `8000` | Host-published on the existing private-IP binding; AWS SG restricts approved team sources | Existing design retained |
| UF receiver `9997` | Host-published on the existing private-IP binding; source restricted by SG | Existing design retained |
| AI bridge `5000` | Docker-internal only | No host port and no AWS SG rule |
| Splunk HEC `8088` | Docker-internal only | No host port and no AWS SG rule |
| Splunk management `8089` | Container-internal | Not publicly exposed |

The webhook URL is therefore an internal Docker hostname:

```text
http://dns-soc-ai-bridge:5000/splunk-webhook
```

The HEC return path is also internal:

```text
https://dns-soc-splunk:8088/services/collector/event
```

## Secret handling

Real secrets are stored outside the repository in:

```text
/etc/dns-soc-ai/ai.env
```

The implementation uses a dedicated OpenAI project/service account and a dedicated Splunk HEC token. The repository contains only [`configs/ai.env.example`](configs/ai.env.example).

Do not commit:

- OpenAI API keys;
- Splunk HEC tokens;
- the real `/etc/dns-soc-ai/ai.env` file;
- screenshots that reveal a token value;
- private keys or unrelated credentials.

## HEC TLS state

The final bridge uses HTTPS to Splunk HEC. During implementation, HTTP caused a connection reset; protocol testing proved that the active listener expected HTTPS.

Current lab setting:

```text
SPLUNK_HEC_URL=https://dns-soc-splunk:8088/services/collector/event
SPLUNK_HEC_VERIFY_TLS=false
```

This means HEC traffic is encrypted on the host-local Docker network, but the bridge does not validate Splunk's current internal/self-signed certificate.

**Future hardening option:** install/trust the Splunk HEC certificate or its CA in the bridge container and set `SPLUNK_HEC_VERIFY_TLS=true`.

This is recorded as a lab security trade-off, not hidden as a completed certificate-validation control.

## Analyst decision boundary

The bridge is explicitly advisory.

It must not:

- declare an alert definitively true-positive or false-positive;
- invent evidence that is not present;
- authorize containment;
- execute response actions;
- treat MITRE ATT&CK or Cyber Kill Chain suggestions as final classifications.

Every successful AI event contains:

```text
human_validation_required = true
```

Raw Splunk telemetry remains the evidence source. The AI result is an investigation aid layered on top of that evidence.

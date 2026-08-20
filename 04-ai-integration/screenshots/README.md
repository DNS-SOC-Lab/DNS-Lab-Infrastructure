# Shared AI Foundation Evidence

These screenshots document the completed shared AI integration. Secrets and token values are not intentionally exposed.

| # | File | What it proves |
|---|---|---|
| 74 | [`74-ai-bridge-container-health.png`](74-ai-bridge-container-health.png) | `dns-soc-ai-bridge` and `dns-soc-splunk` are healthy; bridge uses `dns-soc-internal`; TCP 5000 is container-only |
| 75 | [`75-ai-hec-input-ready.png`](75-ai-hec-input-ready.png) | Dedicated HEC input is enabled for `dns_soc_ai` / `dns_soc:ai:triage` without showing the token value |
| 76 | [`76-ai-internal-hec-connectivity.png`](76-ai-internal-hec-connectivity.png) | Controlled bridge-to-Splunk HEC event is searchable in the AI index |
| 77 | [`77-ai-summary-in-splunk.png`](77-ai-summary-in-splunk.png) | Real structured AI output returned through HEC with `human_validation_required=true` |
| 78 | [`78-ai-foundation-end-to-end-validation.png`](78-ai-foundation-end-to-end-validation.png) | Final strong-vs-incomplete comparison with confidence/framework behavior and human-validation flag |
| - | [`ai-security-context-detail.png`](ai-security-context-detail.png) | Detailed OSI/protocol/indicator/response context from the strong synthetic test |

The original evidence plan reserved screenshot 76 for a webhook-alert configuration view. A clean standalone copy of that screenshot was not present in the supplied evidence pack, so the repository does not fabricate it. The numbered sequence instead uses the real internal HEC validation screenshot; webhook configuration is documented textually in [`../03-splunk-hec-and-webhook.md`](../03-splunk-hec-and-webhook.md) and proven functionally by the successful scheduled-alert end-to-end path.

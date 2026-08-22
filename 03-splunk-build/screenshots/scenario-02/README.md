# Scenario 02 Splunk Evidence

| File | What it proves |
|---|---|
| `88-resolver-uf-active-forward.png` | Resolver Universal Forwarder has `10.50.20.10:9997` as an active destination |
| `89-resolver-dedicated-log-validation.png` | Real Unbound query/reply events reach `/var/log/dns-soc/unbound.log` |
| `90-resolver-uf-input-config.png` | Resolver UF monitor stanza targets `dns_soc_dns` / `unbound:dns` |
| `91-resolver-events-in-splunk.png` | Real resolver events are searchable in `dns_soc_dns` |
| `92-resolver-field-validation.png` | Persistent core DNS fields extract cleanly |
| `93-resolver-reply-metrics.png` | Reply timing/cache indicator/response size extract cleanly |
| `95-sinkhole-uf-input-config.png` | Sinkhole Nginx access log monitor is configured |
| `96-sinkhole-events-in-splunk.png` | Sinkhole Nginx events are searchable in `dns_soc_web` |
| `98-rpz-safe-match-in-splunk.png` | RPZ match is searchable while policy enforcement is disabled |
| `101-rpz-sinkhole-http-in-splunk.png` | Contained HTTP request from the victim is visible in Splunk |

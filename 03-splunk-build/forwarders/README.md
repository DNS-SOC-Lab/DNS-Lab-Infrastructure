<!-- dns-soc-nav:start -->
[🏠 Repository Home](../../README.md) · [📁 03 Splunk Build](../README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Universal Forwarder Configurations

This folder keeps repository-safe forwarder configuration for systems that have actually been onboarded.

Current hosts:

- [`dns-soc-web01/`](dns-soc-web01/) — public Web Nginx telemetry
- [`dns-soc-resolver01/`](dns-soc-resolver01/) — Scenario 02 Unbound DNS telemetry -> `dns_soc_dns`
- [`dns-soc-sinkhole01/`](dns-soc-sinkhole01/) — Scenario 02 private Nginx sinkhole access telemetry -> `dns_soc_web`

All forwarders use the private Splunk receiver `10.50.20.10:9997`.

No credentials, authentication databases, private keys or forwarder admin passwords are stored here.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../../README.md) · [📁 03 Splunk Build](../README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

<!-- dns-soc-nav:start -->
[🏠 Repository Home](../../README.md) · [📁 01 Network Architecture](../README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Architecture Diagram Sources

The diagrams are maintained as Mermaid source so they stay editable and render directly in GitHub.

- [`base-network.mmd`](base-network.mmd) — permanent AWS network, public DNS foundation and deployed monitoring-subnet hosts
- [`dns-authority-delegation.mmd`](dns-authority-delegation.mmd) — registrar, parent zone, child delegation and static child-record authority chain
- [`scenario-01-traffic-flow.mmd`](scenario-01-traffic-flow.mmd) — DNS reconnaissance and public Web follow-up path
- [`scenario-02-defender-dns.mmd`](scenario-02-defender-dns.mmd) — private victim/resolver/sinkhole, Splunk telemetry and NAT egress
- [`soc-lifecycle.mmd`](soc-lifecycle.mmd) — telemetry-to-response workflow

If a diagram is exported to PNG, visually check clipped labels, overlapping arrows, unreadable text and incorrect routes before publication.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../../README.md) · [📁 01 Network Architecture](../README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

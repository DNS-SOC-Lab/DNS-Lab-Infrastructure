# Architecture Diagram Sources

The diagrams in this repository are maintained as Mermaid source so they stay editable, reviewable and render directly in GitHub.

- [`base-network.mmd`](base-network.mmd) - permanent AWS network and public DNS foundation
- [`dns-authority-delegation.mmd`](dns-authority-delegation.mmd) - registrar, parent zone, child delegation and web target authority chain
- [`scenario-01-traffic-flow.mmd`](scenario-01-traffic-flow.mmd) - DNS reconnaissance, delegated resolution and follow-up web path
- [`soc-lifecycle.mmd`](soc-lifecycle.mmd) - telemetry-to-response workflow

If a diagram is later exported to PNG for a report or portfolio post, the exported image should be visually checked for clipped labels, overlapping arrows, unreadable text and incorrect routes before it is published.

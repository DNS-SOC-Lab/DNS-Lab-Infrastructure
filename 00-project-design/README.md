# Project Design

This folder is the source of truth for the lab's purpose and working model. It explains **what we are building and why** before implementation details are introduced.

| Document | Purpose |
|---|---|
| [`project-scope.md`](project-scope.md) | Objective, boundaries, technology choices and success criteria |
| [`team-roles.md`](team-roles.md) | Four rotating roles and shared responsibilities |
| [`scenario-matrix.md`](scenario-matrix.md) | Side-by-side view of all four DNS scenarios |
| [`project-roadmap.md`](project-roadmap.md) | Build sequence and current progress |
| [`scenario-dns-plan.md`](scenario-dns-plan.md) | Permanent child-zone baseline and later scenario-specific DNS changes |
| [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md) | Future scenario-specific EC2, DNS, security and temporary AWS changes |
| [`scenario-documentation-standard.md`](scenario-documentation-standard.md) | Required 20-part scenario workflow, network/MITRE discipline and dashboard standard |

Detailed VPC, subnet, routing, DNS authority and traffic decisions are kept in [`../01-network-architecture/`](../01-network-architecture/) so the project scope does not become a duplicate architecture manual.

The scenario model remains part of the shared project design, while the implementation and evidence for each scenario are maintained in separate scenario repositories by the team. The shared [`scenario-dns-plan.md`](scenario-dns-plan.md) records which DNS records are permanent and which DNS changes must wait for a later scenario.

The shared AI foundation is complete. Future infrastructure is intentionally **scenario-specific and just-in-time**. [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md) records what still needs to be built for Scenarios 02–04. [`scenario-documentation-standard.md`](scenario-documentation-standard.md) gives all four scenario repositories the same reproducible SOC workflow.

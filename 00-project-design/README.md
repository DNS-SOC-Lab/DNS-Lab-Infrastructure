<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12,19,24&height=135&section=header&text=Project%20Design&fontSize=34&fontColor=ffffff&animation=fadeIn&desc=Scope%20%7C%20Scenarios%20%7C%20Roles%20%7C%20Roadmaps&descSize=15&descAlignY=68" width="100%" alt="Project Design" />

[🏠 Repository Home](../README.md) · **🧭 Project Design** · [🌐 Network Architecture](../01-network-architecture/README.md)

This folder is the **source of truth for what the lab is building and why**. It keeps scope, team model, scenario boundaries and implementation sequencing separate from low-level AWS/Splunk configuration.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

## 📚 Design Documents

| Document | Purpose |
|---|---|
| 🎯 [`project-scope.md`](project-scope.md) | Objective, boundaries, technology choices and success criteria |
| 👥 [`team-roles.md`](team-roles.md) | Four rotating roles and shared responsibilities |
| 🧪 [`scenario-matrix.md`](scenario-matrix.md) | Side-by-side view of all four DNS scenarios |
| 🚦 [`project-roadmap.md`](project-roadmap.md) | Build sequence and current progress |
| 📡 [`scenario-dns-plan.md`](scenario-dns-plan.md) | Permanent child-zone baseline and later scenario-specific DNS changes |
| 🏗️ [`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md) | Implemented Scenario 02 defender-DNS resources and remaining just-in-time Scenario 03–04 changes |
| 📋 [`scenario-documentation-standard.md`](scenario-documentation-standard.md) | Required 20-part scenario workflow, network/MITRE discipline and dashboard standard |

## 🧭 How This Section Fits

```mermaid
flowchart LR
    D[Project Design] --> N[Network Architecture]
    N --> A[AWS Build]
    A --> S[Splunk Build]
    S --> AI[Shared AI]
    D --> R[Separate Scenario Repositories]
```

Detailed VPC, subnet, routing, DNS authority and traffic decisions belong in [`../01-network-architecture/`](../01-network-architecture/) so project scope does not become a duplicate architecture manual.

## 🚦 Current Design State

- The **four-scenario model** remains the shared baseline.
- The **shared AI foundation** is complete.
- The **Scenario 02 defender-DNS infrastructure** is complete.
- Remaining infrastructure is **scenario-specific and just-in-time**.
- Scenario implementation/evidence is maintained in separate scenario repositories.

[`scenario-infrastructure-roadmap.md`](scenario-infrastructure-roadmap.md) records what is already implemented and what still needs to be built for Scenarios 03–04. [`scenario-documentation-standard.md`](scenario-documentation-standard.md) keeps all four scenario repositories reproducible and consistent.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

[🏠 Repository Home](../README.md) · [🌐 Next: Network Architecture](../01-network-architecture/README.md)

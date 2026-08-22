<!-- dns-soc-nav:start -->
[🏠 Repository Home](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Contributing

This is a four-person hands-on SOC lab. Contributions should show real work, not just final screenshots.

## Working style

1. Create a short branch for your task, for example `docs/network-architecture`, `build/aws-ec2`, or `detection/dns-recon`.
2. Keep commits focused and readable.
3. Open a pull request when the work is ready for review.
4. Another team member checks technical accuracy, exposed secrets, broken links, and whether the evidence matches the claim.
5. Merge into `main` after review.

## What to record

For implementation work, capture the command or action, purpose, result, timestamp when useful, and evidence. If something fails, document the real problem and fix instead of hiding it.

## Safety

Never commit passwords, MFA secrets, private keys, `.pem` files, API tokens, access keys, raw `.env` files, or screenshots containing credentials. Attack simulations must stay inside systems and domains the team owns or is explicitly authorized to test.

## Scenario repositories

Scenario work follows the shared [`00-project-design/scenario-documentation-standard.md`](00-project-design/scenario-documentation-standard.md). Keep infrastructure changes in this repository and keep scenario-specific dashboards, SPL, attack ground truth, AI profiles, analyst findings, IR evidence and screenshots in the matching scenario repository.

Scenario infrastructure state is maintained in [`00-project-design/scenario-infrastructure-roadmap.md`](00-project-design/scenario-infrastructure-roadmap.md). Scenario 02 resources are now implemented and documented under `02-aws-build/`; Scenario 03–04 additions should still be documented there only after those resources actually exist.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

<!-- dns-soc-nav:start -->
[🏠 Repository Home](../../../README.md) · [📁 Screenshots](../README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Scenario 02 AWS / Defender-DNS Evidence

Selected screenshots continue the shared infrastructure numbering at `79`.

| File | What it proves |
|---|---|
| `79-scenario02-subnet-az-validation.png` | Existing SOC subnets and the monitoring subnet use the expected AZ placement |
| `80-scenario02-nat-gateway-available.png` | `SOC-MONITORING-NAT` reached `Available` |
| `81-scenario02-private-route-via-nat.png` | `SOC-PRIVATE-RT` sends `0.0.0.0/0` through the monitoring NAT |
| `82-scenario02-security-groups.png` | `SG-DNS`, `SG-VICTIM` and `SG-SINKHOLE` exist in `SOC-LAB-VPC` |
| `83-scenario02-resolver-launch-config.png` | Resolver EC2 launch configuration |
| `84-scenario02-victim-launch-config.png` | Victim EC2 launch configuration |
| `85-scenario02-sinkhole-launch-config.png` | Sinkhole EC2 launch configuration |
| `86-unbound-noerror-nxdomain-validation.png` | Normal and nonexistent DNS names resolve through Unbound with `NOERROR` / `NXDOMAIN` |
| `87-unbound-query-reply-logging.png` | Unbound records real query/reply events from `10.50.30.20` |
| `94-sinkhole-nginx-service.png` | Private Nginx sinkhole service is running and serves the controlled page |
| `97-rpz-precontainment-nxdomain.png` | Controlled RPZ test name remains `NXDOMAIN` before enforcement |
| `99-rpz-controlled-redirect.png` | Controlled RPZ enforcement returns `10.50.30.30` |
| `100-rpz-end-to-end-containment.png` | Victim reaches the sinkhole page by the RPZ-controlled hostname |
| `102-rpz-safe-reset.png` | Test hostname returns to the normal `NXDOMAIN` state after reset |
| `103-rpz-final-safe-config.png` | Final RPZ configuration keeps enforcement disabled |
| `104-scenario02-final-health-resolver.png` | Resolver final service/forwarder health |
| `105-scenario02-final-health-victim.png` | Victim final DNS path health |
| `106-scenario02-final-health-sinkhole.png` | Sinkhole final Nginx/forwarder health |

Repeated troubleshooting captures are intentionally not part of the final evidence set. Useful root causes and fixes are documented in the build record instead.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../../../README.md) · [📁 Screenshots](../README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

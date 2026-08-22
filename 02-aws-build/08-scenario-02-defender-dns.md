<!-- dns-soc-nav:start -->
[🏠 Repository Home](../README.md) · [📁 02 Aws Build](README.md)
<!-- dns-soc-nav:end -->

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

# Scenario 02 Defender DNS Infrastructure

**Status:** Complete  
**Scenario:** DGA + High NXDOMAIN  
**Primary MITRE ATT&CK for the later scenario exercise:** `T1568.002` — Dynamic Resolution: Domain Generation Algorithms

This document records the permanent defender-side DNS expansion built for Scenario 02. It is infrastructure validation only. The Scenario 02 DGA simulation, dashboard, detection engineering, alert, AI profile, SOC investigation and incident-response exercise have **not** been executed yet.

## Objective

Add a private client/resolver/sinkhole path that gives the team its own DNS telemetry and a reusable human-controlled containment mechanism without rebuilding the existing AWS, Splunk or AI platform.

## Final architecture

```text
dns-soc-victim01
10.50.30.20
        |
        | DNS
        v
dns-soc-resolver01
10.50.30.10
        |
        | normal forwarding
        v
AWS VPC Resolver
10.50.0.2
        |
        v
Route 53 / Internet DNS

RPZ containment path when deliberately enabled:

dns-soc-victim01
        |
        v
dns-soc-resolver01 / Unbound RPZ
        |
        | A = 10.50.30.30
        v
dns-soc-sinkhole01
Nginx + access logging
```

All three new hosts are private and remain separate from the Splunk role.

| Host | Private IP | Instance | Security group | Role |
|---|---|---|---|---|
| `dns-soc-resolver01` | `10.50.30.10` | Ubuntu 24.04 / `t3.small` / 20 GiB gp3 | `SG-DNS` | Unbound defender resolver + DNS telemetry |
| `dns-soc-victim01` | `10.50.30.20` | Ubuntu 24.04 / `t3.small` / 20 GiB gp3 | `SG-VICTIM` | Controlled client for later DGA/NXDOMAIN activity |
| `dns-soc-sinkhole01` | `10.50.30.30` | Ubuntu 24.04 / `t3.micro` / 16 GiB gp3 | `SG-SINKHOLE` | Private Nginx containment endpoint |

All three are in `SOC-MONITORING-SUBNET`, have no public IPv4 address and use the existing SSM instance role.

## 1. Private subnet egress

`SOC-MONITORING-SUBNET` needed outbound package/management access while its EC2s remained private.

Created:

```text
SOC-MONITORING-NAT
Connectivity: Public NAT Gateway
Subnet: SOC-TARGET-SUBNET
AZ: us-east-1c
```

![Scenario 02 subnet/AZ validation](screenshots/scenario-02/79-scenario02-subnet-az-validation.png)

*The monitoring, target and SIEM subnets use the expected `us-east-1c` placement used by this build.*

![Monitoring NAT available](screenshots/scenario-02/80-scenario02-nat-gateway-available.png)

*The dedicated monitoring NAT reached `Available` before private hosts depended on it.*

`SOC-PRIVATE-RT` now contains:

```text
10.50.0.0/16 -> local
0.0.0.0/0    -> SOC-MONITORING-NAT
```

`SOC-MONITORING-SUBNET` is explicitly associated with this route table.

![Private route through NAT](screenshots/scenario-02/81-scenario02-private-route-via-nat.png)

*The route table keeps SOC-local routing inside the VPC and sends only default outbound traffic through the NAT.*

The NAT is for package/management egress. Normal DNS forwarding uses the VPC Resolver at `10.50.0.2`.

## 2. Security groups

Created:

- `SG-DNS`
- `SG-VICTIM`
- `SG-SINKHOLE`

![Scenario 02 security groups](screenshots/scenario-02/82-scenario02-security-groups.png)

*The three Scenario 02 security groups exist in `SOC-LAB-VPC` as separate role boundaries.*

Final relevant inbound design:

```text
SG-DNS
  UDP 53 <- SG-VICTIM
  TCP 53 <- SG-VICTIM

SG-VICTIM
  no inbound application rule

SG-SINKHOLE
  TCP 80 <- SG-VICTIM

SG-SPLUNK
  TCP 9997 <- SG-WEB
  TCP 9997 <- SG-DNS
  TCP 9997 <- SG-VICTIM
  TCP 9997 <- SG-SINKHOLE
```

No DNS listener was exposed to `0.0.0.0/0`. The additional `SG-VICTIM -> SG-SPLUNK:9997` allowance reserves a private forwarder path, but a victim Universal Forwarder was **not** installed during this build.

## 3. Private EC2 deployment

The three hosts were launched separately and validated for correct private addressing, subnet, security group, SSM access, healthy EC2 status and NAT egress.

![Resolver launch configuration](screenshots/scenario-02/83-scenario02-resolver-launch-config.png)

![Victim launch configuration](screenshots/scenario-02/84-scenario02-victim-launch-config.png)

![Sinkhole launch configuration](screenshots/scenario-02/85-scenario02-sinkhole-launch-config.png)

This separation is intentional:

- Splunk remains the analysis platform;
- the resolver remains the DNS control/telemetry source;
- the victim remains the client producing observable behavior;
- the sinkhole remains an independent containment/evidence endpoint.

## 4. Unbound resolver

Unbound was installed on `dns-soc-resolver01` and listens on private TCP/UDP `53` at `10.50.30.10`.

The final base resolver behavior is preserved in [`configs/scenario-02/unbound/dns-soc.conf`](configs/scenario-02/unbound/dns-soc.conf):

```text
Victim 10.50.30.20
        |
        v
Unbound 10.50.30.10
        |
        v
AWS VPC Resolver 10.50.0.2
```

Important deployed decisions:

- recursion is allowed from the approved victim and localhost only;
- identity/version are hidden;
- query and reply logging are enabled;
- Unbound uses system logging rather than its own custom file path;
- upstream forwarding is `10.50.0.2`;
- final module chain is `respip iterator` because RPZ support was later added;
- the local Unbound DNSSEC validator was not kept in this forwarding design after it produced trust-anchor `SERVFAIL` behavior during testing.

Normal and nonexistent DNS names were both proven through the resolver:

![Unbound NOERROR and NXDOMAIN validation](screenshots/scenario-02/86-unbound-noerror-nxdomain-validation.png)

*The victim receives a normal `NOERROR` answer for `google.com` and a real `NXDOMAIN` for a nonexistent owned-lab name through `10.50.30.10`.*

The resolver also recorded the real client identity and reply result:

![Unbound query and reply logging](screenshots/scenario-02/87-unbound-query-reply-logging.png)

*Unbound logs show `10.50.30.20` querying through the resolver with both query and reply events.*

## 5. Victim DNS path

The victim was configured persistently so its normal operating-system DNS path uses `10.50.30.10` rather than requiring `dig @10.50.30.10` for every test.

The sanitized Netplan example is stored at [`configs/scenario-02/victim/victim-dns-netplan.example.yaml`](configs/scenario-02/victim/victim-dns-netplan.example.yaml).

The deployed host retains its cloud-init/interface identity. The repository intentionally omits the instance-specific MAC address.

On Ubuntu, normal `dig` output can show `127.0.0.53` because `systemd-resolved` is the local stub. `resolvectl` confirmed that its upstream DNS server is `10.50.30.10`.

A host firewall rule blocking deliberate direct use of AWS DNS was discussed during planning but was **not implemented** in this infrastructure build and is therefore not claimed here.

## 6. Resolver telemetry path

Direct custom Unbound file logging originally ran into Ubuntu permission/AppArmor friction. Rather than weaken the working service, the final path uses the system logging stream and a narrow rsyslog copy:

```text
Unbound
   |
   v
system journal / syslog
   |
   v
rsyslog program filter
   |
   v
/var/log/dns-soc/unbound.log
   |
   v
Splunk Universal Forwarder
   |
   | TCP 9997
   v
dns-soc-splunk01
```

The final rsyslog rule is stored in [`configs/scenario-02/rsyslog/30-unbound-splunk.conf`](configs/scenario-02/rsyslog/30-unbound-splunk.conf).

The file is created as `syslog:splunkfwd` with mode `0640`, allowing rsyslog to write and the forwarder to read without forwarding all of `/var/log/syslog`.

Splunk-side onboarding and field validation are documented in [`../03-splunk-build/07-scenario-02-dns-onboarding.md`](../03-splunk-build/07-scenario-02-dns-onboarding.md).

## 7. Private sinkhole service

Nginx was installed on `dns-soc-sinkhole01`. It serves a deliberately simple private page:

```text
DNS SOC Sinkhole
Controlled request successfully redirected.
```

The repository-safe page is [`configs/scenario-02/sinkhole/index.html`](configs/scenario-02/sinkhole/index.html).

No public IP, public DNS, TLS certificate or simulated malware service is needed. The purpose is to create an independent access log when containment redirects the victim.

![Private sinkhole Nginx service](screenshots/scenario-02/94-sinkhole-nginx-service.png)

*The private Nginx endpoint is active and serves the controlled sinkhole page.*

The direct pre-RPZ network path `10.50.30.20 -> 10.50.30.30:80` was validated first so later failures could be isolated to DNS/RPZ rather than the network path.

## 8. Reusable RPZ policy

Unbound `1.19.2` was validated for RPZ support. The resolver module chain was changed to:

```text
module-config: "respip iterator"
```

The reusable policy is split into:

- [`configs/scenario-02/unbound/dns-soc-rpz.conf`](configs/scenario-02/unbound/dns-soc-rpz.conf)
- [`configs/scenario-02/unbound/dns-soc.rpz`](configs/scenario-02/unbound/dns-soc.rpz)

### Safe validation state

The policy was first loaded with:

```text
rpz-action-override: disabled
```

The controlled test hostname matched the RPZ policy, but its normal DNS result remained `NXDOMAIN`.

![Pre-containment NXDOMAIN](screenshots/scenario-02/97-rpz-precontainment-nxdomain.png)

*Before enforcement, the controlled hostname remains in its normal unresolved state.*

This safe-match event was also recorded in the resolver log and Splunk before any response was changed.

### Controlled redirect

For one validation window only, the safe override was removed and the test policy returned:

```text
rpz-test.soclab.abdul4rehman215.tech -> 10.50.30.30
```

![Controlled RPZ redirect](screenshots/scenario-02/99-rpz-controlled-redirect.png)

*The victim receives `10.50.30.30` from Unbound only after the controlled RPZ action is deliberately enabled.*

The victim then accessed the same hostname by name and reached the Nginx sinkhole:

![End-to-end RPZ containment](screenshots/scenario-02/100-rpz-end-to-end-containment.png)

*The full path `Victim -> Unbound RPZ -> 10.50.30.30 -> Nginx` is proven rather than only showing a changed DNS answer.*

This is infrastructure capability testing. It is **not** the later Scenario 02 incident-response exercise, which still requires a real detection, analyst investigation and human-approved response decision.

## 9. Final safe state

The test redirect was not left active.

`rpz-action-override: disabled` was restored after validation, Unbound configuration passed, the service remained active, and the test hostname returned to `NXDOMAIN` rather than `10.50.30.30`.

![RPZ safe reset](screenshots/scenario-02/102-rpz-safe-reset.png)

![Final safe RPZ configuration](screenshots/scenario-02/103-rpz-final-safe-config.png)

*The reusable RPZ policy stays loaded for future controlled use while enforcement is disabled by default.*

## 10. Final health validation

![Resolver final health](screenshots/scenario-02/104-scenario02-final-health-resolver.png)

![Victim final health](screenshots/scenario-02/105-scenario02-final-health-victim.png)

![Sinkhole final health](screenshots/scenario-02/106-scenario02-final-health-sinkhole.png)

Final state:

```text
Resolver
  Unbound active
  SplunkForwarder active
  10.50.20.10:9997 active forward

Victim
  normal DNS uses 10.50.30.10
  ordinary external DNS resolution works

Sinkhole
  Nginx active
  SplunkForwarder active
  10.50.20.10:9997 active forward

RPZ
  policy loaded
  logging available
  enforcement disabled by default
```

## Troubleshooting lessons retained

Only the lessons that changed the final implementation are kept:

1. **Forwarding resolver DNSSEC behavior:** the default local validator produced trust-anchor failures and `SERVFAIL` while direct queries to `10.50.0.2` were healthy. The working design keeps Unbound as the project forwarding/RPZ control rather than adding a second local validation path.
2. **Direct Unbound custom logfile:** `/var/log/unbound/dns-soc.log` produced permission/AppArmor friction. The stable solution is system logging plus an rsyslog program filter.
3. **Rsyslog output ownership:** the dedicated file initially could not be written. The final `syslog:splunkfwd` ownership lets rsyslog write and UF read with mode `0640`.
4. **Safe RPZ testing:** match logging was proven with enforcement disabled before the controlled redirect was enabled. The final state returns to disabled enforcement.

Repeated error screenshots and command retries are intentionally excluded from the public evidence set.

## Completion checkpoint

```text
Scenario 02 defender DNS infrastructure    COMPLETE
Scenario 02 resolver telemetry             COMPLETE
Scenario 02 reusable RPZ/sinkhole path     COMPLETE
Scenario 02 ML                             NOT STARTED
Scenario 02 detection engineering          NOT STARTED
Scenario 02 exercise / SOC / IR            NOT STARTED
```

The next work belongs in the dedicated Scenario 02 repository: baseline, controlled DGA/high-NXDOMAIN generation, dashboard/hunting, rule-based detection, optional Isolation Forest comparison, alerting, AI-assisted analyst context, human investigation and approved containment verification.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="section divider" />

<!-- dns-soc-footer:start -->
<div align="center">

[🏠 Repository Home](../README.md) · [📁 02 Aws Build](README.md)

<sub>DNSentinel Lab · Controlled DNS security training documentation</sub>

</div>
<!-- dns-soc-footer:end -->

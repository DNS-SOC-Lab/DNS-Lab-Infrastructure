# Scenario 02 Repository-Safe Configurations

These files preserve the working Scenario 02 defender-DNS configuration without credentials, instance-specific MAC addresses or authentication material.

- [`unbound/dns-soc.conf`](unbound/dns-soc.conf) — forwarding resolver and query/reply logging
- [`unbound/dns-soc-rpz.conf`](unbound/dns-soc-rpz.conf) — final safe RPZ configuration with enforcement disabled
- [`unbound/dns-soc.rpz`](unbound/dns-soc.rpz) — controlled test policy data retained for repeatable validation
- [`rsyslog/30-unbound-splunk.conf`](rsyslog/30-unbound-splunk.conf) — Unbound-only log copy for Splunk UF
- [`victim/victim-dns-netplan.example.yaml`](victim/victim-dns-netplan.example.yaml) — sanitized persistent victim DNS example
- [`sinkhole/index.html`](sinkhole/index.html) — controlled private sinkhole page

The deployed EC2 files remain the live source of truth. These copies are documentation artifacts and must not be treated as credential stores.

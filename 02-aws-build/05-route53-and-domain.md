# Route 53 Parent and Child DNS Delegation

**Status:** Implemented and validated  
**Implementation owner:** [_Abdul-Rehman_](https://github.com/abdul4rehman215)  
**AWS service:** Amazon Route 53  
**Registrar:** Hostinger  
**Parent domain:** `abdul4rehman215.tech`  
**Lab namespace:** `soclab.abdul4rehman215.tech`  
**Web target:** `dns-soc-web01` / `100.49.192.164`

## Objective

Publish the SOC lab through a real delegated DNS namespace while preserving the existing parent-domain website and mail records.

The final implementation uses two Route 53 public hosted zones:

```text
Hostinger registrar
        |
        v
Route 53 parent zone
abdul4rehman215.tech
        |
        | NS delegation for soclab
        v
Route 53 child zone
soclab.abdul4rehman215.tech
        |
        | A / www CNAME
        v
100.49.192.164
 dns-soc-web01
```

The architecture design is documented separately in [`../01-network-architecture/dns-authority-and-delegation.md`](../01-network-architecture/dns-authority-and-delegation.md).

## Final DNS authority design

| Layer | Implemented value |
|---|---|
| Registrar | Hostinger |
| Parent authoritative zone | `abdul4rehman215.tech` in Route 53 |
| Parent website A record | `2.57.91.91` |
| Child authoritative zone | `soclab.abdul4rehman215.tech` in Route 53 |
| Child web A record | `100.49.192.164` |
| Child web alias | `www.soclab.abdul4rehman215.tech` CNAME -> `soclab.abdul4rehman215.tech.` |
| Child training TXT | `"DNS SOC Training Lab"` |
| Parent NS TTL | `172800` seconds |
| Parent-to-child delegation TTL | `300` seconds |

### Parent nameservers

```text
ns-1398.awsdns-46.org.
ns-1752.awsdns-27.co.uk.
ns-455.awsdns-56.com.
ns-962.awsdns-56.net.
```

### Child nameservers

```text
ns-1750.awsdns-26.co.uk.
ns-1035.awsdns-01.org.
ns-645.awsdns-16.net.
ns-117.awsdns-14.com.
```

The parent and child nameserver sets are intentionally different because they represent separate authoritative hosted zones.

## Implementation decision

The first design kept the parent DNS outside Route 53 and planned to delegate only `soclab`. During implementation, the available parent DNS editor did not expose the required NS-record workflow for the planned subdomain delegation.

The solution was to migrate the parent authoritative DNS to Route 53 while leaving Hostinger as the registrar. Existing parent DNS records were copied into the Route 53 parent zone, the registrar nameservers were changed to the parent Route 53 nameservers, and the parent zone then delegated `soclab` to the separate child hosted zone.

This preserved the parent services while giving the lab a real parent-to-child authority boundary.

## Parent zone migration

The imported parent hosted zone contained the existing website, mail and supporting DNS records. The initial import also exposed two details that required cleanup before delegation was considered complete.

![Parent zone after import, before fixes](screenshots/route53-domain/parent-zone-import-before-fixes.png)

*The imported Route 53 parent zone preserved the existing record set, but the captured state also exposed malformed MX targets and the temporary 300-second parent NS TTL that were corrected before final validation.*

### Registrar nameservers

After the parent zone was prepared, the domain's registrar nameservers were changed to the four Route 53 parent nameservers.

![Hostinger parent Route 53 nameservers](screenshots/route53-domain/hostinger-parent-nameservers.png)

*The registrar now publishes the four Route 53 parent nameservers for `abdul4rehman215.tech`; Hostinger remains the registrar rather than the authoritative DNS service.*

## Troubleshooting - malformed MX targets

The parent-zone import initially produced MX targets such as:

```text
mx1.hostinger.com.abdul4rehman215.tech.
mx2.hostinger.com.abdul4rehman215.tech.
```

The mail hostnames had been interpreted as relative names and the parent zone name was appended. The MX record was corrected to fully qualified targets:

```text
5 mx1.hostinger.com.
10 mx2.hostinger.com.
```

The final dot is important because it makes the target an absolute DNS name.

After the fix, a direct query to a parent authoritative nameserver returned the correct Hostinger MX targets.

## Parent validation

A combined validation checked the public parent nameservers, existing website, corrected mail records and the `www` CNAME.

![Parent Route 53 migration validation](screenshots/route53-domain/parent-migration-validation.png)

*The parent validation confirms Route 53 authority, the unchanged website destination `2.57.91.91`, corrected Hostinger MX records and the existing `www` CNAME.*

A clean `dig -4 +trace abdul4rehman215.tech` then confirmed that public DNS reaches the Route 53 parent authority and returns the existing website address.

![Parent DNS trace](screenshots/route53-domain/parent-dns-trace.png)

*The trace confirms the parent domain resolves through the Route 53 authoritative nameservers rather than through the previous DNS authority.*

The parent NS TTL was then restored from the temporary migration value of `300` seconds to `172800` seconds.

![Parent NS TTL validation](screenshots/route53-domain/parent-ns-ttl-validation.png)

*The direct authoritative response shows all four parent NS records at the restored 172800-second TTL and includes the authoritative-answer flag.*

## Child hosted zone

Before public delegation, the existing child Route 53 zone contained the three core records needed to prove authority:

- `A` -> `100.49.192.164`;
- Route 53-generated `NS` RRset;
- Route 53-generated `SOA` record.

![Child zone core records](screenshots/route53-domain/child-zone-core-records.png)

*The child zone is prepared independently of the parent and maps the delegated hostname to the Elastic IP of `dns-soc-web01`.*

Before creating the parent delegation, the child authority was queried directly.

![Child authoritative validation](screenshots/route53-domain/child-authority-validation.png)

*Direct SOA and NS queries to a child Route 53 nameserver confirm the child zone is authoritative and returns the expected four child nameservers.*

## Parent-to-child delegation

The parent Route 53 zone contains an NS record for `soclab.abdul4rehman215.tech` pointing to the four child nameservers. The delegation record uses a 300-second TTL during the build and validation stage.

![Parent-to-child NS delegation](screenshots/route53-domain/parent-child-delegation.png)

*The parent zone now contains 13 records, including the `soclab` NS delegation to the separate child Route 53 hosted zone.*

### Direct parent referral test

The parent authoritative server was queried with recursion disabled:

```bash
dig @ns-455.awsdns-56.com soclab.abdul4rehman215.tech NS +norecurse
```

The response returned `NOERROR`, `ANSWER: 0` and `AUTHORITY: 4`. That is the expected referral behavior: the parent does not answer the child zone's records directly; it points the resolver to the child authority.

![Parent referral validation](screenshots/route53-domain/parent-referral-validation.png)

*The authority section contains the four child Route 53 nameservers at the 300-second delegation TTL.*

## Public resolution validation

The child NS RRset was checked through Cloudflare, Google and Quad9. All three public recursive resolvers returned the same four child nameservers.

![Public child NS validation](screenshots/route53-domain/public-child-ns-validation.png)

*Independent recursive resolvers agree on the child authority, confirming that the parent delegation is visible publicly.*

The delegated A record was then checked through the system resolver and the same three public resolvers.

![Public child A validation](screenshots/route53-domain/public-child-a-validation.png)

*All tested resolvers return `100.49.192.164` for `soclab.abdul4rehman215.tech`, proving the delegated name reaches the web Elastic IP through normal public DNS resolution.*

## Full delegation trace

The strongest end-to-end DNS validation was:

```bash
dig -4 +trace soclab.abdul4rehman215.tech
```

![SOC lab delegation trace](screenshots/route53-domain/soclab-delegation-trace.png)

*The trace shows the parent Route 53 zone returning the child NS delegation and a child Route 53 nameserver returning the final A record `100.49.192.164`.*

This proves the authority chain rather than only proving that a recursive resolver has cached the expected answer.

## Final combined validation

A final validation placed the parent and child results side by side.

![Parent and child final DNS validation](screenshots/route53-domain/parent-child-final-validation.png)

*The final view separates the two DNS roles clearly: the parent domain keeps its four parent nameservers and `2.57.91.91` website target, while the child namespace uses four different nameservers and resolves to the SOC web Elastic IP.*

## Parent service sanity check

Because the parent DNS authority moved to Route 53, the existing mail-related DNS was checked again after delegation.

![Parent mail DNS sanity check](screenshots/route53-domain/parent-mail-dns-sanity.png)

*The final check confirms the corrected Hostinger MX records, the SPF TXT record and the DMARC policy remain publicly resolvable through the migrated parent DNS.*

The existing parent website was also opened in a browser after the DNS work and continued to load normally. The DNS migration changed authority, not the existing website destination.

## Final static child-zone preparation

After the parent/child authority chain was fully validated, two permanent records were added to make the public web target and Scenario 01 reconnaissance baseline more useful without changing the delegation design:

| Name | Type | Value | TTL | Purpose |
|---|---|---|---:|---|
| `soclab.abdul4rehman215.tech` | A | `100.49.192.164` | 300 | Existing main web target |
| `soclab.abdul4rehman215.tech` | NS | Four child Route 53 nameservers | 172800 | Existing child authority |
| `soclab.abdul4rehman215.tech` | SOA | Route 53-managed SOA | 900 | Existing child authority metadata |
| `soclab.abdul4rehman215.tech` | TXT | `"DNS SOC Training Lab"` | 300 | Controlled DNS-reconnaissance fixture |
| `www.soclab.abdul4rehman215.tech` | CNAME | `soclab.abdul4rehman215.tech.` | 300 | Secondary public web hostname |

![Final child-zone static records](screenshots/route53-domain/child-zone-final-static-records.png)

*The child hosted zone now has five stable record sets. The new `www` CNAME reuses the same web target, while the TXT record gives Scenario 01 a harmless record that can be discovered during authorized enumeration.*

The new records were validated through Cloudflare together with the existing A and NS data.

![Final child static-record validation](screenshots/route53-domain/child-static-records-validation.png)

*The validation confirms the main A record, the `www` CNAME chain, the final `www` address, the training TXT record and the four child nameservers through public recursive DNS.*

These additions do not change the parent-to-child delegation. They extend only the child zone's permanent application/scenario baseline. The Nginx and TLS phase must therefore support both `soclab.abdul4rehman215.tech` and `www.soclab.abdul4rehman215.tech`.

### Later scenario DNS work

No other permanent Route 53 records are required now. Later scenario changes are intentionally deferred:

- Scenario 02 generates nonexistent DGA-style names so NXDOMAIN behavior can be measured.
- Scenario 03 later creates a temporary controlled `flux.soclab...` A RRset with short TTLs when team-controlled endpoints exist.
- Scenario 04 reuses the implemented Scenario 02 controlled resolver/DNS path for tunneling telemetry instead of a fake static public record.
- Sinkhole behavior remains an internal resolver/incident-response control.

The shared design for those changes is documented in [`../00-project-design/scenario-dns-plan.md`](../00-project-design/scenario-dns-plan.md).

## Validation summary

| Check | Result |
|---|---|
| Registrar points parent to Route 53 | Passed |
| Parent authoritative NS | Passed |
| Existing parent website resolution | Passed |
| Parent MX correction | Passed |
| Parent `www` CNAME | Passed |
| Parent DNS trace | Passed |
| Parent NS TTL restored | Passed |
| Child core A / NS / SOA | Passed |
| Child training TXT | Passed |
| Child `www` CNAME -> main A | Passed |
| Parent-to-child NS delegation | Passed |
| Direct parent referral | Passed |
| Cloudflare child NS / A | Passed |
| Google child NS / A | Passed |
| Quad9 child NS / A | Passed |
| Full child delegation trace | Passed |
| SPF / DMARC / MX sanity | Passed |
| Existing parent website browser check | Passed |

## Result

The Route 53 DNS phase is complete. `abdul4rehman215.tech` is authoritative in the Route 53 parent hosted zone, the existing parent website and mail DNS remain intact, and the parent delegates `soclab.abdul4rehman215.tech` to a separate Route 53 child hosted zone.

The delegated lab hostname resolves publicly to `100.49.192.164`, and `www.soclab.abdul4rehman215.tech` follows a CNAME to the same target. The child zone also contains the permanent `"DNS SOC Training Lab"` TXT fixture for controlled reconnaissance.

The stable public DNS baseline is complete. Nginx/HTTPS, Web telemetry and AWS telemetry have since been completed as separate build phases. Scenario-specific DGA, Fast Flux, tunneling and sinkhole DNS behavior remains deferred to the scenario stages that actually need it; see [`../00-project-design/scenario-infrastructure-roadmap.md`](../00-project-design/scenario-infrastructure-roadmap.md).

## Evidence index

- [Parent zone import before fixes](screenshots/route53-domain/parent-zone-import-before-fixes.png)
- [Hostinger parent nameservers](screenshots/route53-domain/hostinger-parent-nameservers.png)
- [Parent migration validation](screenshots/route53-domain/parent-migration-validation.png)
- [Parent DNS trace](screenshots/route53-domain/parent-dns-trace.png)
- [Parent NS TTL validation](screenshots/route53-domain/parent-ns-ttl-validation.png)
- [Child zone core records](screenshots/route53-domain/child-zone-core-records.png)
- [Child authority validation](screenshots/route53-domain/child-authority-validation.png)
- [Parent-to-child delegation](screenshots/route53-domain/parent-child-delegation.png)
- [Parent referral validation](screenshots/route53-domain/parent-referral-validation.png)
- [Public child NS validation](screenshots/route53-domain/public-child-ns-validation.png)
- [Public child A validation](screenshots/route53-domain/public-child-a-validation.png)
- [Full `soclab` delegation trace](screenshots/route53-domain/soclab-delegation-trace.png)
- [Parent/child final validation](screenshots/route53-domain/parent-child-final-validation.png)
- [Parent mail DNS sanity](screenshots/route53-domain/parent-mail-dns-sanity.png)
- [Final child-zone static records](screenshots/route53-domain/child-zone-final-static-records.png)
- [Final child static-record validation](screenshots/route53-domain/child-static-records-validation.png)

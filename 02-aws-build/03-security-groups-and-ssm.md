# Security Groups and Systems Manager

**Status:** Baseline implemented  
**Implementation owner:** Abdul-Rehman

## Objective

Control service exposure with Security Groups and prepare EC2 administration through AWS Systems Manager so SSH does not need to be opened broadly.

## Security groups created

- `SG-WEB`
- `SG-SPLUNK`
- `SG-ATTACKER`

The rule design is documented in [`../01-network-architecture/security-groups.md`](../01-network-architecture/security-groups.md). Rules are kept service-specific: the public web target is the intentionally exposed service, Splunk Web is restricted to the team, and the attack host does not require a public inbound management port.

## SSM role

`DNS-SOC-EC2-SSM-Role` was created with the permissions required for Systems Manager-managed EC2 access. It will be attached to instances during the EC2 deployment phase.

## Evidence

<details>
<summary>EC2 Systems Manager role</summary>

![SSM role](screenshots/account-security/ec2-ssm-role.png)

</details>

<details>
<summary>Security groups created</summary>

![Security groups](screenshots/network-foundation/security-groups.png)

</details>

The current evidence pack confirms the security groups themselves. Rule-level console screenshots can be added when the first EC2 instances are attached and end-to-end access is validated.

## Result

The account has the baseline SG objects and SSM role required to move into EC2 deployment without opening general-purpose SSH access to the Internet.

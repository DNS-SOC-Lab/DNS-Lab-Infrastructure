# Security Groups and Systems Manager

**Status:** Implemented and validated
**Implementation owner:** Abdul-Rehman

## Objective

Control service exposure with Security Groups and administer EC2 through AWS Systems Manager so general-purpose SSH does not need to be opened to the Internet.

## Security group baseline

The current build uses three project security groups:

- `SG-WEB`
- `SG-SPLUNK`
- `SG-ATTACKER`

![Project security groups](screenshots/network-foundation/security-groups.png)

*The security-group inventory confirms that separate controls exist for the public web target, Splunk/SIEM host and attacker environment.*

The rule design is documented in [`../01-network-architecture/security-groups.md`](../01-network-architecture/security-groups.md). The implementation keeps exposure service-specific: the web target is the intentionally public service, Splunk Web is restricted to approved team access, and the attacker host does not require a public inbound management port.

## Systems Manager role

`DNS-SOC-EC2-SSM-Role` was created for Systems Manager-managed EC2 access.

![EC2 Systems Manager role](screenshots/account-security/ec2-ssm-role.png)

*The instance role provides the AWS-side identity used by the project EC2 systems for SSM administration.*

## Runtime validation

The role is now attached to the Scenario 01 EC2 instances and Session Manager access has been successfully used during host validation. This confirms that normal administration can be performed without opening SSH as the default management path.

Runtime screenshots for the three hosts are kept with the EC2 deployment record:

- [Web SSM validation](screenshots/ec2-deployment/web-ssm-validation.png)
- [Splunk SSM validation](screenshots/ec2-deployment/splunk-ssm-validation.png)
- [Attacker SSM validation](screenshots/ec2-deployment/attacker-ssm-validation.png)

## Result

The security-group baseline and SSM management path are both active. Scenario 01 hosts can be administered through Systems Manager while public service exposure remains controlled by role-specific security groups.

## Evidence index

- [Security groups](screenshots/network-foundation/security-groups.png)
- [EC2 SSM role](screenshots/account-security/ec2-ssm-role.png)
- [EC2 deployment and SSM validation](04-ec2-deployment.md)

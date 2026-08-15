# AWS Account Security and Access

**Status:** Implemented  
**Implementation owner:** Abdul-Rehman  
**Region used for the lab:** `us-east-1`

## Objective

Give each team member accountable AWS access without using the root user for daily work, require stronger authentication, and add basic cost protection before deploying lab infrastructure.

## Team IAM access

Four separate IAM identities were created for the project team instead of sharing one daily-use account. Individual identities preserve accountability and will later allow CloudTrail activity to be traced back to the AWS identity that performed a change.

![IAM project users](screenshots/account-security/iam-project-users.png)

*The IAM user inventory confirms that the project uses separate identities for team access.*

## Administrative permission model

The project administrators are managed through the `DNS-SOC-Admins` group. The group carries the AWS-managed `AdministratorAccess` policy for the lab environment so permissions can be managed centrally instead of attaching the same policy separately to each user.

![DNS-SOC-Admins permissions](screenshots/account-security/dns-soc-admins.png)

*The shared administrator group provides one controlled place to manage the team's lab permissions.*

## Password policy and MFA

A custom IAM password policy was configured for console access. MFA is also part of the project access baseline. MFA QR codes, authentication seeds, temporary passwords, recovery information and other credential material are deliberately excluded from the repository.

![IAM password policy](screenshots/account-security/iam-password-policy.png)

*The account-level password policy establishes the minimum credential requirements used by IAM users.*

## Cost control

A monthly AWS budget was created before compute deployment so the team has an early warning if lab usage starts moving beyond the planned spend.

![AWS monthly budget](screenshots/account-security/monthly-budget.png)

*The budget provides cost visibility while the lab grows through later build and scenario phases.*

## EC2 administration preparation

The `DNS-SOC-EC2-SSM-Role` instance role was created for Systems Manager-based administration. Its implementation and runtime validation are documented in [`03-security-groups-and-ssm.md`](03-security-groups-and-ssm.md) and [`04-ec2-deployment.md`](04-ec2-deployment.md).

## Result

The AWS account now has individual team identities, centralized administrator permissions, MFA-backed access, password controls, cost monitoring and the IAM foundation required for SSM-managed EC2 administration.

## Evidence index

- [IAM project users](screenshots/account-security/iam-project-users.png)
- [IAM password policy](screenshots/account-security/iam-password-policy.png)
- [DNS-SOC-Admins permissions](screenshots/account-security/dns-soc-admins.png)
- [AWS monthly budget](screenshots/account-security/monthly-budget.png)

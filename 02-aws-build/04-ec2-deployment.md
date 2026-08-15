# Scenario 01 EC2 Deployment

**Status:** Implemented and validated
**Implementation owner:** Abdul-Rehman
**Region:** `us-east-1` (N. Virginia)
**Availability Zone observed:** `us-east-1c`

## Objective

Deploy the compute layer required for Scenario 01 on top of the completed VPC, routing, security-group and SSM foundation. The deployment keeps the attacker in a separate VPC while the web target and Splunk host remain inside the SOC VPC.

## Deployment overview

| Instance | Role | OS / AMI shown in deployment evidence | Instance type | Storage | Private IP |
|---|---|---|---|---|---|
| `dns-soc-web01` | Public web target | Canonical Ubuntu 26.04, amd64 | `t3.small` | 30 GiB | `10.50.10.10` |
| `dns-soc-splunk01` | Splunk / SIEM host | Canonical Ubuntu 26.04, amd64 | `t3.xlarge` | 100 GiB | `10.50.20.10` |
| `dns-attack01` | Attack / simulation host | Kali Linux | `t3.small` | 25 GiB | `10.60.10.10` |

All three instances use the project SSM administration model. Termination protection was enabled during the launch configuration captured for the hosts.

## Web target — `dns-soc-web01`

The web target is deployed in the SOC target subnet and will become the public application endpoint used by the lab domain in the next build phase.

Key deployment values:

| Setting | Implemented value |
|---|---|
| VPC | `SOC-LAB-VPC` |
| Subnet | `SOC-TARGET-SUBNET` |
| Private IP | `10.50.10.10` |
| Instance type | `t3.small` |
| Storage | 30 GiB |
| Security group | `SG-WEB` |
| Instance profile | `DNS-SOC-EC2-SSM-Role` |

![Web EC2 launch summary](screenshots/ec2-deployment/web-launch-summary.png)

*The launch capture records the Ubuntu image, `t3.small` sizing, 30 GiB storage, `SG-WEB`, SSM instance profile and termination-protection settings used for the web host.*

### Elastic IP

A dedicated Elastic IP was allocated and associated with the web instance so the public DNS record can later point to a stable address.

![Web Elastic IP](screenshots/ec2-deployment/web-elastic-ip.png)

*The Elastic IP inventory shows the `web-elastic-ip` allocation associated with the web EC2 instance. Public address values are intentionally not repeated in the documentation text.*

### Runtime validation

The host was accessed through Session Manager and checked from the operating system.

Validated from the captured session:

- hostname: `dns-soc-web01`;
- interface address: `10.50.10.10/24`;
- default route through the target subnet gateway;
- system timezone: UTC;
- NTP synchronization active;
- HTTPS connectivity to `aws.amazon.com` returned `HTTP/2 200`;
- DNS resolution for `aws.amazon.com` succeeded.

![Web SSM validation](screenshots/ec2-deployment/web-ssm-validation.png)

*The Session Manager session confirms the planned private address, working routing, synchronized UTC time, DNS resolution and outbound HTTPS connectivity.*

## Splunk SOC — `dns-soc-splunk01`

The Splunk host is deployed in the SIEM subnet with larger compute and storage resources because it will run the central Splunk Enterprise workload for the lab.

| Setting | Implemented value |
|---|---|
| VPC | `SOC-LAB-VPC` |
| Subnet | `SOC-SIEM-SUBNET` |
| Private IP | `10.50.20.10` |
| Instance type | `t3.xlarge` |
| Storage | 100 GiB |
| Security group | `SG-SPLUNK` |
| Administration | AWS Systems Manager |

![Splunk EC2 launch summary](screenshots/ec2-deployment/splunk-launch-summary.png)

*The launch summary records the Ubuntu image, `t3.xlarge` sizing, 100 GiB storage, `SG-SPLUNK`, disabled detailed monitoring, Unlimited CPU credit mode and termination protection.*

### Runtime validation

The Splunk host was also validated through Session Manager.

The captured session confirms:

- hostname: `dns-soc-splunk01`;
- interface address: `10.50.20.10/24`;
- default route through the SIEM subnet gateway;
- UTC timezone with NTP synchronization active;
- outbound HTTPS connectivity to AWS;
- working DNS resolution.

![Splunk SSM validation](screenshots/ec2-deployment/splunk-ssm-validation.png)

*The validation proves the SIEM host is reachable through SSM and has the network and DNS connectivity required before Docker and Splunk are installed.*

## Attack host — `dns-attack01`

The attacker is deployed separately inside `ATTACK-LAB-VPC`. This keeps the simulation source outside the SOC VPC's private address space.

| Setting | Implemented value |
|---|---|
| VPC | `ATTACK-LAB-VPC` |
| Subnet | `ATTACK-PUBLIC-SUBNET` |
| Private IP | `10.60.10.10` |
| OS | Kali Linux |
| Instance type | `t3.small` |
| Storage | 25 GiB |
| Administration | AWS Systems Manager |

![Attacker EC2 launch summary](screenshots/ec2-deployment/attacker-launch-summary.png)

*The launch capture records Kali Linux, `t3.small`, 25 GiB storage, the SSM instance profile and termination protection. The project security-group design for the attacker is maintained separately in the security-group documentation.*

### Runtime validation

The attacker host was validated after launch through its management session.

The captured evidence confirms:

- hostname: `dns-attack01`;
- interface address: `10.60.10.10/24`;
- default route through the attacker subnet gateway;
- UTC system time with NTP synchronization active;
- DNS resolution from the attacker environment.

![Attacker SSM validation](screenshots/ec2-deployment/attacker-ssm-validation.png)

*The attacker is operating from the planned `10.60.10.0/24` subnet rather than from the SOC VPC.*

## Final EC2 inventory

All three Scenario 01 instances reached the `Running` state and the captured EC2 inventory shows `3/3 checks passed` for each host.

![Scenario 01 EC2 inventory](screenshots/ec2-deployment/scenario01-ec2-inventory.png)

*The final inventory confirms the three-instance compute layer is active in `us-east-1c` with the planned instance classes.*

## Validation summary

| Instance | Private IP confirmed | SSM access | Routing / network | DNS | Time sync | EC2 status checks |
|---|---|---|---|---|---|---|
| `dns-soc-web01` | Yes | Passed | Passed | Passed | Passed | `3/3` passed |
| `dns-soc-splunk01` | Yes | Passed | Passed | Passed | Passed | `3/3` passed |
| `dns-attack01` | Yes | Passed | Passed | Passed | Passed | `3/3` passed |

## Result

Scenario 01 now has its required compute foundation: a public-facing web target, a dedicated Splunk/SIEM host and a separate Kali attack host. The instances are running on the planned VPC/subnet layout, use the SSM administration path, and passed the network/DNS/time checks captured during deployment.

The next AWS build step is Route 53 and delegation of `soclab.abdul4rehman215.tech`, followed by the web-service/HTTPS configuration.

## Evidence index

- [Web launch summary](screenshots/ec2-deployment/web-launch-summary.png)
- [Web Elastic IP](screenshots/ec2-deployment/web-elastic-ip.png)
- [Web SSM validation](screenshots/ec2-deployment/web-ssm-validation.png)
- [Splunk launch summary](screenshots/ec2-deployment/splunk-launch-summary.png)
- [Splunk SSM validation](screenshots/ec2-deployment/splunk-ssm-validation.png)
- [Attacker launch summary](screenshots/ec2-deployment/attacker-launch-summary.png)
- [Attacker SSM validation](screenshots/ec2-deployment/attacker-ssm-validation.png)
- [Scenario 01 EC2 inventory](screenshots/ec2-deployment/scenario01-ec2-inventory.png)

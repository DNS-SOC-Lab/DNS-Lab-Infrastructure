# Lessons Learned

This folder records decisions and mistakes that are worth carrying into the next scenario. It should stay practical: what happened, why it mattered, what changed, and whether the fix worked.

## Foundation lessons so far

### Separate design from implementation

The project architecture was documented before EC2 deployment, while the AWS build folder continues to contain only resources that have actually been created. This prevents planned components from being mistaken for completed work.

### Keep the attacker and SOC networks independent

Using non-overlapping VPCs with no peering makes the public attack path explicit and prevents the attack host from reaching SOC private addresses directly.

### Use a private route table for monitoring components

The monitoring subnet does not receive the SOC Internet Gateway default route. Later DNS/victim/defense systems can be introduced without accidentally making the whole monitoring segment public.

### Preserve accountability

Separate IAM identities and MFA give the team individual access while keeping future CloudTrail activity attributable to a specific AWS identity.

New lessons should be added after real troubleshooting or scenario execution, not invented to make the documentation look complete.

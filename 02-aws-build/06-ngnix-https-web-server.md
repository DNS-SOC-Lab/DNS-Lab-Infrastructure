# Nginx HTTPS Web Server

**Implementation Owner:** Musfira

---

## 1. Overview

This phase deploys the public web server for the DNS SOC Security Lab on the AWS EC2 instance `dns-soc-web01`.

The web server uses Nginx to serve the SOC lab landing page and provides HTTPS access using a Let's Encrypt certificate.

### Public Hostnames

- `soclab.abdul4rehman215.tech`
- `www.soclab.abdul4rehman215.tech`

### Web Server

| Parameter | Value |
|---|---|
| EC2 Instance | `dns-soc-web01` |
| Private IP | `10.50.10.10` |
| Elastic IP | `100.49.192.164` |
| Web Server | Nginx |
| HTTP | TCP/80 |
| HTTPS | TCP/443 |
| Document Root | `/var/www/dns-soc-lab` |
| Administration | AWS Systems Manager Session Manager |

---

## 2. Objective

The objectives of this phase are:

1. Install and configure Nginx on the web EC2 instance.
2. Deploy a custom DNS SOC Security Lab landing page.
3. Configure a dedicated Nginx virtual host.
4. Connect the public DNS hostname to the EC2 web server.
5. Enable HTTPS using Let's Encrypt.
6. Redirect HTTP traffic to HTTPS.
7. Validate the TLS certificate and SANs.
8. Verify automatic certificate renewal.
9. Configure site-specific Nginx access and error logs.
10. Generate successful and controlled failed requests for log validation.

---

## 3. Architecture

```text
                         Internet
                            |
                            v
                    Public DNS / Route 53
                            |
              +-------------+-------------+
              |                           |
              v                           v
   soclab.abdul4rehman215.tech     www.soclab.abdul4rehman215.tech
              |                           |
              |                           |
              +-------------+-------------+
                            |
                            v
                    100.49.192.164
                      Elastic IP
                            |
                            v
                     dns-soc-web01
                     10.50.10.10
                            |
                    +-------+-------+
                    |               |
                  :80             :443
                    |               |
                    v               v
                  HTTP            HTTPS
                    |               |
                    +-------+-------+
                            |
                          Nginx
                            |
                            v
                  /var/www/dns-soc-lab
                            |
                            v
                       index.html

```
HTTP traffic is redirected to HTTPS.

4. Pre-Deployment Validation

The EC2 instance was accessed through AWS Systems Manager Session Manager.

The following checks were performed:
```
hostnamectl
cat /etc/os-release
ip -br addr
ip route
timedatectl
df -h /
free -h
sudo ss -lntp
sudo ufw status
systemctl status amazon-ssm-agent --no-pager
curl -s https://checkip.amazonaws.com
```
The checks were used to confirm:

Correct hostname
Operating system
Private IP configuration
Routing
System time
Disk and memory availability
Existing listening ports
UFW status
SSM agent health
Public IP address
Result

The EC2 instance was healthy and reachable through SSM.

UFW was inactive.

The instance was ready for Nginx deployment.

Evidence: [`screenshots/nginx-https/39-web-server-preflight.png`]

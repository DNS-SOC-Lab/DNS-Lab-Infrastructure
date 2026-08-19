# Splunk Screenshot Evidence

This folder contains the selected public evidence for the completed Splunk Gate A build. The original implementation archive contained many more screenshots; only evidence that supports the final platform or a useful troubleshooting lesson is kept here.

## Final Gate A evidence

| # | File | What it proves |
|---|---|---|
| 55 | [`platform/55-splunk-host-preflight.png`](platform/55-splunk-host-preflight.png) | Hostname, Ubuntu version, private IP, CPU, memory, disk and time |
| 56 | [`platform/56-docker-engine-compose-validation.png`](platform/56-docker-engine-compose-validation.png) | Docker/Compose runtime validation and successful container test |
| 57 | [`platform/57-docker-storage-baseline.png`](platform/57-docker-storage-baseline.png) | Docker root, Docker storage consumption and root filesystem headroom |
| 58 | [`platform/58-splunk-image-and-compose-ready.png`](platform/58-splunk-image-and-compose-ready.png) | Pinned image, sanitized Compose settings, named volumes and protected env permissions |
| 59 | [`platform/59-splunk-container-startup.png`](platform/59-splunk-container-startup.png) | Final Compose service started with the pinned Splunk image and healthy state |
| 60 | [`platform/60-splunk-container-health.png`](platform/60-splunk-container-health.png) | Running/healthy status, `splunkd`, local Web response and host resource check |
| 61 | [`platform/61-splunk-web-access.png`](platform/61-splunk-web-access.png) | Splunk Web is reachable and responsive |
| 62 | [`platform/62-sg-splunk-access-control.png`](platform/62-sg-splunk-access-control.png) | TCP `9997` from `SG-WEB` and TCP `8000` limited to four team source rules |
| 63 | [`platform/63-splunk-9997-receiver.png`](platform/63-splunk-9997-receiver.png) | Receiver endpoint accepts a TCP connection on `10.50.20.10:9997` |
| 64 | [`platform/64-splunk-port-exposure-validation.png`](platform/64-splunk-port-exposure-validation.png) | Host publishes `8000` and `9997` on the private interface; `8088/8089` are not host-published |
| 65 | [`platform/65-splunk-custom-indexes.png`](platform/65-splunk-custom-indexes.png) | Five project indexes, approved size caps and 30-day retention (`2592000`) |
| 66 | [`platform/66-splunk-restart-validation.png`](platform/66-splunk-restart-validation.png) | Normal restart returns healthy with `unless-stopped` |
| 66b | [`platform/66b-docker-daemon-restart-recovery.png`](platform/66b-docker-daemon-restart-recovery.png) | Docker daemon restart also recovers the Splunk service |
| 67 | [`platform/67-splunk-persistence-recreate.png`](platform/67-splunk-persistence-recreate.png) | Custom index and receiver configuration survive container recreation |
| 68 | [`platform/68-splunk-backup-baseline.png`](platform/68-splunk-backup-baseline.png) | Both persistent-volume archives validate and Splunk returns healthy |

Screenshots `51–54` remain reserved for the next **Web Universal Forwarder** phase.

## Troubleshooting evidence kept publicly

| File | Why it is useful |
|---|---|
| [`troubleshooting/legacy-container-state.png`](troubleshooting/legacy-container-state.png) | Shows why the original `latest` / `RestartPolicy=no` one-off container was replaced |
| [`troubleshooting/hec-401-provisioning-loop.png`](troubleshooting/hec-401-provisioning-loop.png) | Captures the exact provisioning task that caused the Compose restart loop before final correction |

The public troubleshooting record is intentionally short. Repetitive intermediate checks are not needed to prove the final build.

## Publication / redaction checklist

Before Sonia pushes the repository, review every screenshot one final time.

Redact or crop if present:

- team members' exact public `/32` addresses;
- temporary/public Splunk IPv4 addresses where they are not needed;
- AWS account identifiers when unnecessary to explain the configuration;
- SSM session IDs or personal browser/account information;
- passwords, tokens, API keys, secret values, MFA material or private keys.

The selected `62-sg-splunk-access-control.png` already hides the four team public IP values while preserving the rule count and `SG-WEB` receiver source.

## Raw screenshots intentionally excluded

The following files from the original screenshot archive should **not** be added to the public repository:

| Raw file | Action | Reason |
|---|---|---|
| `1.jpeg` | Do not publish | Historical shell command contains an old Splunk password |
| `2.jpeg` | Do not publish | Historical shell command contains an old Splunk password |
| `3.jpeg` | Keep private/raw only | Browser address/tabs contain personal/environment details and a cleaner Web screenshot is available |
| `4.jpeg` | Keep private/raw only | Useful internal-search check but not required for final Gate A evidence |
| `5.jpeg`, `6.jpeg` | Keep private/raw only | Intermediate backup/permission troubleshooting duplicated by cleaner final evidence |
| `Screenshot 2026-08-18 200014.png` | Keep private/raw only | Failed browser state exposes a public IPv4 and is superseded by the documented root cause/result |
| other repeated `1957xx–2152xx` diagnostic screenshots | Keep private/raw only unless specifically needed later | Intermediate audit/migration checks are summarized in `04-troubleshooting-and-lessons.md` |

Private RFC1918 addresses such as `10.50.20.10`, Docker image digests, container names, index names and normal technical configuration are intentionally retained because they explain the lab architecture.

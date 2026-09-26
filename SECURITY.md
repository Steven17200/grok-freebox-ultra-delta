# Security

This repository contains **procedures and examples only**.

## Never commit

- Freebox `app_token`, session token
- Google `client_secret`, `refresh_token`
- WireGuard `PrivateKey` / raw export
- WAN IP, public keys
- SSH passwords, national ID scans

## WireGuard

Export often has `AllowedIPs = 0.0.0.0/0`. Forbidden on an agent host.
Rewrite with `stacks/freebox/sanitize_wg_conf.py`.

## Exposure

Portainer binds `127.0.0.1:9000`. SSH / Plex / qBit stay LAN or split VPN.

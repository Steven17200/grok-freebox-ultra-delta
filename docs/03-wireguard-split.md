# 03 — WireGuard split

Create the peer in Freebox OS → VPN server → WireGuard. Download `.conf` off git.

Export often has `AllowedIPs = 0.0.0.0/0`. **Forbidden** on an agent host.

```bash
python3 stacks/freebox/sanitize_wg_conf.py \
  --in /secure/raw.conf \
  --out /etc/wireguard/wg0.conf \
  --lan 192.168.1.0/24 \
  --wg 192.168.27.64/27 \
  --extra 212.27.0.0/16 \
  --extra 213.36.0.0/16
```

Adjust prefixes to **your** LAN. Check:

```bash
ip route get 192.168.1.254   # wg0
ip route get 1.1.1.1         # not wg0
```

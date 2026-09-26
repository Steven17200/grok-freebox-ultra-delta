# 08 — VM Linux + Portainer + RAM (Ultra / Delta)

Target: Ubuntu VM on the Freebox hypervisor, typically **2 GiB RAM** + ~8 Gi swap file.
You cannot invent RAM. Cap processes + zram.

## Image

Official Ubuntu Server cloud or netinst ISO on the box disk. No random third-party qcow2.

## Create VM

Freebox OS → Virtual machines, or `POST /api/v8/vm/` (right `vm`).

| Field | Example |
|---|---|
| name | `lab` |
| vcpus | `2` |
| memory | `2048` |
| disk_type | `qcow2` |
| os | `ubuntu` |
| enable_cloudinit | `true` |

No VNC/SSH on the WAN.

## cloud-init

`examples/cloud-init-vm.yml` installs Docker + Portainer CE on `127.0.0.1:9000`.

```bash
ssh -L 9000:127.0.0.1:9000 user@VM_LAN
```

## RAM (2 GiB)

`examples/sysctl-ram.conf` + `examples/docker-mem-limits.env`

- swappiness 25
- zram ~25 %
- swapfile 8G if disk allows
- Docker hard limits (Plex 768m, HA 512m, qBit 256m, Portainer 64m)

If `free -h` available stays under ~200 Mi: stop a stack, do not set swappiness 100.

```bash
free -h && swapon --show && docker stats --no-stream
ss -lnt | grep 9000   # 127.0.0.1:9000 only
```

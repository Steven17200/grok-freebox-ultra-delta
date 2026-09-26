# 09 — Stack média optionnelle (2 GiB VM)

Optional. Do not start every service on 2 GiB at once.

Order if RAM is tight: qBittorrent → Prowlarr → Radarr/Sonarr → Overseerr → Tautulli → Plex last.

## Services

| Service | Port | Role |
|---|---|---|
| Plex | 32400 | library |
| Radarr | 7878 | movies |
| Sonarr | 8989 | series |
| Prowlarr | 9696 | indexer hub |
| Overseerr | 5055 | requests |
| Tautulli | 8181 | Plex stats |
| qBittorrent | 8080 | download |

Bind on the VM. Do **not** publish these ports on the WAN.

## Trackers (qBittorrent)

Public discovery **off**: DHT, PeX, LSD. Does not delete a private tracker the user added.

## Bring up

```bash
cp stacks/media/.env.example stacks/media/.env
docker compose -f stacks/media/docker-compose.yml --env-file stacks/media/.env up -d qbittorrent prowlarr
# add radarr sonarr overseerr tautulli when RAM allows
# Plex: --profile plex
```

## API wiring

```bash
python3 stacks/media/bootstrap_apis.py --out /secure/media-apis.json
```

Writes keys off git. Grok Bot / Chat read that private file. Never paste keys in chat.

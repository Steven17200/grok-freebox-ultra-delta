# 02 — Freebox OS API

Official: https://dev.freebox.fr/sdk/os/login/

Authorize **from the LAN**. Press the box button.

```bash
python3 stacks/freebox/authorize.py --host https://mafreebox.freebox.fr
```

Save `app_token` off git. Session = HMAC-SHA1(app_token, challenge), header `X-Fbx-App-Auth`.

```bash
python3 stacks/freebox/session_probe.py --config /secure/freebox-api.json
```

Rights: Freebox OS → Applications. Useful: `tv`, `pvr`, `explorer`, `vm`, `settings`, `player`.
Missing right = tick the box, do not recreate the app if the token works.

VPN **server** peer: UI Freebox OS / app Free, then sanitize the export (doc 03).

#!/usr/bin/env python3
"""Open a Freebox session. Prints permissions only."""
from __future__ import annotations
import argparse, hashlib, hmac, json, ssl, urllib.request
from pathlib import Path
from urllib.parse import urlparse, urlunparse
CTX = ssl._create_unverified_context()

def call(url, method="GET", body=None):
    headers, data = {}, None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(r, context=CTX, timeout=20) as resp:
        return json.loads(resp.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--host", default="")
    args = p.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8-sig"))
    host = args.host or f"https://{cfg.get('api_domain', 'mafreebox.freebox.fr')}"
    if cfg.get("https_port") and cfg["https_port"] not in (443, 80):
        u = urlparse(host)
        if u.port is None:
            host = urlunparse(u._replace(netloc=f"{u.hostname}:{cfg['https_port']}"))
    base = host.rstrip("/")
    login = call(f"{base}/api/v8/login/")
    if not login.get("success"):
        raise SystemExit(json.dumps({"ok": False, "step": "login"}))
    digest = hmac.new(cfg["app_token"].encode(), login["result"]["challenge"].encode(), hashlib.sha1).hexdigest()
    sess = call(f"{base}/api/v8/login/session/", "POST", {"app_id": cfg["app_id"], "password": digest})
    if not sess.get("success"):
        raise SystemExit(json.dumps({"ok": False, "step": "session"}))
    print(json.dumps({"ok": True, "permissions": (sess.get("result") or {}).get("permissions") or {}}, indent=2))

if __name__ == "__main__":
    main()

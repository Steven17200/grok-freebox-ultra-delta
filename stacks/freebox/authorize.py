#!/usr/bin/env python3
"""LAN Freebox app authorize. Prints JSON. Does not write secrets to disk."""
from __future__ import annotations
import argparse, json, ssl, time, urllib.request
CTX = ssl._create_unverified_context()

def req(url, method="GET", body=None):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"} if body else {})
    with urllib.request.urlopen(r, context=CTX, timeout=20) as resp:
        return json.loads(resp.read().decode())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="https://mafreebox.freebox.fr")
    p.add_argument("--app-id", default="fr.example.grok.home")
    p.add_argument("--app-name", default="Grok Home")
    p.add_argument("--app-version", default="1.0.0")
    p.add_argument("--device-name", default="grok-agent")
    p.add_argument("--timeout", type=int, default=120)
    args = p.parse_args()
    base = args.host.rstrip("/")
    auth = req(f"{base}/api/v8/login/authorize/", "POST", {"app_id": args.app_id, "app_name": args.app_name, "app_version": args.app_version, "device_name": args.device_name})
    if not auth.get("success"):
        raise SystemExit(json.dumps(auth))
    track, token = auth["result"]["track_id"], auth["result"]["app_token"]
    status = "pending"
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        st = req(f"{base}/api/v8/login/authorize/{track}")
        status = (st.get("result") or {}).get("status") or "unknown"
        if status in {"granted", "denied", "timeout"}:
            break
        time.sleep(2)
    print(json.dumps({"status": status, "app_id": args.app_id, "app_token": token if status == "granted" else None, "note": "save app_token off git"}, indent=2))
    if status != "granted":
        raise SystemExit(2)

if __name__ == "__main__":
    main()

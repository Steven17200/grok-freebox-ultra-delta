#!/usr/bin/env python3
"""Collect local *arr / qBit keys and harden qBit. Never prints secrets."""
from __future__ import annotations
import argparse, json, os, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QBIT_PREFS = {"dht": False, "pex": False, "lsd": False, "anonymous_mode": False, "encryption": 1}

def _xml_key(path: Path, tag: str = "ApiKey"):
    if not path.is_file():
        return None
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    node = root.find(tag)
    return node.text.strip() if node is not None and node.text else None

def qbit_login(base, user, password):
    data = urlencode({"username": user, "password": password}).encode()
    req = Request(base.rstrip("/") + "/api/v2/auth/login", data=data, method="POST")
    try:
        with urlopen(req, timeout=10) as resp:
            cookie = resp.headers.get("Set-Cookie") or ""
            if "SID=" in cookie:
                return cookie.split("SID=")[1].split(";")[0]
    except Exception:
        return None
    return None

def qbit_set_prefs(base, sid):
    body = urlencode({"json": json.dumps(QBIT_PREFS)}).encode()
    req = Request(base.rstrip("/") + "/api/v2/app/setPreferences", data=body, method="POST")
    req.add_header("Cookie", f"SID={sid}")
    try:
        with urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config-root", default="")
    p.add_argument("--out", required=True)
    p.add_argument("--qbit-url", default="http://127.0.0.1:8080")
    p.add_argument("--qbit-user", default="admin")
    p.add_argument("--qbit-pass", default="")
    args = p.parse_args()
    root = Path(args.config_root or os.environ.get("CONFIG_ROOT") or "/opt/fbx-lab/config")
    summary = {"ok": True, "services": {}}
    mapping = {
        "radarr": root / "radarr" / "config.xml",
        "sonarr": root / "sonarr" / "config.xml",
        "prowlarr": root / "prowlarr" / "config.xml",
    }
    secret = {}
    for name, path in mapping.items():
        key = _xml_key(path)
        summary["services"][name] = {"api_key_present": bool(key)}
        ports = {"radarr": 7878, "sonarr": 8989, "prowlarr": 9696}
        secret[name] = {"base_url": f"http://127.0.0.1:{ports[name]}", "api_key": key}
    secret["overseerr"] = {"base_url": "http://127.0.0.1:5055", "api_key": None}
    secret["plex"] = {"base_url": "http://127.0.0.1:32400", "token": None}
    secret["tautulli"] = {"base_url": "http://127.0.0.1:8181", "api_key": None}
    secret["qbittorrent"] = {"base_url": args.qbit_url, "username": args.qbit_user}
    if args.qbit_pass:
        sid = qbit_login(args.qbit_url, args.qbit_user, args.qbit_pass)
        summary["qbittorrent_login"] = bool(sid)
        if sid:
            summary["qbittorrent_prefs"] = qbit_set_prefs(args.qbit_url, sid)
            summary["qbittorrent_prefs_applied"] = ["dht=off", "pex=off", "lsd=off"]
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(secret, indent=2), encoding="utf-8")
    dest.chmod(0o600)
    print(json.dumps(summary))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Rewrite AllowedIPs. Never prints PrivateKey."""
from __future__ import annotations
import argparse
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="src", required=True)
    p.add_argument("--out", dest="dst", required=True)
    p.add_argument("--lan", action="append", default=[])
    p.add_argument("--wg", action="append", default=[])
    p.add_argument("--extra", action="append", default=[])
    args = p.parse_args()
    prefixes = [x for x in (args.lan + args.wg + args.extra) if x]
    if not prefixes:
        raise SystemExit("need prefixes")
    if "0.0.0.0/0" in prefixes or "::/0" in prefixes:
        raise SystemExit("full tunnel forbidden")
    text = Path(args.src).read_text(encoding="utf-8")
    out, replaced = [], False
    for line in text.splitlines():
        if line.strip().lower().startswith("allowedips"):
            out.append("AllowedIPs = " + ", ".join(prefixes)); replaced = True
        else:
            out.append(line)
    if not replaced:
        raise SystemExit("AllowedIPs line not found")
    dest = Path(args.dst)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    dest.chmod(0o600)
    print(f"ok wrote {dest}")

if __name__ == "__main__":
    main()

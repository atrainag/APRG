#!/usr/bin/env python3
"""
whois_parser.py

Usage (from repo root):
    python -m parsers.whois_parser --target example.com --base outputs

Expect raw input:
    outputs/<target>/raw/whois_<target>.txt

Produces parsed output:
    outputs/<target>/parsed/whois.json
"""
import re
import os
import json
import argparse
from pathlib import Path

# Regex helpers (case-insensitive, multiline)
RE_DOMAIN = re.compile(r"(?mi)^\s*domain name[:\s]*([^\r\n]+)\s*$")
RE_REGISTRAR = re.compile(r"(?mi)^\s*registrar[:\s]*([^\r\n]+)\s*$")
RE_CREATED = re.compile(
    r"(?mi)^\s*(?:creation date|created on|registered on|created)[:\s]*([^\r\n]+)\s*$"
)
RE_EXPIRES = re.compile(
    r"(?mi)^\s*(?:registry expiry date|expires on|expiry date|paid-till|expire[s]*|expires)[:\s]*([^\r\n]+)\s*$"
)
RE_NS = re.compile(
    r"(?mi)^\s*(?:name server|nserver|ns(?:erver)?)[\.:]?\s*([^\r\n]+)\s*$"
)
RE_EMAIL = re.compile(r"(?mi)([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})")
RE_PHONE = re.compile(
    r"(?mi)(?:\+?\d{1,3}[\s\-\.]?)?(?:\(\d+\)[\s\-\.]?)?\d{2,4}[\s\-\.]?\d{2,4}[\s\-\.]?\d{2,4}"
)


def read_raw_whois(target, raw, base="outputs"):
    if raw == "NON":
        raw_path = Path(base) / target / "raw" / f"whois_{target}.txt"
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw whois file not found: {raw_path}")
    else:
        raw_path = Path(raw)
    text = raw_path.read_text(encoding="utf-8", errors="replace")
    return text


def find_all(pattern, text):
    return [m.group(1).strip() for m in pattern.finditer(text) if m.group(1).strip()]


def first_match(pattern, text):
    m = pattern.search(text)
    return m.group(1).strip() if m else None


def parse_whois_text(text):
    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Sometimes whois includes multiple blocks — pick the *last* domain block if multiple occur
    domains = find_all(RE_DOMAIN, text)
    domain = domains[-1] if domains else first_match(RE_DOMAIN, text)

    registrar = first_match(RE_REGISTRAR, text)
    created = first_match(RE_CREATED, text)
    expires = first_match(RE_EXPIRES, text)

    # Name servers — collect all, dedupe preserving order
    ns = []
    for m in RE_NS.finditer(text):
        val = m.group(1).strip().rstrip(".").lower()
        if val not in ns:
            ns.append(val)

    # Emails — often appear many times; prefer admin/contact-looking ones
    emails = []
    for em in RE_EMAIL.finditer(text):
        e = em.group(1).strip()
        if e.lower() not in emails:
            emails.append(e.lower())

    # Phone numbers — crude extraction, dedupe
    phones = []
    for ph in RE_PHONE.finditer(text):
        p = ph.group(0).strip()
        if p not in phones:
            phones.append(p)

    parsed = {
        "domain": domain,
        "registrar": registrar,
        "created": created,
        "expires": expires,
        "name_servers": ns,
        "emails": emails,
        "phones": phones,
    }
    return parsed


def write_parsed(target, parsed, base="outputs"):
    parsed_dir = Path(base) / target / "parsed"
    parsed_dir.mkdir(parents=True, exist_ok=True)
    outpath = parsed_dir / "whois.json"
    with outpath.open("w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    return str(outpath)


def run(target, raw, base="outputs"):
    text = read_raw_whois(target, raw, base=base)
    parsed = parse_whois_text(text)
    out = write_parsed(target, parsed, base=base)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="NON", help="Raw file")
    ap.add_argument(
        "--target", required=True, help="Target name (folder under outputs)"
    )
    ap.add_argument("--base", default="outputs", help="Base outputs directory")
    args = ap.parse_args()
    try:
        out = run(args.target, args.raw, base=args.base)
        print("[+] Parsed whois saved to:", out)
    except Exception as e:
        print("[!] Error:", e)
        raise

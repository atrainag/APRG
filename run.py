#!/usr/bin/env python3
import argparse
import os

import yaml
from parsers import nmap_parser
from report.generate_docx import generate_report
from tools import nmap_runner, theharvester_runner, whois_runner

OUTPUT_DIR = "outputs"



def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ensure_out(target):
    d = os.path.join(OUTPUT_DIR, target)
    os.makedirs(d, exist_ok=True)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    args = ap.parse_args()

    cfg = load_config()
    target = args.target
    outdir = ensure_out(target)

    # Run simple sequential pipeline for MVP
    print(f"[+] Running whois for {target}")
    whois_path = whois_runner.run_whois(target, outdir)

    print(f"[+] Running theHarvester for {target}")
    theharv_path = theharvester_runner.run_theharvester(target, outdir)

    print(f"[+] Running nmap for {target}")
    nmap_xml = nmap_runner.run_nmap(target, outdir)

    print("[+] Parsing nmap output")
    parsed = nmap_parser.parse_nmap_xml(nmap_xml)

    print("[+] Generating report")
    generate_report(target, outdir, parsed)

    print("[+] Done. Report saved in", outdir)


if __name__ == "__main__":
    main()

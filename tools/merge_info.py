import os, json, argparse

def merge_parsed(base_dir):
    merged = {"whois": {}, "dns": {}, "ports": [], "web": {}, "notes": []}
    for fname in os.listdir(base_dir):
        if not fname.endswith(".json"): 
            continue
        fpath = os.path.join(base_dir, fname)
        with open(fpath) as f:
            data = json.load(f)
        if fname.startswith("whois"):
            merged["whois"] = data
        elif fname.startswith("dns"):
            merged["dns"] = data
        elif fname.startswith("nmap"):
            merged["ports"].extend(data.get("ports", []))
        elif fname.startswith("gobuster"):
            merged["web"]["paths"] = data.get("paths", [])
        elif fname.startswith("sqlmap"):
            merged["web"]["sql_injections"] = data.get("injections", [])
        else:
            merged["notes"].append({fname: data})
    return merged

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--base", default="outputs")
    args = ap.parse_args()
    target_dir = os.path.join(args.base, args.target, "parsed")
    merged = merge_parsed(target_dir)
    outpath = os.path.join(args.base, args.target, "summary.json")
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(merged, f, indent=2)
    print("[+] Summary saved:", outpath)

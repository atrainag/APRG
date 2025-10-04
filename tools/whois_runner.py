import os
import subprocess


def run_whois(target, outdir):

    out = os.path.join(outdir, f"whois_{target}.txt")
    with open(out, "w") as f:
        subprocess.run(["whois", target], stdout=f, stderr=subprocess.DEVNULL, check=False)
    return out

import os
import subprocess


def run_theharvester(target, outdir):

    out = os.path.join(outdir, f"theharvester_{target}.html")
    # Example: theHarvester -d example.com -b google -f out.html
    subprocess.run(["theHarvester", "-d", target, "-b", "google", "-f", out], check=False)
    return out

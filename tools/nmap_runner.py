import subprocess
import os


def run_nmap(target, outdir):
    xml_out = os.path.join(outdir, f"nmap_{target}.xml")
    cmd = ["nmap", "-sV", "-O", "-oX", xml_out, target]
    subprocess.run(cmd, check=False)
    return xml_out

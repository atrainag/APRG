# AutoPentest — Automated Pentesting Report Generator (MVP)

Prototype that runs a small set of reconnaissance & scan tools, parses output, and generates a Word report.

## Quick start (dev environment)

1. Create a Python 3.10+ virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the prototype (example):

```
python run.py --target example.com
```

Outputs will be written to outputs/<target>/ and a Word report report\_<target>.docx will be created.

WARNING: Only scan targets you own or have permission to test.``

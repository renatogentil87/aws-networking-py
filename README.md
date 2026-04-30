# aws-networking-py

**Learn Python by automating AWS networking tasks.**

One script at a time. Each script does one thing. You run it, you see results, you learn.

## How This Project Works

```
aws-networking-py/
├── scripts/                    ← Your scripts. One file per task.
│   ├── cloudwan_routes.py      ← python3 scripts/cloudwan_routes.py --segment hybrid
│   ├── cloudwan_attachments.py
│   ├── vpc_routes.py
│   ├── vpn_status.py
│   └── ...                     ← You add more as you learn
├── exercises/                  ← Learning exercises (follow LEARNING.md)
├── config/                     ← YAML files for drift detection (later)
├── outputs/                    ← JSON files your scripts save
├── LEARNING.md                 ← Your daily learning guide
├── requirements.txt
└── README.md
```

Every script:
- Does one thing
- Takes arguments from the command line
- Prints results to the terminal
- Saves output as JSON

## Getting Started

```bash
cd aws-networking-py
source venv/bin/activate
pip install -r requirements.txt
```

## Running Scripts

```bash
# Check Cloud WAN routes
python3 scripts/cloudwan_routes.py \
  --global-network-id global-network-xxx \
  --core-network-id core-network-xxx \
  --segment hybrid \
  --edge ca-central-1

# Check Cloud WAN attachments
python3 scripts/cloudwan_attachments.py --core-network-id core-network-xxx

# Check VPC route tables
python3 scripts/vpc_routes.py --region ca-central-1

# Check VPN tunnel status
python3 scripts/vpn_status.py --region ca-central-1
```

## Learning Path

Follow `LEARNING.md` — it has exercises that go from Python basics to advanced automation.

Start with the exercises. Then build scripts. Then improve them over time.

## What You'll Build Over Time

| Week | What you build | What you learn |
|------|---------------|----------------|
| 1-2 | Simple scripts that print AWS data | boto3, dicts, lists, argparse |
| 3-4 | Scripts that save JSON and check for problems | JSON files, functions, filtering |
| 5-6 | Drift detection against YAML desired state | YAML, set operations, comparisons |
| 7-8 | Refactor scripts to share common code | Imports, modules, project structure |
| 9+ | Multi-region, graphs, HTML reports | Libraries, classes, advanced Python |

## License

MIT

# 🌐 AWS Networking Troubleshooting Scripts

A collection of Python scripts using **boto3** to troubleshoot, validate, and audit AWS networking resources — without touching the console.

Built for network engineers who want to automate their daily troubleshooting workflows.

## 📁 Project Structure

```
aws-networking-py/
├── cloudwan/                        # AWS Cloud WAN
│   ├── cloudwan_routes.py           # ✅ Check routes for a core network segment
│   └── cloudwan_attachments.py      # 🔲 List attachments and their state
│
├── vpc/                             # Amazon VPC
│   ├── vpc_routes.py                # 🔲 Dump all route tables for a VPC
│   ├── security_groups.py           # 🔲 Find overly permissive rules
│   ├── reachability.py              # 🔲 VPC Reachability Analyzer wrapper
│   ├── eni_lookup.py                # 🔲 Find who owns an IP address
│   └── subnet_usage.py             # 🔲 Show available IPs per subnet
│
├── vpn/                             # Site-to-Site VPN
│   ├── vpn_status.py                # 🔲 Check VPN tunnel status (UP/DOWN)
│   ├── bgp_neighbors.py             # 🔲 BGP session details and routes received
│   └── vpn_dashboard.py             # 🔲 Multi-region VPN status dashboard
│
├── tgw/                             # Transit Gateway
│   └── tgw_routes.py                # 🔲 TGW route tables, associations, propagations
│
├── validation/                      # Cross-account validation
│   └── cross_account_routes.py      # 🔲 Validate spoke account route tables via AssumeRole
│
├── reports/                         # Reporting and inventory
│   └── network_inventory.py         # 🔲 Export all networking resources to CSV
│
├── requirements.txt
└── README.md
```

> ✅ = implemented | 🔲 = to do

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- AWS CLI configured (`aws configure`) or environment variables set
- IAM permissions for the networking APIs you want to use

### Setup

```bash
git clone https://github.com/<your-username>/aws-networking-py.git
cd aws-networking-py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
# Check Cloud WAN routes for a segment
python cloudwan/cloudwan_routes.py \
  --global-network-id global-network-0abc123 \
  --core-network-id core-network-0def456 \
  --segment-name shared \
  --edge-location us-east-1
```

## 📋 Script Roadmap

### Priority 1 — Daily Troubleshooting
| Script | Description | Key boto3 API |
|--------|-------------|---------------|
| `cloudwan/cloudwan_routes.py` | Check Cloud WAN routes by segment and edge location | `networkmanager.get_network_routes` |
| `vpn/vpn_status.py` | VPN tunnel status — the 2am call script | `ec2.describe_vpn_connections` |
| `vpc/vpc_routes.py` | Dump route tables for a VPC | `ec2.describe_route_tables` |
| `vpc/eni_lookup.py` | Find who owns an IP address | `ec2.describe_network_interfaces` |

### Priority 2 — Deeper Analysis
| Script | Description | Key boto3 API |
|--------|-------------|---------------|
| `vpn/bgp_neighbors.py` | BGP session details and received routes | `ec2.describe_vpn_connections` (telemetry) |
| `tgw/tgw_routes.py` | TGW route tables with associations | `ec2.search_transit_gateway_routes` |
| `vpc/security_groups.py` | Find 0.0.0.0/0 rules and validate port access | `ec2.describe_security_groups` |
| `vpc/subnet_usage.py` | Available IPs per subnet | `ec2.describe_subnets` |

### Priority 3 — Advanced Automation
| Script | Description | Key boto3 API |
|--------|-------------|---------------|
| `vpc/reachability.py` | VPC Reachability Analyzer wrapper | `ec2.create_network_insights_path` |
| `cloudwan/cloudwan_attachments.py` | List and validate Cloud WAN attachments | `networkmanager.list_attachments` |
| `vpn/vpn_dashboard.py` | Multi-region consolidated VPN view | `ec2.describe_vpn_connections` (all regions) |
| `validation/cross_account_routes.py` | Validate spoke routes via AssumeRole | `sts.assume_role` + `ec2.describe_route_tables` |
| `reports/network_inventory.py` | Full network inventory export to CSV | Multiple APIs |

## 🧠 Python Concepts You'll Learn

| Script | Concepts |
|--------|----------|
| `vpn_status.py` | Iterating lists, datetime handling, status formatting |
| `vpc_routes.py` | boto3 Filters, nested response parsing |
| `eni_lookup.py` | Search patterns, conditional logic |
| `security_groups.py` | String matching, filtering rules |
| `tgw_routes.py` | Cross-referencing data from multiple API calls |
| `reachability.py` | Async-style polling (start job → wait → get results) |
| `vpn_dashboard.py` | Multi-region loops, reusable functions |
| `cross_account_routes.py` | STS AssumeRole, session management |
| `network_inventory.py` | File I/O, csv module, end-to-end reporting |

## 📄 License

MIT

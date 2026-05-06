"""
Exercise 18: CloudWAN Inbound Route Filtering & Prefix List Management

Scenario:
Your on-premises site advertises routes via VPN to Cloud WAN's hybrid segment.
Some of these routes are dangerous — they overlap with your AWS VPC CIDRs or
advertise default routes that could blackhole traffic.

Current state:
- VPN advertises: 192.168.10.0/24, 192.168.20.0/24, 192.168.30.0/24,
                  192.168.40.0/24, 172.16.0.0/16, 0.0.0.0/0
- Your inbound drop policy currently only blocks: 192.168.10.0/24

Problem:
- 172.16.0.0/16 from VPN CONFLICTS with your Canada VPC-A (same CIDR!)
- 0.0.0.0/0 from VPN could attract all traffic to on-prem (route leak)
- These must be filtered inbound

Tasks:
1. Read `outputs/vpn_advertised_routes.json` (routes received from VPN)
2. Read `outputs/aws_vpc_cidrs.json` (your VPC CIDRs that must be protected)
3. Detect conflicts: any VPN-advertised route that overlaps with an AWS VPC CIDR
4. Detect dangerous routes: default route (0.0.0.0/0) or supernets that cover multiple VPCs
5. Generate an updated prefix list of routes to DROP:
   ```
   CONFLICT DETECTED:
     VPN advertises 172.16.0.0/16 — conflicts with VPC-A (172.16.0.0/16)
     VPN advertises 0.0.0.0/0 — dangerous default route

   UPDATED DROP PREFIX LIST:
     - 192.168.10.0/24 (existing)
     - 172.16.0.0/16 (NEW - conflicts with VPC-A)
     - 0.0.0.0/0 (NEW - dangerous default route)

   ALLOWED THROUGH:
     - 192.168.20.0/24 ✓
     - 192.168.30.0/24 ✓
     - 192.168.40.0/24 ✓
   ```
6. Write the updated prefix list to `outputs/updated_drop_prefixes.json`

Bonus:
- Use `ipaddress` module to check if a VPN route is a SUPERNET of any VPC CIDR
  (e.g., 172.0.0.0/8 would cover 172.16.0.0/16)
- Check for subnet overlaps, not just exact matches

Hints:
- ipaddress.ip_network('172.16.0.0/16').overlaps(ipaddress.ip_network('172.16.0.0/16'))
- ipaddress.ip_network('0.0.0.0/0').supernet_of(ipaddress.ip_network('172.16.0.0/16'))
- A default route (0.0.0.0/0) is always dangerous from an external source
"""

import json


def load_vpn_routes(file):
    """Load routes advertised by VPN."""
    pass


def load_vpc_cidrs(file):
    """Load AWS VPC CIDRs to protect."""
    pass


def detect_conflicts(vpn_routes, vpc_cidrs):
    """Find VPN routes that overlap with AWS VPC CIDRs."""
    pass


def detect_dangerous_routes(vpn_routes):
    """Find default routes or overly broad supernets from VPN."""
    pass


def build_drop_prefix_list(existing_drops, new_conflicts, dangerous):
    """Combine existing drops with newly detected threats."""
    pass


def print_filter_report(conflicts, dangerous, allowed, drop_list):
    """Print the filtering analysis report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

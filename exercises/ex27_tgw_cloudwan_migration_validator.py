"""
Exercise 19: TGW-to-CloudWAN Migration Route Validator

Scenario:
You're migrating from Transit Gateway to Cloud WAN. Before cutting over,
you need to verify that Cloud WAN's segment-based routing will produce
the SAME reachability as your current TGW route tables.

Your TGW has 4 route tables:
  - full-mesh: VPC-A, VPC-B, VPN, Peering (sees all except VPC-C)
  - shared: Shared VPC (sees VPC-A, VPC-B, VPN routes)
  - isolated: VPC-C (sees only Shared VPC)
  - firewall: Firewall VPC (sees VPC-A, VPC-B, Shared VPC + default route)

Your CloudWAN has 4 segments:
  - fullmesh: VPC-A, VPC-B (shares with shared, hybrid)
  - shared: Shared VPC (shares with isolated)
  - isolated: VPC-C
  - hybrid: VPN

Tasks:
1. Read `outputs/tgw_route_tables.json` (current TGW state)
2. Read `outputs/cloudwan_segments.json` (Cloud WAN state)
3. For each VPC, determine:
   - What it can reach via TGW (current)
   - What it can reach via CloudWAN (target)
4. Report reachability gaps:
   ```
   VPC-A (172.16.0.0/16):
     TGW reachability:      172.18.0.0/16, 172.22.0.0/16, 10.20.0.0/16, 192.168.x.x
     CloudWAN reachability: 172.18.0.0/16, 172.22.0.0/16, 10.20.0.0/16, 192.168.x.x
     Status: ✓ EQUIVALENT

   VPC-C (172.20.0.0/16):
     TGW reachability:      172.22.0.0/16
     CloudWAN reachability: 172.22.0.0/16, 10.40.0.0/16
     Status: ⚠ CLOUDWAN HAS MORE ROUTES (shared segment includes eu-west-2 shared VPC)
     Action: Verify if VPC-C should reach eu-west-2 Shared VPC

   Firewall VPC (100.64.0.0/16):
     TGW reachability:      172.16.0.0/16, 172.18.0.0/16, 172.22.0.0/16, 0.0.0.0/0
     CloudWAN reachability: NOT ATTACHED
     Status: ✗ MIGRATION GAP - Firewall VPC not yet on CloudWAN
   ```

Bonus:
- Suggest which CloudWAN segment the Firewall VPC should join
- Identify if any blackhole routes in TGW need equivalent "drop" policies in CloudWAN

Hints:
- TGW reachability = routes in the route table the VPC is associated with (minus its own CIDR)
- CloudWAN reachability = routes in the segment the VPC belongs to (minus its own CIDR)
- Don't forget: CloudWAN sharing is transitive through segment-actions
"""

import json


def load_tgw_routes(file):
    """Load TGW route tables."""
    pass


def load_cloudwan_routes(file):
    """Load CloudWAN segment routes."""
    pass


def get_tgw_reachability(vpc_cidr, tgw_data):
    """Determine what a VPC can reach via its TGW route table."""
    pass


def get_cloudwan_reachability(vpc_cidr, segment_name, cloudwan_data):
    """Determine what a VPC can reach via its CloudWAN segment."""
    pass


def compare_reachability(tgw_reach, cloudwan_reach):
    """Compare TGW vs CloudWAN reachability. Return status and differences."""
    pass


def print_migration_report(results):
    """Print the migration validation report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

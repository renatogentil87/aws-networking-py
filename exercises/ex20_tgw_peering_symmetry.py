"""
Exercise 22: TGW Peering Route Symmetry Checker

Scenario:
You have TGW peering between ca-central-1 and eu-west-2. Peering requires
STATIC routes on both sides — there's no route propagation across peering.

If you add a new VPC in London but forget to add a static route on the Canada
side pointing to it via peering, Canada VPCs can't reach it (and vice versa).

Your peering setup:
  Canada TGW (tgw-0d51868a0ff863669) ←→ London TGW (tgw-09ab9333bcf15e162)
  Peering attachment: tgw-attach-01de207ef227a3377

Canada VPCs: 172.16.0.0/16, 172.18.0.0/16, 172.20.0.0/16, 172.22.0.0/16
London VPCs: 10.10.0.0/16, 10.20.0.0/16, 10.30.0.0/16, 10.40.0.0/16

Tasks:
1. Read `outputs/tgw_peering_routes.json` (routes on both sides of the peering)
2. Check symmetry: for every route pointing to peering on side A,
   there should be a corresponding VPC/route on side B that can route back
3. Detect asymmetric routes (one side can reach the other, but not vice versa)
4. Detect missing routes (a VPC exists but no peering route points to it)
5. Print a symmetry report:
   ```
   CANADA → LONDON (via peering):
     ✓ 10.20.0.0/16 → peering (London VPC-B exists and has return route)
     ✓ 10.40.0.0/16 → peering (London Shared VPC exists and has return route)
     ✗ 10.10.0.0/16 → MISSING (London VPC-A has no route from Canada)
     ✗ 10.30.0.0/16 → MISSING (London VPC-C not reachable from Canada)

   LONDON → CANADA (via peering):
     ✓ 172.16.0.0/16 → peering (Canada VPC-A exists and has return route)
     ✓ 172.22.0.0/16 → peering (Canada Shared VPC reachable)
     ✗ 172.18.0.0/16 → MISSING (Canada VPC-B not reachable from London)

   ASYMMETRIC PATHS: 3
   RECOMMENDATION: Add static routes for missing prefixes on both sides
   ```

Hints:
- Peering routes are always static (Type: "static")
- Check both directions independently
- A route is symmetric if: Canada has route to X via peering AND London has route to Y via peering
- Remember: the peering attachment ID is the same on both sides but referenced differently
"""

import json


def load_peering_routes(file):
    """Load peering route data for both TGWs."""
    pass


def get_peering_routes(tgw_routes):
    """Extract only routes that point to the peering attachment."""
    pass


def check_symmetry(canada_peering_routes, london_peering_routes, canada_vpcs, london_vpcs):
    """Check if routes are symmetric across the peering."""
    pass


def find_missing_routes(peering_routes, remote_vpcs):
    """Find VPCs on the remote side that have no peering route."""
    pass


def print_symmetry_report(canada_results, london_results):
    """Print the symmetry analysis report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

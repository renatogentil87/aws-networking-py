"""
Exercise 24: TGW Blackhole & Route Conflict Detector

Scenario:
Your TGW has blackhole routes to intentionally block traffic (e.g., VPC-C
is blackholed on the full-mesh RT to enforce isolation). But blackholes can
also appear UNINTENTIONALLY when:
  - A VPC attachment is deleted but the propagated route remains
  - A static route points to a detached/deleted attachment
  - A peering attachment goes down

You also have potential route CONFLICTS:
  - Same CIDR in multiple route tables with different next-hops
  - A static route overriding a propagated route (static wins)
  - Overlapping CIDRs where longest-prefix-match might cause unexpected behavior

Tasks:
1. Read `outputs/tgw_route_conflicts.json`
2. Categorize blackhole routes:
   - INTENTIONAL: matches your isolation policy (VPC-C blocked on full-mesh)
   - SUSPICIOUS: blackhole for a CIDR that should be reachable
3. Detect route conflicts:
   - Same CIDR appears in the same RT with different states (active vs blackhole)
   - A propagated route exists but a static blackhole overrides it
   - Overlapping prefixes (e.g., 172.16.0.0/16 and 172.16.20.0/24 both exist)
4. Print analysis:
   ```
   BLACKHOLE ANALYSIS:
     ✓ 172.20.0.0/16 on full-mesh RT → INTENTIONAL (VPC-C isolation)
     ⚠ 10.20.0.0/16 on full-mesh RT → SUSPICIOUS (London VPC-B should be reachable via peering)
     ⚠ 172.31.0.0/16 on shared RT → SUSPICIOUS (VPN prefix blackholed - attachment down?)

   ROUTE CONFLICTS:
     ⚠ 172.22.0.0/16 on full-mesh RT:
       - Static route → peering attachment
       - Propagated route → shared-vpc attachment
       Winner: STATIC (peering) — is this intended?

   OVERLAPPING PREFIXES:
     ⚠ full-mesh RT: 172.16.0.0/16 (→ vpc-a) overlaps with 172.16.20.0/24 (→ vpc-a-subnet)
       Longest prefix match: traffic to 172.16.20.0/24 uses the /24 route

   SUMMARY: 1 intentional blackhole, 2 suspicious, 1 conflict, 1 overlap
   ```

Hints:
- Static routes always win over propagated routes for the same prefix
- Longest prefix match: /24 is more specific than /16
- A blackhole with no matching isolation policy = suspicious
- Use ipaddress module to check if one prefix is a subnet of another
"""

import json


def load_routes(file):
    """Load TGW route data."""
    pass


def classify_blackholes(routes, isolation_policy):
    """Classify blackhole routes as intentional or suspicious."""
    pass


def detect_conflicts(routes):
    """Find same-CIDR routes with different next-hops or states."""
    pass


def detect_overlaps(routes):
    """Find overlapping prefixes using longest-prefix-match logic."""
    pass


def print_analysis(blackholes, conflicts, overlaps):
    """Print the full route analysis report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

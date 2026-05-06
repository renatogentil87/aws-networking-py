"""
Exercise 25: TGW VPN Route Preference & Failover Simulation

Scenario:
You have two VPN connections to your on-premises site via TGW:
  - Primary VPN (vpn-0583032be2a67f256): BGP ASN 65001, shorter AS_PATH
  - Backup VPN (vpn-024e020d345ca6fef): BGP ASN 65001, longer AS_PATH (prepended)

Both advertise the same prefixes: 192.168.20.0/24, 192.168.30.0/24, 192.168.40.0/24, 172.31.0.0/16

AWS TGW selects the best route based on:
  1. Longest prefix match
  2. Static > Propagated
  3. Shortest AS_PATH (for propagated BGP routes)
  4. Lowest MED

Tasks:
1. Read `outputs/tgw_vpn_routes.json` (routes from both VPN connections)
2. For each prefix, determine which VPN is the ACTIVE path and why
3. Simulate a failover: primary VPN goes DOWN
   - Which routes switch to backup?
   - Are there any prefixes that become unreachable (no backup)?
4. Simulate AS_PATH manipulation: what if backup prepends 3x instead of 1x?
   - Does it change the preference? (No — shortest still wins regardless of how much longer)
5. Print route preference report:
   ```
   ROUTE PREFERENCE TABLE:
   Prefix              Active VPN      AS_PATH         Backup VPN      AS_PATH
   192.168.20.0/24     vpn-058...      65001           vpn-024...      65001 65001
   192.168.30.0/24     vpn-058...      65001           vpn-024...      65001 65001
   172.31.0.0/16       vpn-058...      65001           vpn-024...      65001 65001

   FAILOVER SIMULATION (Primary DOWN):
     192.168.20.0/24 → FAILOVER to vpn-024... (AS_PATH: 65001 65001)
     192.168.30.0/24 → FAILOVER to vpn-024... (AS_PATH: 65001 65001)
     172.31.0.0/16   → FAILOVER to vpn-024... (AS_PATH: 65001 65001)
     Status: ALL PREFIXES HAVE BACKUP ✓

   WHAT-IF: Both VPNs advertise same AS_PATH length?
     → TGW uses ECMP (equal-cost multi-path) across both tunnels
     → Traffic is load-balanced, not active/passive
   ```

Hints:
- AS_PATH is a list of ASNs; length = number of ASNs in the list
- Shorter AS_PATH = preferred
- If AS_PATH length is equal, TGW does ECMP across both
- A VPN with Status "DOWN" has its routes withdrawn from the TGW RT
"""

import json


def load_vpn_routes(file):
    """Load VPN route data with AS_PATH info."""
    pass


def determine_preference(routes_for_prefix):
    """Given multiple routes for same prefix, determine which is active and why."""
    pass


def simulate_failover(all_routes, failed_vpn_id):
    """Simulate a VPN failure and determine new active routes."""
    pass


def detect_single_points_of_failure(all_routes):
    """Find prefixes that only have one VPN path (no redundancy)."""
    pass


def print_preference_report(preferences, failover_results):
    """Print route preference and failover simulation report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

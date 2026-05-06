"""
Exercise 20: CloudWAN Multi-Region Traffic Engineering & Policy Simulation

Scenario:
You manage a Cloud WAN spanning ca-central-1 and eu-west-2. A new requirement
comes in: the security team wants ALL traffic from the isolated segment destined
to on-premises (hybrid segment) to be inspected by the Firewall VPC first.

Currently:
- isolated segment shares with shared (via segment-actions)
- hybrid segment has VPN to on-prem
- There is NO direct path from isolated → hybrid

The security team wants:
- VPC-C (isolated) traffic to on-prem must go: VPC-C → shared → fullmesh → hybrid (VPN)
- But with an inspection hop: VPC-C → Firewall → hybrid (VPN)
- This requires a "service insertion" pattern using attachment routing policies

Tasks:
1. Read `outputs/cloudwan_policy_current.json`
2. Read `outputs/traffic_flows.json` (simulated traffic flows with src/dst)
3. For each traffic flow, determine the path through Cloud WAN segments:
   - Which segment does the source belong to?
   - Which segment does the destination belong to?
   - Is there a direct sharing relationship, or does it need to traverse multiple segments?
4. Identify flows that CANNOT reach their destination (no sharing path exists)
5. Identify flows that SHOULD be inspected (isolated → hybrid)
6. Generate a report:
   ```
   FLOW: VPC-C (172.20.0.0/16) → On-Prem (192.168.20.0/24)
     Source segment: isolated
     Dest segment:   hybrid
     Path: isolated → shared → hybrid (via segment sharing chain)
     Inspection required: YES (isolated to external)
     Hops: 2 segment traversals

   FLOW: VPC-A (172.16.0.0/16) → VPC-B (172.18.0.0/16)
     Source segment: fullmesh
     Dest segment:   fullmesh
     Path: direct (same segment)
     Inspection required: NO
     Hops: 0 segment traversals

   FLOW: VPC-C (172.20.0.0/16) → VPC-A (172.16.0.0/16)
     Source segment: isolated
     Dest segment:   fullmesh
     Path: NO PATH EXISTS
     Status: ✗ BLOCKED (isolated cannot reach fullmesh - by design)
   ```

7. Suggest policy changes needed to enable inspection for isolated→hybrid flows

Bonus:
- Build a graph of segment relationships and use BFS/DFS to find paths
- Calculate if adding a new segment-action would create unintended reachability

Hints:
- Sharing is directional: "fullmesh shares with shared" means shared can SEE fullmesh routes
- To find a path from segment A to segment B, you need a chain of shares
- isolated sees shared routes (shared shares with isolated)
- shared sees fullmesh and hybrid routes (they share with shared)
- So isolated → shared → hybrid is possible IF hybrid shares with shared
"""

import json


def load_policy(file):
    """Load CloudWAN policy."""
    pass


def load_traffic_flows(file):
    """Load simulated traffic flows."""
    pass


def build_segment_graph(segment_actions):
    """Build a directed graph of segment sharing relationships.
    
    If segment A shares with segment B, then B can reach A's routes.
    Edge direction: A → B means "B can see A's routes"
    """
    pass


def find_segment_for_prefix(prefix, segment_assignments):
    """Determine which segment a prefix belongs to."""
    pass


def find_path(source_segment, dest_segment, graph):
    """Find the path between two segments using the sharing graph."""
    pass


def requires_inspection(source_segment, dest_segment):
    """Determine if a flow requires security inspection."""
    pass


def analyze_flow(flow, segment_assignments, graph):
    """Analyze a single traffic flow and determine path/reachability."""
    pass


def print_flow_report(results):
    """Print traffic flow analysis report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

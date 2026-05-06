"""
Exercise 21: TGW Route Table Isolation Verification

Scenario:
Your Transit Gateway has 4 route tables implementing network segmentation:
  - full-mesh: VPC-A, VPC-B, VPN, Peering can all talk to each other
  - shared: Shared VPC can reach VPC-A, VPC-B, and VPN
  - isolated: VPC-C can ONLY reach Shared VPC
  - firewall: Firewall VPC receives traffic for inspection

VPC-C (172.20.0.0/16) is in the isolated segment. It must NEVER be able to
reach VPC-A, VPC-B, or the VPN directly. The only path out is via Shared VPC.

A junior engineer accidentally propagated VPC-A into the isolated route table.
You need a script that audits route table isolation.

Tasks:
1. Read `outputs/tgw_isolation_audit.json`
2. Define isolation rules:
   - isolated RT: ONLY Shared VPC (172.22.0.0/16) and default route allowed
   - full-mesh RT: VPC-C (172.20.0.0/16) must be blackholed or absent
   - shared RT: must NOT have VPC-C routes
3. For each route table, check if any route violates the isolation policy
4. Print an audit report:
   ```
   ROUTE TABLE: isolated (tgw-rtb-0af904d0ef0293628)
     ✓ 172.22.0.0/16 → shared-vpc (ALLOWED)
     ✓ 0.0.0.0/0 → firewall-vpc (ALLOWED)
     ✗ 172.16.0.0/16 → vpc-a (VIOLATION - isolated must not reach VPC-A)
     ✗ 192.168.20.0/24 → vpn (VIOLATION - isolated must not reach VPN directly)

   ROUTE TABLE: full-mesh (tgw-rtb-0a6cdcbdb133655ec)
     ✓ 172.20.0.0/16 → blackhole (CORRECTLY BLOCKED)
     ✓ 172.16.0.0/16 → vpc-a (ALLOWED)
     ✓ 172.18.0.0/16 → vpc-b (ALLOWED)

   VIOLATIONS FOUND: 2
   ```

Hints:
- Define allowed routes per route table as a dict
- A blackhole route for a CIDR means it's intentionally blocked
- The isolation policy is: VPC-C sees ONLY shared services, nothing else
"""

import json


def load_tgw_routes(file):
    """Load TGW route tables for audit."""
    pass


def define_isolation_policy():
    """Define what each route table is allowed to contain.
    
    Returns a dict like:
    {
        "isolated": {
            "allowed_cidrs": ["172.22.0.0/16", "0.0.0.0/0"],
            "must_blackhole": [],
            "forbidden_cidrs": ["172.16.0.0/16", "172.18.0.0/16", "192.168.0.0/16"]
        },
        ...
    }
    """
    pass


def audit_route_table(rt_name, routes, policy):
    """Check routes against isolation policy. Return violations and compliant routes."""
    pass


def print_audit_report(results):
    """Print formatted audit report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

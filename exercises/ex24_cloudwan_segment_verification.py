"""
Exercise 16: CloudWAN Segment Route Verification

Scenario:
You have a Cloud WAN with 4 segments: isolated, fullmesh, hybrid, shared.
Segment sharing rules:
  - fullmesh shares routes with shared and hybrid
  - hybrid shares routes with shared
  - shared shares routes with isolated

Your VPCs:
  CA-CENTRAL-1: VPC-A (172.16.0.0/16), VPC-B (172.18.0.0/16), VPC-C (172.20.0.0/16), Shared (172.22.0.0/16)
  EU-WEST-2: VPC-A (10.10.0.0/16), VPC-B (10.20.0.0/16), VPC-C (10.30.0.0/16), Shared (10.40.0.0/16)

Segment assignments:
  - fullmesh: VPC-A (ca), VPC-B (ca), VPC-A (eu), VPC-B (eu)
  - isolated: VPC-C (ca), VPC-C (eu)
  - shared: Shared VPC (ca), Shared VPC (eu)
  - hybrid: VPN attachment

Tasks:
1. Read `outputs/cloudwan_segments.json` (segment route tables from Cloud WAN)
2. Based on the sharing rules above, calculate which prefixes SHOULD appear in each segment
3. For each segment, report:
   - EXPECTED routes that are MISSING
   - UNEXPECTED routes that should NOT be there
4. Print a compliance report:
   ```
   Segment: isolated
     ✓ 172.22.0.0/16 (from shared) - PRESENT
     ✓ 10.40.0.0/16 (from shared) - PRESENT
     ✗ 172.16.0.0/16 (from fullmesh) - UNEXPECTED (isolation violation!)

   Segment: hybrid
     ✓ 172.16.0.0/16 (from fullmesh) - PRESENT
     ✗ 10.30.0.0/16 (from isolated) - UNEXPECTED
   ```

Hints:
- The isolated segment should ONLY see routes shared from the shared segment
- The hybrid segment should see fullmesh routes (via sharing) but NOT isolated routes
- Think about what "share" means: routes from segment X become visible in segment Y
- A route appearing where it shouldn't indicates a policy misconfiguration
"""

import json


def load_segment_routes(file):
    """Load Cloud WAN segment route tables."""
    pass


def calculate_expected_routes(segment_name, segment_assignments, sharing_rules):
    """Given sharing rules, calculate which prefixes should appear in a segment."""
    pass


def verify_segment_compliance(segment_name, actual_routes, expected_routes, forbidden_sources):
    """Check if actual routes match expected state. Return present, missing, unexpected."""
    pass


def print_compliance_report(results):
    """Print formatted compliance report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

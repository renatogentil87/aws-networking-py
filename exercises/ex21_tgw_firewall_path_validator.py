"""
Exercise 23: TGW Firewall Inspection Path Validator

Scenario:
Your TGW implements centralized egress inspection via a Firewall VPC (100.64.0.0/16).
The traffic flow for internet-bound traffic is:

  VPC-A → TGW (full-mesh RT, 0.0.0.0/0 → firewall attachment)
       → Firewall VPC (TGW subnet → NFW endpoint → NAT GW → IGW)
       → Internet
       → Return: IGW → NAT → NFW endpoint → TGW subnet
       → TGW (firewall RT, 172.16.0.0/16 → vpc-a attachment)
       → VPC-A

If ANY hop in this chain is misconfigured, traffic blackholes.

Common failures:
- Firewall RT missing return route to a VPC
- Full-mesh RT missing 0.0.0.0/0 pointing to firewall
- Firewall VPC route table not pointing to NFW endpoint
- Appliance mode not enabled on firewall attachment (causes asymmetric routing)

Tasks:
1. Read `outputs/tgw_firewall_path.json` (all route tables in the inspection path)
2. For each VPC that uses the firewall for egress, trace the FULL path:
   a. VPC route table has 0.0.0.0/0 → TGW? 
   b. TGW route table has 0.0.0.0/0 → firewall attachment?
   c. Firewall TGW subnet route table has 0.0.0.0/0 → NFW endpoint?
   d. Firewall public subnet has 0.0.0.0/0 → IGW?
   e. RETURN: Firewall RT in TGW has route back to VPC CIDR?
   f. Appliance mode enabled on firewall attachment?
3. Print path validation:
   ```
   INSPECTION PATH: VPC-A (172.16.0.0/16) → Internet
     [1] VPC-A RT: 0.0.0.0/0 → tgw-0d51868a0ff863669          ✓
     [2] TGW full-mesh RT: 0.0.0.0/0 → firewall-vpc-attachment  ✓
     [3] FW TGW-subnet RT: 0.0.0.0/0 → vpce-0beb16e3ff4353b12  ✓
     [4] FW private RT: 0.0.0.0/0 → nat-0xxxxx                  ✓
     [5] FW public RT: 0.0.0.0/0 → igw-0xxxxx                   ✓
     [6] RETURN - TGW firewall RT: 172.16.0.0/16 → vpc-a        ✓
     [7] Appliance mode: ENABLED                                  ✓
     Status: FULL PATH VALID ✓

   INSPECTION PATH: VPC-C (172.20.0.0/16) → Internet
     [1] VPC-C RT: 0.0.0.0/0 → tgw-0d51868a0ff863669          ✗ MISSING
     Status: BROKEN AT HOP 1 - VPC-C has no default route to TGW
   ```

Hints:
- Appliance mode ensures return traffic goes to the same AZ's firewall endpoint
- Without appliance mode, asymmetric routing causes drops
- The firewall VPC has 3 subnets: TGW subnet, firewall subnet, public subnet
- Each subnet has its own route table with different next-hops
"""

import json


def load_inspection_path(file):
    """Load all route tables involved in the inspection path."""
    pass


def validate_outbound_path(vpc_name, vpc_cidr, path_data):
    """Validate each hop in the outbound path to internet."""
    pass


def validate_return_path(vpc_cidr, path_data):
    """Validate the return path from firewall back to VPC."""
    pass


def check_appliance_mode(attachment_config):
    """Check if appliance mode is enabled on firewall attachment."""
    pass


def print_path_report(results):
    """Print the full path validation report."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

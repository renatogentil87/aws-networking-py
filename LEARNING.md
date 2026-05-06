# Learning Path

Your daily guide. Each exercise is a real networking task you'd do at work.

Write your code in `exercises/`. The scripts in `scripts/` are your reference — look AFTER you try.

---

## Level 1 — Python Basics Through Networking (Week 1)

You know boto3 but need Python fundamentals. These exercises use networking data.

### Exercise 1.1 — Print VPN tunnel status from a list

Create `exercises/ex01_vpn_list.py`

You have this data (copy it into your file):
```python
tunnels = [
    {"ip": "52.1.2.3", "status": "UP"},
    {"ip": "52.4.5.6", "status": "DOWN"},
    {"ip": "35.7.8.9", "status": "UP"},
    {"ip": "35.10.11.12", "status": "DOWN"},
]
```

Tasks:
- Loop through the list and print each tunnel: `52.1.2.3: UP`
- Count how many are UP and how many are DOWN
- Print a summary: `2 UP, 2 DOWN`

### Exercise 1.2 — Work with route table data

Create `exercises/ex02_routes.py`

You have this data:
```python
routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
]
```

Tasks:
- Print all routes: `10.0.0.0/16 → local [active]`
- Print only blackhole routes
- Print only active routes
- Count blackholes and print: `Found 2 blackhole routes`

### Exercise 1.3 — Write a function

Create `exercises/ex03_functions.py`

Using the same route data from 1.2:
- Write a function `find_blackholes(routes)` that takes a list of routes and returns only the blackholes
- Write a function `find_active(routes)` that returns only active routes
- Call both functions and print the results

This is the most important exercise. If you understand functions, you understand the whole project.

### Exercise 1.4 — Save and load JSON

Create `exercises/ex04_json.py`

Tasks:
- Take the routes list from 1.2
- Save it to `exercises/my_routes.json` using `json.dump()`
- Read it back using `json.load()`
- Print what you read to confirm it matches
- Run your `find_blackholes()` function on the loaded data

### Exercise 1.5 — Command line arguments

Create `exercises/ex05_argparse.py`

Tasks:
- Accept `--region` and `--vpn-id` arguments
- Print: `Checking VPN vpn-xxx in region ca-central-1`
- Add `--output` argument (optional, default: `outputs/result.json`)

Run it: `python3 exercises/ex05_argparse.py --region ca-central-1 --vpn-id vpn-123`

---

## Level 2 — Talking to AWS (Week 2)

You know boto3 basics. Now build real scripts.

### Exercise 2.1 — List all VPCs

Create `exercises/ex06_list_vpcs.py`

Tasks:
- Use boto3 to call `describe_vpcs()` in ca-central-1
- Print each VPC ID and CIDR block
- Add `--region` argument

### Exercise 2.2 — Check VPN tunnel status (real AWS)

Create `exercises/ex07_vpn_real.py`

Scenario: It's 2am. A VPN is reported down. You need to check quickly.

Tasks:
- Fetch all VPN connections in a region
- For each VPN, print the VPN ID and state
- For each tunnel, print the outside IP and status (UP/DOWN)
- Save to `outputs/vpn_status.json`
- Add `--region` argument

Then compare your code with `scripts/vpn_status.py`.

### Exercise 2.3 — Fetch Cloud WAN segment routes (real AWS)

Create `exercises/ex08_cloudwan_routes.py`

Scenario: You need to verify which routes are in the hybrid segment.

Tasks:
- Use `networkmanager` client, `get_network_routes()` API
- Print destination, state, type for each route
- Save to JSON
- Add arguments: `--global-network-id`, `--core-network-id`, `--segment`, `--edge`

Then compare with `scripts/cloudwan_routes.py`.

### Exercise 2.4 — Fetch VPC route tables

Create `exercises/ex09_vpc_routes.py`

Scenario: You need to check all route tables in a VPC to find where traffic goes.

Tasks:
- Use `describe_route_tables()` with a VPC filter
- For each route table, print the route table ID
- For each route, print: `destination → target [state]`
- The tricky part: the target could be `GatewayId`, `TransitGatewayId`, `NatGatewayId`, `NetworkInterfaceId`, or `CoreNetworkArn` — handle all of them
- Save to JSON

### Exercise 2.5 — List Cloud WAN attachments

Create `exercises/ex10_cloudwan_attachments.py`

Scenario: You need to verify all attachments are in the correct segment.

Tasks:
- Use `list_attachments()` API
- Print: attachment ID, type, segment, state
- Save to JSON

---

## Level 3 — Analyzing Data (Week 3-4)

Now you have scripts that collect data. Time to analyze it.

### Exercise 3.1 — Find blackhole routes from saved data

Create `exercises/ex11_check_blackholes.py`

Scenario: You collected VPC route tables yesterday. Now check if any routes went blackhole overnight.

Tasks:
- Read `outputs/vpc_routes.json` (or use the sample in `examples/sample_output.json`)
- Find all routes where state is "blackhole"
- Print: `BLACKHOLE: rtb-xxx — 10.99.0.0/16 → tgw-dead000`
- Accept `--input` argument for the JSON file path

### Exercise 3.2 — Check if expected routes exist

Create `exercises/ex12_check_missing.py`

Scenario: After a change window, you need to verify all expected routes are present.

Tasks:
- Define a list of expected CIDRs: `["10.0.0.0/16", "172.16.0.0/16", "10.1.0.0/16"]`
- Read your saved route tables
- For each route table, check if all expected CIDRs exist
- Print what's missing
- Accept `--input` and `--expected` (comma-separated CIDRs) arguments

### Exercise 3.3 — VPN health check with UP/DOWN summary

Create `exercises/ex13_vpn_health.py`

Scenario: You manage 50 VPN connections. You need a daily health report.

Tasks:
- Read `outputs/vpn_status.json`
- For each VPN, count UP and DOWN tunnels
- Print a summary table:
  ```
  VPN ID                    Tunnel 1    Tunnel 2    Status
  vpn-0583032be2a67f256     UP          DOWN        DEGRADED
  vpn-0abc123def456789      UP          UP          HEALTHY
  ```
- A VPN is HEALTHY if both tunnels are UP, DEGRADED if one is DOWN, DOWN if both are DOWN

### Exercise 3.4 — Compare Cloud WAN routes before and after a change

Create `exercises/ex14_compare_routes.py`

Scenario: You're about to apply a Cloud WAN policy change. You want to compare routes before and after.

Tasks:
- Read two JSON files: `--before` and `--after`
- Find routes that were added (in after but not before)
- Find routes that were removed (in before but not after)
- Print a diff report:
  ```
  ADDED:   192.168.10.0/24
  REMOVED: 172.16.0.0/12
  ```

This is the foundation of drift detection.

---

## Level 4 — Drift Detection (Week 5-6)

### Exercise 4.1 — Create a desired state YAML

Create `exercises/ex15_desired_state.yaml`

Write a YAML file that describes what your network SHOULD look like:
```yaml
vpn_connections:
  vpn-0583032be2a67f256:
    expected_state: available
    tunnels:
      - status: UP
      - status: UP

cloudwan_segments:
  hybrid:
    edge_location: ca-central-1
    expected_routes:
      - "192.168.20.0/24"
      - "192.168.30.0/24"
      - "192.168.40.0/24"
    should_not_have:
      - "192.168.10.0/24"
```

### Exercise 4.3 — Cloud WAN route drift detection

Create `exercises/ex17_cloudwan_drift.py`

Scenario: You applied a routing policy to drop 192.168.10.0/24. Verify it worked.

Tasks:
- Read your desired state YAML (which says hybrid should NOT have 192.168.10.0/24)
- Fetch actual Cloud WAN routes (or read from saved JSON)
- Check: are the expected routes present? Are the blocked routes absent?
- Print a drift report

### Exercise 4.4 — Full network health check

Create `exercises/ex18_full_check.py`

Scenario: Monday morning. Run one script to check everything.

Tasks:
- Check VPN tunnels (all UP?)
- Check Cloud WAN routes (expected routes present? blocked routes absent?)
- Check VPC route tables (any blackholes?)
- Print a summary:
  ```
  NETWORK HEALTH CHECK
  ====================
  VPN:      2 healthy, 0 degraded, 0 down
  CloudWAN: hybrid segment OK, 192.168.10.0/24 correctly dropped
  VPC:      0 blackhole routes found
  
  STATUS: HEALTHY ✅
  ```

---

## Level 4B — Transit Gateway Deep Dive (Week 6-7)

### Exercise 4.5 — TGW Route Table Isolation Audit

Create `exercises/ex19_tgw_isolation_audit.py`

Scenario: Your TGW has 4 route tables implementing network segmentation (full-mesh, shared, isolated, firewall). VPC-C (172.20.0.0/16) is in the isolated segment and must NEVER reach VPC-A, VPC-B, or the VPN directly. A junior engineer accidentally propagated VPC-A into the isolated route table. You need a script that audits route table isolation.

Tasks:
- Read `outputs/tgw_isolation_audit.json`
- Define isolation rules:
  - isolated RT: ONLY Shared VPC (172.22.0.0/16) and default route allowed
  - full-mesh RT: VPC-C (172.20.0.0/16) must be blackholed or absent
  - shared RT: must NOT have VPC-C routes
- For each route table, check if any route violates the isolation policy
- Print an audit report showing violations and compliant routes

### Exercise 4.6 — TGW Peering Route Symmetry Checker

Create `exercises/ex20_tgw_peering_symmetry.py`

Scenario: You have TGW peering between ca-central-1 and eu-west-2. Peering requires STATIC routes on both sides — there's no route propagation across peering. If you add a new VPC in London but forget to add a static route on the Canada side, Canada VPCs can't reach it.

Tasks:
- Read `outputs/tgw_peering_routes.json`
- Check symmetry: for every route pointing to peering on side A, there should be a corresponding VPC on side B that can route back
- Detect asymmetric routes (one side can reach the other, but not vice versa)
- Detect missing routes (a VPC exists but no peering route points to it)
- Print a symmetry report for both directions

### Exercise 4.7 — TGW Firewall Inspection Path Validator

Create `exercises/ex21_tgw_firewall_path_validator.py`

Scenario: Your TGW implements centralized egress inspection via a Firewall VPC (100.64.0.0/16). The traffic flow is: VPC → TGW → Firewall VPC (TGW subnet → NFW endpoint → NAT GW → IGW) → Internet. If ANY hop in this chain is misconfigured, traffic blackholes.

Tasks:
- Read `outputs/tgw_firewall_path.json`
- For each VPC that uses the firewall for egress, trace the FULL path:
  - VPC route table has 0.0.0.0/0 → TGW?
  - TGW route table has 0.0.0.0/0 → firewall attachment?
  - Firewall TGW subnet route table has 0.0.0.0/0 → NFW endpoint?
  - Firewall public subnet has 0.0.0.0/0 → IGW?
  - RETURN: Firewall RT in TGW has route back to VPC CIDR?
  - Appliance mode enabled on firewall attachment?
- Print path validation showing each hop as pass/fail

### Exercise 4.8 — TGW Blackhole & Route Conflict Detector

Create `exercises/ex22_tgw_blackhole_conflict_detector.py`

Scenario: Blackholes can appear intentionally (isolation) or unintentionally (deleted attachment). You also have potential route conflicts: same CIDR with different next-hops, static overriding propagated, or overlapping prefixes.

Tasks:
- Read `outputs/tgw_route_conflicts.json`
- Categorize blackholes as INTENTIONAL (matches isolation policy) or SUSPICIOUS
- Detect route conflicts: same CIDR with different states or next-hops
- Detect overlapping prefixes (e.g., 172.16.0.0/16 and 172.16.20.0/24)
- Use `ipaddress` module to check subnet containment
- Print analysis report with recommendations

### Exercise 4.9 — TGW VPN Route Preference & Failover Simulation

Create `exercises/ex23_tgw_vpn_failover.py`

Scenario: You have two VPN connections (primary and backup). Primary has shorter AS_PATH, backup has prepended AS_PATH. Both advertise the same prefixes.

Tasks:
- Read `outputs/tgw_vpn_routes.json`
- For each prefix, determine which VPN is ACTIVE and why (shortest AS_PATH wins)
- Simulate failover: primary VPN goes DOWN — which routes switch to backup?
- Detect single points of failure (prefixes only advertised by one VPN)
- Print route preference table and failover simulation results

---

## Level 4C — Cloud WAN Routing Policies & Traffic Manipulation (Week 7-8)

### Exercise 4.10 — CloudWAN Segment Route Verification

Create `exercises/ex24_cloudwan_segment_verification.py`

Scenario: Your Cloud WAN has 4 segments (isolated, fullmesh, hybrid, shared) with sharing rules: fullmesh shares with shared and hybrid, hybrid shares with shared, shared shares with isolated. You need to verify routes appear only where they should.

Tasks:
- Read `outputs/cloudwan_segments.json`
- Based on sharing rules, calculate which prefixes SHOULD appear in each segment
- For each segment, report EXPECTED routes that are MISSING and UNEXPECTED routes that shouldn't be there
- Print a compliance report (e.g., 172.16.0.0/16 appearing in isolated = isolation violation)

### Exercise 4.11 — CloudWAN Route Summarization Policy Builder

Create `exercises/ex25_cloudwan_route_summarization.py`

Scenario: Your Cloud WAN advertises individual VPC prefixes to on-prem via VPN. The on-prem router's table is bloated. You need to summarize: 172.16/18/22 → 172.16.0.0/12 (existing) and add EU prefixes: 10.10/20/40 → 10.0.0.0/8 (new).

Tasks:
- Read `outputs/cloudwan_policy_current.json`
- Parse existing routing-policies section
- Add a new summarization rule (rule-number 200) for EU prefixes
- Validate that summary prefix covers all specific prefixes using `ipaddress` module
- Write updated policy to `outputs/cloudwan_policy_updated.json`
- Print before/after comparison

### Exercise 4.12 — CloudWAN Inbound Route Filtering & Prefix List Management

Create `exercises/ex26_cloudwan_inbound_filtering.py`

Scenario: Your on-prem site advertises routes via VPN including dangerous ones: 172.16.0.0/16 (conflicts with VPC-A!) and 0.0.0.0/0 (could blackhole all traffic). Your current drop policy only blocks 192.168.10.0/24.

Tasks:
- Read `outputs/vpn_advertised_routes.json` and `outputs/aws_vpc_cidrs.json`
- Detect conflicts: VPN routes that overlap with AWS VPC CIDRs
- Detect dangerous routes: default route or supernets covering multiple VPCs
- Generate updated prefix list of routes to DROP
- Use `ipaddress` module for overlap/supernet detection
- Print filtering report showing conflicts, allowed, and blocked routes

### Exercise 4.13 — TGW-to-CloudWAN Migration Route Validator

Create `exercises/ex27_tgw_cloudwan_migration_validator.py`

Scenario: You're migrating from TGW to Cloud WAN. Before cutting over, verify that CloudWAN's segment-based routing produces the SAME reachability as your current TGW route tables.

Tasks:
- Read `outputs/tgw_route_tables.json` and `outputs/cloudwan_segments.json`
- For each VPC, determine what it can reach via TGW vs CloudWAN
- Report reachability gaps: equivalent, CloudWAN has more routes, or migration gap
- Identify VPCs not yet attached to CloudWAN (e.g., Firewall VPC)
- Suggest which segment unattached VPCs should join

### Exercise 4.14 — CloudWAN Multi-Region Traffic Engineering & Policy Simulation

Create `exercises/ex28_cloudwan_traffic_engineering.py`

Scenario: The security team wants ALL traffic from isolated segment destined to on-prem (hybrid) to be inspected first. You need to understand segment sharing as a directed graph and trace traffic paths.

Tasks:
- Read `outputs/traffic_flows.json`
- Build a directed graph of segment sharing relationships
- For each traffic flow, determine the path through segments (or if it's blocked)
- Identify flows that require inspection (isolated → external)
- Use BFS/DFS to find paths between segments
- Print flow analysis showing path, hops, and whether inspection is needed
- Suggest policy changes for flows that are currently blocked but should be allowed

---

## Level 5 — Improving Your Code (Week 9-10)

### Exercise 5.1 — Error handling

Go back to any script and add:
- What happens if AWS credentials are expired? (try/except botocore.exceptions.ClientError)
- What happens if the JSON file doesn't exist? (try/except FileNotFoundError)
- What happens if the region is wrong?

### Exercise 5.2 — Refactor duplicate code

By now you have 10+ scripts that all create boto3 clients the same way.
- Create `scripts/helpers.py` with a `get_client(service, region)` function
- Update your scripts to import from helpers
- This is your first module — you just learned imports!

### Exercise 5.3 — Add logging

Replace `print()` with Python logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Found 3 blackhole routes")
logger.warning("VPN tunnel is DOWN")
logger.error("Failed to connect to AWS")
```

### Exercise 5.4 — Write unit tests

Create `exercises/ex29_tests.py`

Test your `find_blackholes()` function with fake data — no AWS needed:
```python
import unittest

class TestFindBlackholes(unittest.TestCase):
    def test_finds_blackholes(self):
        routes = [
            {"destination": "10.0.0.0/16", "state": "active"},
            {"destination": "10.99.0.0/16", "state": "blackhole"},
        ]
        result = find_blackholes(routes)
        self.assertEqual(len(result), 1)
```

---

## Level 6 — Advanced (Week 9+)

### Exercise 6.1 — List comprehensions
Rewrite all your loops as one-liners:
```python
blackholes = [r for r in routes if r["state"] == "blackhole"]
```

### Exercise 6.2 — Dataclasses
Replace dicts with proper Python objects:
```python
from dataclasses import dataclass

@dataclass
class Route:
    destination: str
    target: str
    state: str
```

### Exercise 6.3 — Multi-region collection
Check VPN status across ALL regions in one script.

### Exercise 6.4 — Build a single CLI tool
Combine all your scripts into one `awsnet.py` with subcommands.
This is where the project structure from before makes sense.

### Exercise 6.5 — HTML report
Generate an HTML page with your network health check results.

---

## Daily Routine

1. Open LEARNING.md
2. Pick the next exercise
3. Write it in `exercises/`
4. Run it, fix errors, run again
5. Compare with `scripts/` if stuck
6. Commit to git
7. Tomorrow: next exercise

"""
Scenario: You applied a routing policy to drop 192.168.10.0/24. Verify it worked.

Tasks:
- Read your desired state YAML (which says hybrid should NOT have 192.168.10.0/24)
- Fetch actual Cloud WAN routes (or read from saved JSON)
- Check: are the expected routes present? Are the blocked routes absent?
- Print a drift report

- global-network-id: global-network-007efcd46173a27a1
- core-network-id core-network-0d91631a180884713
- segment: hybrid
- edge: ca-central-1
"""

"""
  DRIFT REPORT: hybrid (ca-central-1)
  ====================================
  EXPECTED ROUTES:
    ✓ 192.168.20.0/24 - PRESENT
    ✓ 192.168.30.0/24 - PRESENT
    ✗ 172.18.0.0/16 - MISSING
  
  BLOCKED ROUTES:
    ✓ 192.168.10.0/24 - CORRECTLY ABSENT
    ✗ 10.30.0.0/16 - LEAK DETECTED (should not be here!)
  
  STATUS: DRIFT DETECTED
"""
import argparse

import yaml
import boto3

def get_cloudwan_routes(core_network_id, segment, global_network_id, edge):

    client = boto3.client('networkmanager')
    response = client.get_network_routes(
        GlobalNetworkId=global_network_id,
        RouteTableIdentifier={
            'CoreNetworkSegmentEdge': {
                'CoreNetworkId': core_network_id,
                'SegmentName': segment,
                'EdgeLocation': edge
            },
        }
    )
    return response

def load_desired_state(segment):
    with (open('ex15_desired_state.yml', 'r') as stream):
        desired_state = yaml.safe_load(stream)
        expected_routes = [seg for seg in desired_state['cloudwan_segments'][segment]['expected_routes']]
        should_not_have = [noroute for noroute in desired_state['cloudwan_segments'][segment]['should_not_have']]

        return expected_routes, should_not_have

def compare_routes(actual_routes, expected, should_not_have):

    missing = [route for route in expected if route not in actual_routes]
    leaked = [ route for route in should_not_have if route  in actual_routes]
    present = [ route for route in actual_routes if route in expected]

    return missing, leaked, present

def print_drift_report(missing, leaked, present, segment, edge ):

    print(f"DRIFT REPORT: {segment}, {edge}")
    print("======" *15, end='\n' )
    print(f"EXPECTED ROUTES:")
    print(f"{present} - PRESENT \n")
    print(f"LEADER ROUTES:")
    print(f"{leaked} - LEAK \n")
    print(f"MISSING ROUTES:")
    print(f"{missing} - MISSING")


def main():
    parser = argparse.ArgumentParser( description='Get CloudWAN routes')
    parser.add_argument( '--global-network-id', help='Global Network ID', required=True)
    parser.add_argument( '--segment', help='Segment ID', required=True)
    parser.add_argument('--edge', help='Edge', required=True)
    parser.add_argument( "--core-network-id", help='Cloud WLAN Network ID', required=True)
    args = parser.parse_args()

    response = get_cloudwan_routes(args.core_network_id, args.segment, args.global_network_id, args.edge)
    actual_routes = [r['DestinationCidrBlock'] for r in response['NetworkRoutes']]

    expected_routes, should_not_have  = load_desired_state(args.segment)
    missing, leaked, present   = compare_routes(actual_routes, expected_routes , should_not_have)
    print_drift_report(missing, leaked, present, args.segment, args.edge)

if __name__ == '__main__':
    main()
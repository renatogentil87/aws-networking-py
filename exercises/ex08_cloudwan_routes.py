"""
Scenario: You need to verify which routes are in the hybrid segment.

Tasks:
- Use `networkmanager` client, `get_network_routes()` API
- Print destination, state, type for each route
- Save to JSON
- Add arguments: `--global-network-id`, `--core-network-id`, `--segment`, `--edge`
- global-network-id: global-network-007efcd46173a27a1
- core-network-id core-network-0d91631a180884713
- segment: hybrid
- edge: ca-central-1
Then compare with `scripts/cloudwan_routes.py`.
"""

import json
import argparse
import boto3

def get_network_routes(global_network_id, core_network_id, segment, edge):
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

def main():
    arg_parser = argparse.ArgumentParser(description='Get CloudWAN routes')
    arg_parser.add_argument("--global-network-id", required=True)
    arg_parser.add_argument("--core-network-id", required=True)
    arg_parser.add_argument("--segment", required=True, help="e.g. hybrid")
    arg_parser.add_argument("--edge", required=True, help="e.g. ca-central-1")
    args = arg_parser.parse_args()

    network_routes = (get_network_routes( args.global_network_id, args.core_network_id, args.segment, args.edge))

    routes = []
    for dst in network_routes['NetworkRoutes']:
        for netattachment in dst['Destinations']:
            routes.append({
                "destination" : dst["DestinationCidrBlock"],
                "attachment": netattachment.get("CoreNetworkAttachmentId"),
                "State": dst["State"],
                "Type": dst["Type"],
            })

    with open('cloudwan_routes.json', 'w') as f:
        json.dump(routes, f)

    print(json.dumps(routes, indent=2))

if __name__ == "__main__":
    main()

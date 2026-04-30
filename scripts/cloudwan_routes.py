"""Check Cloud WAN routes for a segment."""

import argparse
import json
import boto3


def get_routes(global_network_id, core_network_id, segment_name, edge_location, region):
    client = boto3.client("networkmanager", region_name=region)
    response = client.get_network_routes(
        GlobalNetworkId=global_network_id,
        RouteTableIdentifier={
            "CoreNetworkSegmentEdge": {
                "CoreNetworkId": core_network_id,
                "SegmentName": segment_name,
                "EdgeLocation": edge_location,
            }
        },
    )
    return response.get("NetworkRoutes", [])


def main():
    parser = argparse.ArgumentParser(description="Check Cloud WAN routes")
    parser.add_argument("--global-network-id", required=True)
    parser.add_argument("--core-network-id", required=True)
    parser.add_argument("--segment", required=True, help="e.g. hybrid")
    parser.add_argument("--edge", required=True, help="e.g. ca-central-1")
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()

    routes = get_routes(args.global_network_id, args.core_network_id, args.segment, args.edge, args.region)

    if not routes:
        print("No routes found.")
        return

    # Print
    print(f"\n{'Destination':<25} {'Type':<15} {'State':<12}")
    print("-" * 52)
    for route in routes:
        dest = route.get("DestinationCidrBlock", "N/A")
        state = route.get("State", "N/A")
        route_type = route.get("Type", "N/A")
        print(f"{dest:<25} {route_type:<15} {state:<12}")

    # Save
    with open("outputs/cloudwan_routes.json", "w") as f:
        json.dump(routes, f, indent=2)
    print(f"\nSaved {len(routes)} routes to outputs/cloudwan_routes.json")


if __name__ == "__main__":
    main()

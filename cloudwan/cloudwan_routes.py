"""Check Cloud WAN routes for a given core network segment and edge location."""

import argparse
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

    routes = response.get("NetworkRoutes", [])
    if not routes:
        print("No routes found.")
        return

    print(f"{'Destination':<25} {'ResourceType':<15} {'State':<12} {'Type':<15}")
    print("-" * 67)
    for route in routes:
        dest = route.get("DestinationCidrBlock", "N/A")
        state = route.get("State", "N/A")
        route_type = route.get("Type", "N/A")
        destinations = route.get("Destinations", [])
        resource_type = destinations[0].get("ResourceType", "N/A") if destinations else "N/A"
        print(f"{dest:<25} {resource_type:<15} {state:<12} {route_type:<15}")



def main():
    parser = argparse.ArgumentParser(description="Check Cloud WAN routes")
    parser.add_argument("--global-network-id", required=True, help="Global network ID")
    parser.add_argument("--core-network-id", required=True, help="Core network ID")
    parser.add_argument("--segment-name", required=True, help="Segment name (e.g. shared)")
    parser.add_argument("--edge-location", required=True, help="Edge location (e.g. us-east-1)")
    parser.add_argument("--region", default="us-east-1", help="AWS region (default: us-east-1)")
    args = parser.parse_args()

    get_routes(args.global_network_id, args.core_network_id, args.segment_name, args.edge_location, args.region)


if __name__ == "__main__":
    main()

"""
Scenario: You need to check all route tables in a VPC to find where traffic goes.

Tasks:
- Use `describe_route_tables()` with a VPC filter
- For each route table, print the route table ID
- For each route, print: `destination → target [state]`
- The tricky part: the target could be `GatewayId`, `TransitGatewayId`, `NatGatewayId`, `NetworkInterfaceId`, or `CoreNetworkArn` — handle all of them
- Save to JSON


VPC Ids:
- vpc-066f19abe5b3c9887
- vpc-0219ac334c48b2c4e
- vpc-003944ca32330a44c
- vpc-0175a0134327883b4
"""

import json
import boto3
import argparse

def describe_route_tables(vpc_id):
    try:
        client = boto3.client('ec2')

        response = client.describe_route_tables(
            Filters=[
                {
                    'Name': "vpc-id",
                    'Values': [
                        vpc_id,
                    ]
                }]
        )
        result = []
        targets = ['TransitGatewayId', 'NatGatewayId', 'GatewayId', 'NetworkInterfaceId', 'CoreNetworkArn']
        for route_table in response['RouteTables']:
            for route in route_table['Routes']:
                for t in targets:
                    if t in route:
                        result.append({
                            "RouteTableId": route_table['RouteTableId'],
                            "Destination": route.get('DestinationCidrBlock'),
                            "State": route['State'],
                            "Target" : route[t]
                        })
    except Exception as e:
        print(e)

    with open(f'{vpc_id}.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

    print(json.dumps(result, indent=2))




def main():
    arg_parser = argparse.ArgumentParser(description= "Get VPC route tables")
    arg_parser.add_argument("--vpc-id", required=True, help="VPC ID")
    args = arg_parser.parse_args()

    describe_route_tables(args.vpc_id)


if __name__ == "__main__":
    main()
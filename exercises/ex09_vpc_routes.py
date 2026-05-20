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
from botocore.exceptions import ClientError


class RouteTables():
    def __init__(self, vpc_id):
        self.result = []
        self.vpc_id = vpc_id
        self.client = boto3.client('ec2')
        try:
            self.response = self.client.describe_route_tables(
                Filters=[
                    {
                        'Name': "vpc-id",
                        'Values': [
                            self.vpc_id,
                        ]
                    }]
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    def __str__(self):
        return json.dumps(self.result, indent=4)

    def routes(self):
        targets = ['TransitGatewayId', 'NatGatewayId', 'GatewayId', 'NetworkInterfaceId', 'CoreNetworkArn']
        for route_table in self.response['RouteTables']:
            for route in route_table['Routes']:
                for target in targets:
                    if target in route:
                        self.result.append({
                            "RouteTableId": route_table['RouteTableId'],
                            "Destination": route.get('DestinationCidrBlock'),
                            "State": route['State'],
                            "Target" : route[target]
                        })

        with open(f'{self.vpc_id}.json', 'w') as outfile:
            json.dump(self.result, outfile, indent=4)

        return self.result

def main():
    arg_parser = argparse.ArgumentParser(description= "Get VPC route tables")
    arg_parser.add_argument("--vpc-id", required=True, help="VPC ID")
    args = arg_parser.parse_args()

    try:
        routetable = (RouteTables(args.vpc_id))
        routetable.routes()
        print(routetable)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
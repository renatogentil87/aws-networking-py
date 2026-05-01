'''
Tasks:
- Fetch all VPN connections in a region
- For each VPN, print the VPN ID and state
- For each tunnel, print the outside IP and status (UP/DOWN)
- Save to `outputs/vpn_status.json`
- Add `--region` argument
'''

import boto3
import argparse
import json


def check_vpn(region):
    client = boto3.client('ec2', region_name=region)
    response = client.describe_vpn_connections()
    return response

def main():
    parser = argparse.ArgumentParser(description="Fetch all VPN connections in a region")
    parser.add_argument("--region", help="AWS region", required=True)
    args = parser.parse_args()
    output = []
    for vpn in check_vpn(args.region)['VpnConnections']:
        output.append(vpn)

    all_vpns = []
    for i in output:
        for x in i['VgwTelemetry']:
            vpn_details = { "vpn_id": i['VpnConnectionId'], "State": i['State'] , "OutsideIP": x['OutsideIpAddress'], "Status": x['Status']}
            all_vpns.append(vpn_details)
            print(f"VPN ID: {i['VpnConnectionId']}, State: {i['State']}, Outside IP: {x['OutsideIpAddress']} Status: {x['Status']}")

    json.dump(all_vpns, open("vpn_status.json", "w"))

if __name__ == "__main__":
    main()
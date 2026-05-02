import yaml
import boto3
import argparse

def get_vpn_status(region):
    client = boto3.client('ec2', region_name=region)
    response = client.describe_vpn_connections()
    return response

def main():
    arg_parser = argparse.ArgumentParser(description='VPN check')
    arg_parser.add_argument('--region', required=True, help='AWS region')
    args = arg_parser.parse_args()


    output = {}
    for vpn in get_vpn_status(args.region)['VpnConnections']:
        tunnels = []
        for t in vpn["VgwTelemetry"]:
            tunnels.append({"outside_ip": t["OutsideIpAddress"], "status": t["Status"]})
        output[vpn['VpnConnectionId']] = {"state": vpn['State'], "tunnels": tunnels}

    check_drift(output)

def check_drift(actual_vpn_status):
    yaml_file = "vpn_desired_status.yml"
    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)

    for vpn_id, expected in yaml_data['vpn_connections'].items():
        for i, expected_tunnel in enumerate(expected['tunnels']):
            actual_tunnel = actual_vpn_status[vpn_id]['tunnels'][i]
            if expected_tunnel['status'] == actual_tunnel['status']:
                print(f"  Tunnel {i + 1} ({actual_tunnel['outside_ip']}): {actual_tunnel['status']} ")
            else:
                print(f"  Tunnel {i + 1} ({actual_tunnel['outside_ip']}): expected {expected_tunnel['status']}, got {actual_tunnel['status']} ")


if __name__ == '__main__':
    main()
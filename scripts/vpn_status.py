"""Check VPN tunnel status — UP or DOWN."""

import argparse
import json
import boto3


def get_vpn_status(region):
    client = boto3.client("ec2", region_name=region)
    response = client.describe_vpn_connections()
    return response.get("VpnConnections", [])


def main():
    parser = argparse.ArgumentParser(description="Check VPN tunnel status")
    parser.add_argument("--region", required=True)
    args = parser.parse_args()

    vpns = get_vpn_status(args.region)

    if not vpns:
        print("No VPN connections found.")
        return

    # Print
    for vpn in vpns:
        vpn_id = vpn["VpnConnectionId"]
        state = vpn["State"]
        print(f"\n{vpn_id} ({state})")
        for tunnel in vpn.get("VgwTelemetry", []):
            ip = tunnel.get("OutsideIpAddress", "N/A")
            status = tunnel.get("Status", "N/A")
            print(f"  Tunnel {ip}: {status}")

    # Save
    with open("outputs/vpn_status.json", "w") as f:
        json.dump(vpns, f, indent=2, default=str)
    print(f"\nSaved {len(vpns)} VPN connections to outputs/vpn_status.json")


if __name__ == "__main__":
    main()

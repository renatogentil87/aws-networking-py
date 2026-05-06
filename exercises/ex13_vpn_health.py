"""
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

"""

import json


def check_vpn_health(file):
    """Parse VPN status JSON and return health assessment for each connection."""
    with open(file) as f:
        data = json.load(f)

    results = []
    for vpn in data["VpnConnections"]:
        tunnel1 = vpn["VgwTelemetry"][0]["Status"]
        tunnel2 = vpn["VgwTelemetry"][1]["Status"]

        if tunnel1 == "UP" and tunnel2 == "UP":
            status = "HEALTHY"
        elif tunnel1 == "DOWN" and tunnel2 == "DOWN":
            status = "DOWN"
        else:
            status = "DEGRADED"

        results.append(
            {
                "VPN ID": vpn["VpnConnectionId"],
                "Tunnel 1": tunnel1,
                "Tunnel 2": tunnel2,
                "Status": status,
            }
        )

    return results


def print_vpn_table(results):
    """Print a formatted summary table of VPN health status."""
    print(f"{'VPN ID':<30}{'Tunnel 1':<12}{'Tunnel 2':<12}{'Status'}")
    print("-" * 66)
    for r in results:
        print(f"{r['VPN ID']:}{r['Tunnel 1']:<12}{r['Tunnel 2']:<12}{r['Status']}")


def main():
    try:
        results = check_vpn_health("vpn_status.json")
        print_vpn_table(results)
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

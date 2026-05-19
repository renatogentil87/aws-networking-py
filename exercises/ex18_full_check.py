"""
  NETWORK HEALTH CHECK
====================
VPN:      2 healthy, 0 degraded, 0 down
CloudWAN: Route count per segment — "hybrid has 8 routes, production has 12, isolated has 4
CloudWAN: 8 attachments AVAILABLE, 0 FAILED
VPC:      0 blackhole routes found

STATUS: HEALTHY
"""

import boto3


def check_vpn():
    region = 'ca-central-1'
    client = boto3.client('ec2', region_name=region)
    response = client.describe_vpn_connections()
    return response

def vpn_check_tunnel_status(response):
    results = []
    for vpn in response["VpnConnections"]:
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


def cloudwan_route_check():
    core_network_id = "core-network-0d91631a180884713"
    global_network_id = "global-network-007efcd46173a27a1"
    edge = ['ca-central-1', 'eu-west-2']
    segment = ['isolated', 'fullmesh', 'hybrid']

    client = boto3.client('networkmanager')
    result = []
    for seg in segment:
        for ed in edge:
            response = client.get_network_routes(
                GlobalNetworkId=global_network_id,
                RouteTableIdentifier={
                    'CoreNetworkSegmentEdge': {
                        'CoreNetworkId': core_network_id,
                        'SegmentName': seg,
                        'EdgeLocation': ed,
                    },
                }
            )
            route_count = len(response['NetworkRoutes'])
            result.append({
                "Route Count": route_count,
                "Segment Name": seg,
                "Edge Location": ed,
            })

    return result


def cloudwan_attachment_check():
    client = boto3.client('networkmanager')
    response = client.list_attachments(CoreNetworkId="core-network-0d91631a180884713")
    return response


def vpc_routes_check():
    client = boto3.client('ec2', region_name='ca-central-1')
    response = client.describe_route_tables()
    results = []
    for rt in response['RouteTables']:
        for route in rt.get('Routes', []):
            if route.get('State') == 'blackhole':
                results.append({
                    "RouteTableId": rt['RouteTableId'],
                    "Destination": route.get('DestinationCidrBlock', 'N/A'),
                })
    return results


def print_report(vpn_results, cloudwan_routes, cloudwan_attachments, vpc_blackholes):

    attachment_state = []
    for attachment in cloudwan_attachments['Attachments']:
        attachment_state.append({
            "Attachment Id": attachment['AttachmentId'],
            "Attachment Type": attachment['AttachmentType'],
            "Attachment State": attachment['State'],
        })

    healthy = 0
    degraded = 0
    down = 0
    for vpn in vpn_results:
        if vpn['Status'] == 'HEALTHY':
            healthy += 1
        elif vpn['Status'] == 'DEGRADED':
            degraded += 1
        else:
            down += 1

    print("=" * 50)
    print("\n  VPN HEALTH CHECK")
    print(f"\n  VPN:      {healthy} healthy, {degraded} degraded, {down} down")
    print("-" * 50)
    print("\n  CLOUDWAN ROUTES HEALTH CHECK")
    print(f"\n  {'Segment':<12}{'Edge Location':<20}{'Routes'}")
    print(f"  {'-'*12}{'-'*20}{'-'*8}")
    for r in cloudwan_routes:
        print(f"  {r['Segment Name']:<12}{r['Edge Location']:<20}{r['Route Count']}")
    print("\n  CLOUDWAN ATTACHMENT HEALTH CHECK")
    for attach in attachment_state:
        print(f"  {attach['Attachment Id']:<30}{attach['Attachment Type']:<20}{attach['Attachment State']:<20}")
    print("-" * 50)
    print("\n  VPC ROUTES HEALTH CHECK")
    print(f"  {len(vpc_blackholes)} blackhole routes found")
    for bh in vpc_blackholes:
        print(f"    {bh['RouteTableId']} → {bh['Destination']}")
    print("=" * 50)


def main():
    try:
        response = check_vpn()
        vpn_results = vpn_check_tunnel_status(response)
        cloudwan_routes = cloudwan_route_check()
        cloudwan_attachments = cloudwan_attachment_check()
        vpc_blackholes = vpc_routes_check()
        print_report(vpn_results, cloudwan_routes, cloudwan_attachments, vpc_blackholes)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

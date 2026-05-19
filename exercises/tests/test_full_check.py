from exercises.ex18_full_check import vpn_check_tunnel_status
from exercises.ex18_full_check import cloudwan_route_check

vpn_check = {
  "VpnConnections": [
    {
      "VpnConnectionId": "vpn-healthy111",
      "VgwTelemetry": [
        {"Status": "UP"},
        {"Status": "UP"}
      ]
    },
    {
      "VpnConnectionId": "vpn-down222",
      "VgwTelemetry": [
        {"Status": "DOWN"},
        {"Status": "DOWN"}
      ]
    },
    {
      "VpnConnectionId": "vpn-degraded333",
      "VgwTelemetry": [
        {"Status": "UP"},
        {"Status": "DOWN"}
      ]
    }
  ]
}

def test_vpn_check_tunnel_status():
    response = vpn_check_tunnel_status(vpn_check)
    assert response[0]['Status'] == 'HEALTHY'
    assert response[1]['Status'] == 'DOWN'
    assert response[2]['Status'] == 'DEGRADED'

def test_cloudwan_route_check():
    response = cloudwan_route_check()









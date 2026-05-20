from exercises.ex02_routes import get_all_routes


routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
]

def test_get_all_routes():
    assert len(get_all_routes(routes)) == 5
    assert type(get_all_routes(routes)) == list
    for route in get_all_routes(routes):
        if route["destination"] == "10.0.0.0/16":
            assert route["target"] == "local"
            assert route["state"] == "active"
        if route["destination"] == "172.16.0.0/16":
            assert route["target"] == "tgw-dead000"
            assert route["state"] == "blackhole"











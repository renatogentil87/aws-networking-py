routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
]


def get_all_routes(routes):
    if len(routes) == 0:
        return "No routes found"
    else:
        return routes


def get_blackhole_routes(routes):
    result = []
    for route in routes:
        if route.get('state') == "blackhole":
            result.append(route)
    return result


def get_active_routes(routes):
    result = []
    for route in routes:
        if route.get('state') == "active":
            result.append(route)
    return result


def count_blackholes(routes):
    return len(get_blackhole_routes(routes))


def main():
    print("All routes:")
    for route in get_all_routes(routes):
        print(f"  {route['destination']} → {route['target']} [{route['state']}]")

    print("\nBlackhole routes:")
    for route in get_blackhole_routes(routes):
        print(f"  {route['destination']} → {route['target']} [{route['state']}]")

    print("\nActive routes:")
    for route in get_active_routes(routes):
        print(f"  {route['destination']} → {route['target']} [{route['state']}]")

    print(f"\nFound {count_blackholes(routes)} blackhole routes")


if __name__ == "__main__":
    main()

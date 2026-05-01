routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
]


# `10.0.0.0/16 → local [active]`
def print_10_routes():
    for route in routes:
        print(route['destination'], "->", route['target'], route['state'])


def print_blackhole_routes():
    for route in routes:
        if route.get('state') == "blackhole":
            print (f"{route['destination']} -> {route['target']} -> {route['state']}")

def active_routes():
    for route in routes:
        if route.get('state') == "active":
           print(f"{route['destination']} -> {route['target']} -> {route['state']}")

def count_blackholes():
    blackhole = 0
    for route in routes:
        if route.get('state') == "blackhole":
            blackhole += 1

    print(f"Found {blackhole} blackhole routes")



def main():
    print_blackhole_routes()

if __name__ == "__main__":
    main()
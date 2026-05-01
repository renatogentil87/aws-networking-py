'''
Tasks:
- Take the routes list from 1.2
- Save it to `exercises/my_routes.json` using `json.dump()`
- Read it back using `json.load()`
- Print what you read to confirm it matches
- Run your `find_blackholes()` function on the loaded data
'''
import json

routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"}
]

def save_routes(routes):
    json.dump(routes, open("my_routes.json", "w"))

def load_routes():
    with open("my_routes.json") as f:
        return json.load(f)


def find_blackholes(routes):
    blackholes = []
    for route in routes:
        if route.get('state') == 'blackhole':
            blackholes.append(route)
    return blackholes

def compared_json():
    return load_routes() == routes


def main():
    save_routes(routes)
    loaded = load_routes()

    print('All Routes from json')
    for r in loaded:
        print(r['destination'], r['target'], r['state'])

    print('\nRunning find_blackholes function')
    for route in find_blackholes(loaded):
        print(route['destination'], route['target'], route['state'])

    print('\nChecking Json Routes with Existing Routes:')
    print(compared_json())

if __name__ == "__main__":
    main()


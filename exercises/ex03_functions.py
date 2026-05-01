'''
Create `exercises/ex03_functions.py`

Using the same route data from 1.2:
- Write a function `find_blackholes(routes)` that takes a list of routes and returns only the blackholes
- Write a function `find_active(routes)` that returns only active routes
- Call both functions and print the results

This is the most important exercise. If you understand functions, you understand the whole project.
'''

routes = [
    {"destination": "10.0.0.0/16", "target": "local", "state": "active"},
    {"destination": "0.0.0.0/0", "target": "igw-abc123", "state": "active"},
    {"destination": "172.16.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
    {"destination": "10.1.0.0/16", "target": "tgw-abc123", "state": "active"},
    {"destination": "10.99.0.0/16", "target": "tgw-dead000", "state": "blackhole"},
]


def find_blackholes(routes):
    blackholes = []
    for route in routes:
        if route.get('state') == 'blackhole':
            blackholes.append(route)
    return blackholes


def find_active(routes):
    active = []
    for route in routes:
        if route.get('state')=='active':
            active.append(route)
    return active

def main():
    print()
    print("Blackhole Routes:")
    for r in find_blackholes(routes):
        print(r['destination'], r['target'], r['state'])
    print()
    print("Active Routes:", end='\n')
    for r in find_active(routes):
        print(r['destination'], r['target'], r['state'])

if __name__ == '__main__':
    main()



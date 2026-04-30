"""
Tasks:
- Loop through the list and print each tunnel: `52.1.2.3: UP`
- Count how many are UP and how many are DOWN
- Print a summary: `2 UP, 2 DOWN`
"""

tunnels = [
    {"ip": "52.1.2.3", "status": "UP"},
    {"ip": "52.4.5.6", "status": "DOWN"},
    {"ip": "35.7.8.9", "status": "UP"},
    {"ip": "35.10.11.12", "status": "DOWN"},
]

def tunnels_up():
    results = []
    for ip['ip'], key['status'] in tunnels:
        results.append({ip ,  key})
    return results


def main():
    print(tunnels_up())

if __name__ == "__main__":
    main()
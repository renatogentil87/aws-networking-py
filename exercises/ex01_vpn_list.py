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


def main():
    up = 0
    down = 0
    for tunnel in tunnels:
        print(tunnel.get("ip"), tunnel.get("status"))
        if tunnel.get("status") == "UP":
            up += 1
        else:
            down += 1
    print("--"*24)
    print(up, "UP", down, "DOWN")


if __name__ == "__main__":
    main()
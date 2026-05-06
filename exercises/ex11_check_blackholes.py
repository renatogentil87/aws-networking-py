"""
Scenario: You collected VPC route tables yesterday. Now check if any routes went blackhole overnight.

Tasks:
- Read `outputs/vpc_routes.json` (or use the sample in `examples/sample_output.json`)
- Find all routes where state is "blackhole"
- Print: `BLACKHOLE: rtb-xxx — 10.99.0.0/16 → tgw-dead000`
- Accept `--input` argument for the JSON file path
"""

import json
import argparse


def check_blackholes(filepath):
    result = []
    try:
        with open(filepath) as f:
            routes = json.load(f)
            for state in routes:
                if state["State"] == "blackhole":
                    result.append({
                        "RouteTableId": state["RouteTableId"],
                        "Destination": state["Destination"],
                        "Target": state["Target"],
                        "State": state["State"],
                    })

                    print(f"BLACKHOLE: {state['RouteTableId']} - {state['Destination']} -> {state['Target']}")
        print("----" * 24)
        print("Total number of blackhole routes: ", len(result))

    except FileNotFoundError as e:
        print(f"File '{filepath}' not found!")
        return None

def main():
    parser = argparse.ArgumentParser(description="Check if any routes went blackhole overnight")
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    check_blackholes(args.input)

if __name__ == "__main__":
    main()
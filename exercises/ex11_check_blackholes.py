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

class Blackhole():
    def __init__(self):
        self.result = []

    def blackhole(self, filepath):
        try:
            with open (filepath) as f:
                routes = json.load(f)
                for state in routes:
                    if state["State"] == "blackhole":
                        self.result.append({
                            "RouteTableId": state["RouteTableId"],
                            "Destination": state["Destination"],
                            "Target": state["Target"],
                            "State": state["State"],
                        })

            return self.result

        except FileNotFoundError as e:
            print(f"File '{filepath}' not found!")

    def __str__(self):
        if not self.result:
            return "No blackhole routes found!"
        lines = []
        for state in self.result:
            lines.append(f"BLACKHOLE: {state['RouteTableId']} - {state['Destination']} -> {state['Target']}")
        lines.append("----" * 24)
        lines.append(f"Total number of blackholes: {len(self.result)}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check if any routes went blackhole overnight")
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    output = Blackhole()
    output.blackhole(args.input)
    print(output)

if __name__ == "__main__":
    main()
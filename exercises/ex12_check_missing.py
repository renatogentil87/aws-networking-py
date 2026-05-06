"""
Scenario: After a change window, you need to verify all expected routes are present.

Tasks:
- Define a list of expected CIDRs: `["10.0.0.0/16", "172.16.0.0/16", "10.1.0.0/16"]`
- Read your saved route tables
- For each route table, check if all expected CIDRs exist
- Print what's missing
- Accept `--input` and `--expected` (comma-separated CIDRs) arguments

"""
import json
import argparse


def expected_cidrs(expected_cidrs, input):
    try:
        routes = []
        with open(input) as f:
            json_data = json.load(f)
            for route in json_data:
                routes.append(route['Destination'])
        for dst in expected_cidrs:
            if dst not in routes:
                print(f"{dst} is not in the route table")
            else:
                print(f"{dst} in the route table")


    except FileNotFoundError:
        print(f"File '{input}' not found")
        return None

def main():
    args = argparse.ArgumentParser(description="Check if route is missing")
    args.add_argument("-i", "--input", required=True)
    args.add_argument("-e", "--expected", required=True)
    parsed_args = args.parse_args()

    expected_cidrs(parsed_args.expected.split(","), parsed_args.input)


if __name__ == "__main__":
    main()
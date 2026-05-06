"""
Scenario: You're about to apply a Cloud WAN policy change. You want to compare routes before and after.

Tasks:
- Read two JSON files: `--before` and `--after`
- Find routes that were added (in after but not before)
- Find routes that were removed (in before but not after)
- Print a diff report:
  ```
  ADDED:   192.168.10.0/24
  REMOVED: 172.16.0.0/12
  ```

This is the foundation of drift detection.
"""

import json
import argparse


def compare_routes(before_file, after_file):
    """Compare two route files and return added/removed routes."""
    with open(before_file) as f:
        before = json.load(f)
    with open(after_file) as f:
        after = json.load(f)

    before_routes = before["Routes"]
    after_routes = after["Routes"]

    added = [r for r in after_routes if r not in before_routes]
    removed = [r for r in before_routes if r not in after_routes]

    return added, removed


def print_diff(added, removed):
    """Print a formatted diff report."""
    for route in added:
        print(f"ADDED:   {route['DestinationCidrBlock']}")
    for route in removed:
        print(f"REMOVED: {route['DestinationCidrBlock']}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare CloudWAN routes before and after"
    )
    parser.add_argument("--before", required=True, help="Before JSON file")
    parser.add_argument("--after", required=True, help="After JSON file")
    args = parser.parse_args()

    try:
        added, removed = compare_routes(args.before, args.after)
        print_diff(added, removed)
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

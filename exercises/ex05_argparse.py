'''
Tasks:
- Accept `--region` and `--vpn-id` arguments
- Print: `Checking VPN vpn-xxx in region ca-central-1`
- Add `--output` argument (optional, default: `outputs/result.json`)

Run it: `python3 exercises/ex05_argparse.py --region ca-central-1 --vpn-id vpn-123`
'''
import argparse

def main():
    parser = argparse.ArgumentParser(description="Check VPN ")
    parser.add_argument("--vpn-id", required=True)
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--output", default="outputs/result.json")
    args = parser.parse_args()

    print(f"Checking VPN {args.vpn_id} in region {args.region}")



if __name__ == "__main__":
    main()
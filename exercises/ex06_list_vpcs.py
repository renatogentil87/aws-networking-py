'''
- Use boto3 to call `describe_vpcs()` in ca-central-1
- Print each VPC ID and CIDR block
- Add `--region` argument
'''
import boto3
import argparse


def describe_vpcs(region):
    client = boto3.client('ec2', region_name=region)
    response = client.describe_vpcs()
    return response


def main():
    parser = argparse.ArgumentParser(description='Print VPC ID and CIDR block')
    parser.add_argument('--region', required=True, help='AWS region', default='us-east-1')
    args = parser.parse_args()
    vpcs = describe_vpcs(args.region)

    for vpc in vpcs['Vpcs']:
        print(f"VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}")

if __name__ == '__main__':
    main()
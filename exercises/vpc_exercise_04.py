"""
  Exercise 4 — Build a lookup dict mapping every SubnetId to its VpcId.
  Expected output: {'subnet-1a': 'vpc-aaa', 'subnet-1b': 'vpc-aaa', ..., 'subnet-3a': 'vpc-ccc'}
"""
vpcs = [
    {
        "VpcId": "vpc-aaa",
        "CidrBlock": "10.0.0.0/16",
        "Subnets": [
            {"SubnetId": "subnet-1a", "CidrBlock": "10.0.1.0/24", "AvailabilityZone": "us-east-1a"},
            {"SubnetId": "subnet-1b", "CidrBlock": "10.0.2.0/24", "AvailabilityZone": "us-east-1b"},
            {"SubnetId": "subnet-1c", "CidrBlock": "10.0.3.0/24", "AvailabilityZone": "us-east-1c"}
        ]
    },
    {
        "VpcId": "vpc-bbb",
        "CidrBlock": "172.16.0.0/16",
        "Subnets": [
            {"SubnetId": "subnet-2a", "CidrBlock": "172.16.1.0/24", "AvailabilityZone": "us-east-1a"},
            {"SubnetId": "subnet-2b", "CidrBlock": "172.16.2.0/24", "AvailabilityZone": "us-east-1b"}
        ]
    },
    {
        "VpcId": "vpc-ccc",
        "CidrBlock": "192.168.0.0/16",
        "Subnets": [
            {"SubnetId": "subnet-3a", "CidrBlock": "192.168.1.0/24", "AvailabilityZone": "us-east-1a"}
        ]
    }
]

def map_subnets():
    result = {}
    for vpc in vpcs:
        for subnet in vpc["Subnets"]:
            result.update({subnet["SubnetId"]: vpc["VpcId"]})

    return result

def main():
    print(map_subnets())

if __name__ == "__main__":
    main()
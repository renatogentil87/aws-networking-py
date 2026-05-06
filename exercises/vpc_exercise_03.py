"""
 Exercise 3 — Inside: For each VPC, find subnets only in us-east-1a.

  Expected output:
  vpc-aaa: ['10.0.1.0/24']
  vpc-bbb: ['172.16.1.0/24']
  vpc-ccc: ['192.168.1.0/24']
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
            {"SubnetId": "subnet-2b", "CidrBlock": "172.16.2.0/24", "AvailabilityZone": "us-east-1a"}
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

def get_subnets():
    for vpc in vpcs:
        output = []
        for subnet in vpc["Subnets"]:
            if subnet['AvailabilityZone'] == 'us-east-1a':
                output.append(subnet['CidrBlock'])
        print(vpc["VpcId"],":", output)

def main():
    get_subnets()

if __name__ == "__main__":
    main()
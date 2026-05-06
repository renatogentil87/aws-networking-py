"""
Exercise 5 — Both: Collect all subnets globally, but also print per-VPC summary

  Expected output:
  vpc-aaa: ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24']
  vpc-bbb: ['172.16.1.0/24', '172.16.2.0/24']
  vpc-ccc: ['192.168.1.0/24']
  All subnets: ['10.0.1.0/24', '10.0.2.0/24', ..., '192.168.1.0/24']

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

def subnet_summary():
    all_subnets = []
    for vpc in vpcs:
        subnets = []
        vpcid = vpc['VpcId']
        for subnet in vpc['Subnets']:
            subnets.append(subnet['CidrBlock'])
            all_subnets.append(subnet['CidrBlock'])
        print(f"{vpcid}: {subnets}")
    print(f"All subnets: {all_subnets}")



def main():
    subnet_summary()

if __name__=="__main__":
    main()
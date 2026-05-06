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


#  Expected output: ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24', '172.16.1.0/24', ...]


def get_subnets():
    subnets = []
    for vpc in vpcs:
        for subnet in vpc['Subnets']:
            subnets.append(subnet['CidrBlock'])

    return subnets

def main():
    print(get_subnets())

if __name__ == "__main__":
    main()
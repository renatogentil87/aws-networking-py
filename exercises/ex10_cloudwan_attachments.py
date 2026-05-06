"""
Scenario: You need to verify all attachments are in the correct segment.

Tasks:
- Use `list_attachments()` API
- Print: attachment ID, type, segment, state
- Save to JSON

- global network id: global-network-007efcd46173a27a1
- core network id: core-network-0d91631a180884713
"""

import json
import boto3
import argparse
from botocore.exceptions import ClientError


def list_attachments(core_network_id):
    try:
        client = boto3.client('networkmanager')
        response = client.list_attachments(
            CoreNetworkId= core_network_id,
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

def main():
    parser = argparse.ArgumentParser(description = "List CloudWAN Attachments" )
    parser.add_argument("--core-network-id", required=True, help = "The ID of the CloudWAN Network Manager Core Network")
    args = parser.parse_args()

    result =[]
    response = list_attachments(args.core_network_id)
    if response is None:
        print("Failed to fetch CloudWAN Attachments")
        return None
    else:
        for attachment in response['Attachments']:
            result.append( {
                'AttachmentId': attachment['AttachmentId'],
                'AttachmentType': attachment['AttachmentType'],
                'State': attachment['State'],
                'Segment': attachment['SegmentName']
            })

    try:
        with open('cloudwan_attachments.json', 'w') as f:
            json.dump(result, f, indent=4)
    except IOError:
        print(f"IO Error")
        return None

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
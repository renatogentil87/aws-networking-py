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

class CloudWANAttachments():

    def __init__(self, core_network_id ):
        self.core_network_id = core_network_id
        self.results = []
        try:
            self.client = boto3.client('networkmanager')
            self.response = self.client.list_attachments(
                CoreNetworkId= self.core_network_id,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    def __str__(self):
        return json.dumps(self.results, indent=4, default=str)

    def attachments(self):
        if self.response is None:
            print("Failed to fetch CloudWAN Attachments")
            return None
        else:
            for attachment in self.response['Attachments']:
                self.results.append( {
                    'AttachmentId': attachment['AttachmentId'],
                    'AttachmentType': attachment['AttachmentType'],
                    'State': attachment['State'],
                    'Segment': attachment['SegmentName']
                })

        try:
            with open('cloudwan_attachments.json', 'w') as f:
                json.dump(self.results, f, indent=4)
        except IOError:
            print(f"IO Error")
            return None

        return json.dumps(self.results, indent=4)



def main():
    parser = argparse.ArgumentParser(description = "List CloudWAN Attachments" )
    parser.add_argument("--core-network-id", required=True, help = "The ID of the CloudWAN Network Manager Core Network")
    args = parser.parse_args()

    filtered_response = CloudWANAttachments(args.core_network_id)
    filtered_response.attachments()
    print(filtered_response)




if __name__ == "__main__":
    main()
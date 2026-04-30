"""List Cloud WAN attachments."""

import argparse
import json
import boto3


def get_attachments(core_network_id, region):
    client = boto3.client("networkmanager", region_name=region)
    response = client.list_attachments(CoreNetworkId=core_network_id)
    return response.get("Attachments", [])


def main():
    parser = argparse.ArgumentParser(description="List Cloud WAN attachments")
    parser.add_argument("--core-network-id", required=True)
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()

    attachments = get_attachments(args.core_network_id, args.region)

    if not attachments:
        print("No attachments found.")
        return

    # Print
    print(f"\n{'Attachment ID':<35} {'Type':<20} {'Segment':<15} {'State':<12}")
    print("-" * 82)
    for a in attachments:
        print(f"{a['AttachmentId']:<35} {a['AttachmentType']:<20} {a.get('SegmentName', 'N/A'):<15} {a['State']:<12}")

    # Save
    with open("outputs/cloudwan_attachments.json", "w") as f:
        json.dump(attachments, f, indent=2)
    print(f"\nSaved {len(attachments)} attachments to outputs/cloudwan_attachments.json")


if __name__ == "__main__":
    main()

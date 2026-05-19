# How To Summarize Routes from VPCs to On-Premises Using AWS Cloud WAN Advanced Routing Policies

## Overview

When building multi-region hybrid networks on AWS, controlling route propagation is critical. Without proper route management, on-premises routers end up with bloated route tables full of granular VPC prefixes they don't need. AWS Cloud WAN's Advanced Routing Policy solves this by enabling route summarization directly within the Cloud WAN policy document.

In this post, we walk through a real-world scenario where multiple VPC prefixes shared across segments are summarized into a single /16 before being advertised outbound to on-premises over an IPsec Site-to-Site VPN.

## What is Advanced Routing Policy in Cloud WAN

AWS Cloud WAN Routing Policy gives you fine-grained control over dynamic route propagation across your global network. It follows a classical match-action model where you define routing policies composed of ordered rules. Each rule specifies a match condition (prefix, prefix list, BGP community, ASN, or MED) and an action (allow, drop, summarize, set local preference, modify AS-PATH, or manipulate communities).

Policies can be associated at three distribution points:

- **On attachments** — via routing policy labels and attachment routing policy rules
- **Across segments** — via segment sharing actions
- **Across regions** — via Core Network Edge (CNE) to CNE peering

This feature requires policy version `2025.11` and is available at no additional charge in all regions where Cloud WAN operates.

## Scenario — Summarizing VPC Prefixes Outbound to On-Premises

We have a Cloud WAN core network spanning two regions (ca-central-1 and eu-west-2) with four segments:

- **fullmesh** — VPC A (172.16.10.0/24) and VPC B (172.16.20.0/24). Full connectivity between them and shared routes with hybrid and shared segments.
- **shared** — Shared-services VPC (172.16.30.0/24). Routes shared with fullmesh and hybrid.
- **isolated** — VPC C (172.16.40.0/24). No route sharing with other segments.
- **hybrid** — On-premises connectivity via IPsec Site-to-Site VPN. Routes shared with fullmesh and shared segments.

Without routing policy, on-premises learns each individual /24 prefix. Our goal is to summarize these into a single `172.16.0.0/16` route advertised outbound to the VPN.

## On-Premises Routing Table — Before Summarization

Before applying the routing policy, the on-premises router learns every individual VPC prefix via BGP over the VPN tunnel:

```
Router# show ip route bgp

     172.16.0.0/16 is variably subnetted, 3 subnets
B       172.16.10.0/24 [20/0] via 169.254.131.205, 00:45:12
B       172.16.20.0/24 [20/0] via 169.254.131.205, 00:45:12
B       172.16.30.0/24 [20/0] via 169.254.131.205, 00:45:12
```

Three individual /24 routes in the routing table. As VPCs are added, this table grows — potentially to hundreds of entries in large environments.

## Implementation

The implementation involves three components in the Cloud WAN policy document and one API call to bind the policy to the VPN attachment.

### Step 1 — Define the Routing Policy

In the `routing-policies` section, create an outbound policy that matches the specific VPC prefixes and summarizes them:

```json
{
  "routing-policies": [
    {
      "routing-policy-name": "outboundSummarizeToVpn",
      "routing-policy-description": "Summarize VPC prefixes outbound to VPN on hybrid segment",
      "routing-policy-direction": "outbound",
      "routing-policy-number": 100,
      "routing-policy-rules": [
        {
          "rule-number": 100,
          "rule-definition": {
            "match-conditions": [
              { "type": "prefix-equals", "value": "172.16.10.0/24" },
              { "type": "prefix-equals", "value": "172.16.20.0/24" },
              { "type": "prefix-equals", "value": "172.16.30.0/24" }
            ],
            "condition-logic": "or",
            "action": {
              "type": "summarize",
              "value": "172.16.0.0/16"
            }
          }
        }
      ]
    }
  ]
}
```

This rule says: if any route matches one of these three /24 prefixes, replace them with a single `172.16.0.0/16` summary route in the outbound direction.

### Step 2 — Create an Attachment Routing Policy Rule

In the `attachment-routing-policy-rules` section, create a rule that maps a routing policy label to the policy defined in Step 1:

```json
{
  "attachment-routing-policy-rules": [
    {
      "rule-number": 100,
      "description": "Associate summarization policy to hybrid VPN attachments",
      "conditions": [
        { "type": "routing-policy-label", "value": "hybridVpnSummarization" }
      ],
      "action": {
        "associate-routing-policies": ["outboundSummarizeToVpn"]
      }
    }
  ]
}
```

Any attachment carrying the label `hybridVpnSummarization` gets the summarization policy applied.

### Step 3 — Configure Segment Sharing

The `segment-actions` section defines route sharing between segments:

```json
{
  "segment-actions": [
    { "action": "share", "mode": "attachment-route", "segment": "fullmesh", "share-with": ["shared", "hybrid"] },
    { "action": "share", "mode": "attachment-route", "segment": "hybrid", "share-with": ["fullmesh", "shared"] },
    { "action": "share", "mode": "attachment-route", "segment": "shared", "share-with": ["fullmesh", "hybrid"] }
  ]
}
```

The isolated segment is absent from all `share-with` arrays — VPC C remains unreachable from other segments by design.

### Step 4 — Assign the Routing Policy Label to the VPN Attachment

This step activates the policy. The routing policy label is assigned directly to the VPN attachment using the AWS API:

```bash
aws networkmanager create-attachment-routing-policy-label \
  --attachment-id attachment-xxxxxxxxxxxx \
  --routing-policy-label "hybridVpnSummarization"
```

This separation is intentional. Segment association uses tags (managed by attachment owners), while routing policy association uses labels (managed by the core network owner). This gives the network team control over routing behavior without depending on how attachments are tagged.

## On-Premises Routing Table — After Summarization

After applying the routing policy, the on-premises router receives a single summary route instead of three individual prefixes:

```
Router# show ip route bgp

B    172.16.0.0/16 [20/0] via 169.254.131.205, 00:02:37
```

Three /24 routes replaced by one /16 summary. The on-premises routing table is clean, scalable, and unaffected by future VPC additions within the `172.16.0.0/16` range.

### Before vs After Comparison

| Metric | Before | After |
|--------|--------|-------|
| Routes learned via BGP | 3 (growing with each VPC) | 1 (static) |
| Routing table entries | 172.16.10.0/24, 172.16.20.0/24, 172.16.30.0/24 | 172.16.0.0/16 |
| Impact of adding new VPC | New route appears on-prem | No change on-prem |
| On-prem router memory | Grows linearly | Constant |

## Pro Tip — prefix-equals vs prefix-in-cidr

When writing match conditions, choose carefully:

- **prefix-equals** — matches the exact prefix (e.g., `172.16.10.0/24` matches only `172.16.10.0/24`)
- **prefix-in-cidr** — matches only strict subsets with longer prefix lengths (e.g., `172.16.0.0/16` would match `172.16.10.0/24` but NOT `172.16.0.0/16` itself)

If your VPCs advertise exact /24 routes, use `prefix-equals`. If you need both the exact prefix and its subnets, combine both match types.

## Conclusion

AWS Cloud WAN's Advanced Routing Policy transforms how network engineers manage route propagation in complex hybrid environments. By applying route summarization at the attachment distribution point, we reduced three granular VPC prefixes to a single summary route advertised to on-premises — keeping router tables clean and preventing unnecessary route proliferation.

The real-world impact is clear: the on-premises router went from learning individual /24 prefixes (that grow with every VPC addition) to a single stable /16 summary that never changes. This reduces router memory consumption, simplifies troubleshooting, and eliminates the operational burden of updating on-premises route filters every time a new VPC is deployed.

This approach scales elegantly — as you add VPCs within the `172.16.0.0/16` range, you simply add their prefix to the match conditions without changing what on-premises sees.

**Important:** You must use policy version `"version": "2025.11"` to enable routing policies in your core network policy.

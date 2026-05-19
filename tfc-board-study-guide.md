highly available dx connection on DX


# AWS Networking TFC Board - Quick Reference

---

## Direct Connect (DX)

- Dedicated private connection from on-prem to AWS
- VIF types: Private (→ VGW), Transit (→ DXGW → TGW/CloudWAN), Public (→ AWS public services)
- Transit VIF: max 4 per dedicated connection
- DX Gateway: max 6 TGW associations OR max 20 VGW associations (not both)
- DX Gateway can associate with TGW OR CloudWAN OR VGW (mutually exclusive per DXGW)
- Maximum resilience: 2 locations × 2 connections × 2 customer routers = 99.99% SLA
- MACsec: L2 encryption (AES-256) on the physical fiber. Prevents sniffing in colo. Line-rate, no throughput penalty. 10G/100G dedicated only.

### DX Dedicated vs Hosted

| | Dedicated | Hosted |
|---|---|---|
| Who owns AWS port | Customer | Partner |
| Cross-connect | Customer arranges | Partner handles |
| Speeds | 1G, 10G, 100G | 50M to 10G |
| VIFs | Up to 50 private/public + 4 transit | 1 VIF only |
| MACsec | Yes (10G/100G) | No |
| Must be in colo? | Yes | No |
| Lead time | Weeks | Minutes/hours |

- **Dedicated**: customer router ←fiber cross-connect→ AWS DX router (same colo)
- **Hosted**: customer router → partner network → partner's DX port → AWS DX router

### DX Route Manipulation

**BGP route preference order (private/transit VIF):**
1. Longest prefix match
2. Local preference (BGP communities 7224:7100/7200/7300)
3. AS-PATH length
4. MED (lowest wins)

**BGP communities (7224:7100/7200/7300):**
- Only work on private/transit VIFs (NOT VPN)
- Use when: multiple VIFs on the same DXGW, prefer one over another
- 7300 = high, 7200 = medium, 7100 = low

**AS-PATH prepend:**
- On-prem prepends on backup DX to make it look longer
- TGW/CloudWAN prefers shorter AS-PATH

**Allowed prefixes on DXGW-TGW association:**
- Controls what AWS advertises to on-prem (acts as summary)
- Up to 200 prefixes. Use to reduce route count to on-prem.

### DX Pricing
- Port hour (varies by speed)
- Data transfer OUT per GB (varies by region)
- Data transfer IN — free
- No per-GB processing fee

---

## Transit Gateway (TGW)

- Regional hub-and-spoke router. Connects VPCs, VPNs, DX, peering.
- Segmentation via route tables (associate + propagate)
- No route filtering (all-or-nothing propagation)
- Blackhole routes for explicit blocking
- Appliance mode for stateful firewall attachments
- ECMP across VPN tunnels only (not DX + VPN)
- Cross-region peering: static routes only, no propagation
- 50 Gbps per VPC attachment, 10K routes per route table
- Does NOT evaluate BGP communities

### TGW Route Preference Order

1. Longest prefix match
2. Static > propagated
3. **DX > VPN** (built-in)
4. Shortest AS-PATH
5. Lowest MED

### TGW Route Manipulation

- Cannot filter routes (no routing policies like CloudWAN)
- Cannot prepend or manipulate BGP attributes
- Traffic engineering relies on: on-prem AS-PATH prepend, MED, longest prefix match
- If traffic shifts to VPN when DX healthy: prepend on VPN from on-prem + enable BFD on DX

### TGW Pricing
- Per attachment per hour
- Per GB data processed
- Peering: data transfer charges cross-region

---

## AWS Cloud WAN

- Global policy-driven network. Replaces TGW + peering + manual routes.
- Segments = global routing domains. Sharing = explicit, directional.
- `isolate-attachments`: blocks within segment, sharing from other segments still works
- `require-attachment-acceptance`: approval gate for new attachments
- Network Function Groups: service insertion (single-hop / dual-hop)
- `associate-routing-policy`: filters CNE-to-CNE within a segment (cross-region blocking)
- Supports DX Gateway natively (no TGW needed as intermediary)
- VPC attachments: only support inbound route filtering (no outbound manipulation)
- No BGP community support on DX and TGW peering attachments
- `list-core-network-routing-information` API shows routes BEFORE policy application

### CloudWAN Routing Policies

**Inbound (routes entering CloudWAN from attachment) = "my decision":**

| Action | Use case |
|---|---|
| `drop/allow` | Block or permit specific routes from entering |
| `set-local-preference` | Prefer one attachment globally (higher LP wins) |

**Outbound (routes leaving CloudWAN to attachment or via segment share) = "influencing their decision":**

| Action | Use case |
|---|---|
| `drop/allow` | Block routes from being shared/advertised |
| `summarize` | Aggregate prefixes before advertising to on-prem |
| `prepend-asn-list` | Make a path look longer (per-region preference on segment share, or influence on-prem) |
| `set-med` | Influence on-prem path selection (lower = preferred) |
| `add-community` | Tag routes for on-prem to act on |
| `remove-community` | Strip internal tags before advertising |

### CloudWAN Path Preference

| Goal | Mechanism | Direction |
|---|---|---|
| All regions prefer one DX globally | `set-local-preference` | Inbound on attachment |
| Per-region DX preference | `prepend-asn-list` on segment sharing | Outbound on share action |
| On-prem prefers one path | `prepend-asn-list` on attachment | Outbound to on-prem |
| On-prem prefers one path (alt) | `set-med` on attachment | Outbound to on-prem |

### Where prepend-asn-list works

| Scenario | Works? |
|---|---|
| Outbound to on-prem (DX/VPN attachment) | ✓ On-prem sees longer AS-PATH |
| On segment sharing (hybrid → prod) | ✓ Per-region DXGW preference |
| CNE-to-CNE (cross-region within segment) | ✗ Not supported |

### Filtering on Segment Sharing

Apply `routing-policy-names` on share actions to control which routes are shared:
- `allow` specific prefix (low rule number) → terminal
- `drop` everything else (higher rule number)
- Can match by: prefix, prefix-list, BGP community

### Single-Hop vs Dual-Hop Inspection

| Mode | Where inspection happens | Use case |
|---|---|---|
| Single-hop | Once at one point | East-west between segments, hybrid traffic |
| Dual-hop | At source CNE AND destination CNE | Cross-region, need inspection at both ends |

### CloudWAN Pricing
- Per attachment per hour
- Per GB data processed (per edge location)
- Per peering per hour (CNE-to-CNE)

---

## Site-to-Site VPN

- Encrypted IPsec tunnel (2 tunnels per connection for HA)
- BGP or static routing. Supports IKEv1/IKEv2.
- Per tunnel: ~1.25 Gbps max. With ECMP on TGW: up to 50 Gbps aggregate.
- Accelerated VPN: uses Global Accelerator for better performance
- Private IP VPN: over transit VIF (fully private, no public endpoints)
- BGP communities NOT supported on VPN

### VPN Route Manipulation

| Direction | Mechanism |
|---|---|
| AWS → on-prem | AS-PATH prepend on backup (on-prem does this) |
| On-prem → AWS | Local preference on on-prem router |

### VPN Pricing
- Per VPN connection per hour
- Accelerated VPN: additional per-hour + data transfer
- On TGW: also pay TGW attachment + per-GB processing

---

## AWS Network Firewall

- Managed stateful firewall (L3-7), powered by Suricata
- Stateless rules: 5-tuple, fast path
- Stateful rules: connection tracking, IPS/IDS
- Domain filtering (FQDN allow/deny)
- TLS/SNI inspection + full TLS decryption
- Always enable appliance mode (prevents asymmetric routing)

### Simple rules vs Suricata rules

| Simple rules | Suricata rules |
|---|---|
| IP/port/protocol, domain lists | Everything simple does PLUS: |
| No payload inspection | Deep packet inspection, HTTP header/URI matching |
| No regex | PCRE regex, byte-level matching |
| No file detection | File type detection, thresholding |

### Firewall VPC Split Routing

```
0.0.0.0/0         → NAT Gateway (internet egress)
10.0.0.0/8        → TGW (on-prem, post-inspection)
192.168.0.0/16    → TGW (on-prem, post-inspection)
```

Missing on-prem routes in firewall VPC = blackhole.

### Network Firewall Pricing
- Firewall endpoint per hour (per AZ)
- Traffic processed per GB
- TLS inspection per GB (additional)

---

## VPC Lattice

- Application-layer (L7) service-to-service networking
- No VPC peering or TGW needed — Lattice provides connectivity
- Works with overlapping CIDRs
- IAM-based access control
- Use for: service mesh (many services ↔ many services)
- NOT for: arbitrary TCP, full network connectivity

### VPC Lattice Pricing
- Per service per hour
- Per request (HTTP/gRPC)
- Per GB data processed

---

## Virtual Private Gateway (VGW)

- VPN/DX termination for a single VPC (legacy)
- No transitive routing, no segmentation
- Max 1 per VPC. Free.
- Use only for: single VPC with simple VPN or DX

---

## Other Key Concepts

### GENEVE Protocol
- Tunneling protocol used by **GWLB** and **TGW Connect** (SD-WAN)
- GWLB encapsulates original packet in GENEVE header → appliance inspects → sends back. Preserves original src/dst IPs.
- UDP port 6081

### Gateway Load Balancer (GWLB)

- Used for third-party firewalls (Palo Alto, Fortinet, Check Point) in AWS
- GENEVE encapsulation: preserves original src/dst IPs — no NAT, firewall sees real traffic
- 5-tuple hashing: session stickiness — same flow always hits same firewall instance
- Health checks: failed instance detected, new flows rerouted to healthy targets
- Firewall must support GENEVE decapsulation
- CloudWAN integration: same NFG + `send-via` — works identically to Network Firewall from CloudWAN's perspective
- Traffic path: VPC → CloudWAN → GWLB endpoint → firewall instance → GWLB → CloudWAN → destination

**GWLB vs Network Firewall:**

| | Network Firewall | GWLB + Third-Party |
|---|---|---|
| Management | AWS manages scaling | You manage instances + autoscaling |
| Rules | Suricata + simple rules | Vendor-specific (Palo Alto, etc.) |
| Ops overhead | Low | High |
| Existing licenses | N/A | Can reuse existing licenses |
| Threat intel | AWS managed rule groups | Vendor feeds |
| CloudWAN integration | Same (NFG + send-via) | Same (NFG + send-via) |

### Gateway Endpoint vs Interface Endpoint

| | Gateway Endpoint | Interface Endpoint |
|---|---|---|
| How it works | Prefix list in route table | ENI with private IP |
| Services | S3, DynamoDB only | 100+ services |
| Cost | Free | Per hour per AZ + per GB |
| On-prem access | ✗ No (VPC-local only) | ✓ Yes (DNS resolvable) |

### Asymmetric Routing & Appliance Mode
- Symptom: Firewall sees SYN, drops SYN-ACK
- Cause: Multi-AZ, flow split across AZs
- Fix: Appliance mode. Always. No exceptions.

### Stable Public IP for Egress
- App VPC → TGW → Firewall VPC (NFW → NAT GW with EIP) → IGW → SaaS
- EIP = stable IP for third-party whitelisting

### TGW to CloudWAN Migration
- `replace-route` is an **EC2 VPC API** — atomic, per-VPC, reversible
- Pre-stage CloudWAN attachments while TGW active
- Both coexist simultaneously. Migrate VPC by VPC.

---

## DX Traffic Engineering Mental Model

| Scenario | Where decision is made | Mechanism |
|---|---|---|
| Multiple VIFs → same DXGW | DX Gateway | BGP communities (7224:7100/7200/7300) |
| Multiple DXGWs → CloudWAN | CloudWAN | `set-local-preference` (global) or `prepend-asn-list` (per-region) |
| Multiple DXGWs → TGW | TGW | AS-PATH prepend (on-prem, no per-region control) |
| DX + VPN → TGW | TGW | DX wins built-in. Prepend on VPN for guarantee. |
| DX + VPN → CloudWAN | CloudWAN | `set-local-preference` inbound (higher on DX) |

---

## Architecture Decision Guide

| Scenario | Recommended |
|----------|-------------|
| 2-3 VPCs, simple connectivity | VPC Peering |
| 10+ VPCs, single region | TGW |
| Multi-region, policy-driven | Cloud WAN |
| On-prem, consistent latency, high bandwidth | Direct Connect |
| On-prem, quick setup, encrypted | Site-to-Site VPN |
| Encrypted over DX | MACsec (10G/100G) or Private IP VPN |
| Microservice mesh across accounts | VPC Lattice |
| One service exposed to many consumers | PrivateLink |
| Centralized egress inspection | Network Firewall + TGW/CloudWAN |
| Tenant isolation (50 VPCs, no cross-talk) | TGW per-tenant route tables |
| Single VPC, simple VPN | VGW |

---

## Questions to Practice

1. "200 VPCs across 4 regions, centralized inspection. How to minimize latency?"
2. "Two DX connections, same prefix. How to prefer one per region with CloudWAN?"
3. "50 tenant VPCs, must never talk to each other. TGW or CloudWAN?"
4. "Migrating from TGW to CloudWAN. Zero-downtime approach?"
5. "How to achieve 99.99% SLA on Direct Connect?"
6. "Filter dangerous routes from on-prem before entering cloud. How?"
7. "VPC Lattice vs PrivateLink — when to use which?"
8. "Firewall drops return traffic after enabling inspection. Why?"
9. "100TB/month over DX. Cost implications of TGW in the path?"
10. "VPN as backup for DX. How to ensure DX always preferred?"

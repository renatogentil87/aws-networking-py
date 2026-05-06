"""
Exercise 17: CloudWAN Route Summarization Policy Builder

Scenario:
Your Cloud WAN advertises individual VPC prefixes to on-premises via VPN.
The on-prem router's routing table is getting bloated. You need to summarize
multiple specific prefixes into a single aggregate before advertising outbound.

Your current outbound policy summarizes:
  172.16.0.0/16 + 172.18.0.0/16 + 172.22.0.0/16 → 172.16.0.0/12

But now the business wants you to:
1. Add EU prefixes to the summarization (10.10.0.0/16, 10.20.0.0/16, 10.40.0.0/16 → 10.0.0.0/8)
2. Keep the existing Canada summarization
3. Generate the updated CloudWAN routing policy JSON

Tasks:
1. Read the current policy from `outputs/cloudwan_policy_current.json`
2. Parse the existing routing-policies section
3. Add a new summarization rule for EU prefixes (rule-number 200):
   - Match: 10.10.0.0/16, 10.20.0.0/16, 10.40.0.0/16
   - Action: summarize to 10.0.0.0/8
   - Direction: outbound
4. Write the updated policy to `outputs/cloudwan_policy_updated.json`
5. Print a before/after comparison showing:
   ```
   BEFORE: 3 prefixes advertised to VPN (172.16/18/22)
   AFTER:  2 summary routes advertised (172.16.0.0/12, 10.0.0.0/8)
   
   Rule 100: 172.16.0.0/16, 172.18.0.0/16, 172.22.0.0/16 → 172.16.0.0/12
   Rule 200: 10.10.0.0/16, 10.20.0.0/16, 10.40.0.0/16 → 10.0.0.0/8
   ```

Bonus:
- Validate that the summary prefix actually covers all the specific prefixes
  (e.g., 10.10.0.0/16 is within 10.0.0.0/8)
- Use the `ipaddress` module to verify containment

Hints:
- Look at the structure of routing-policy-rules in the current policy
- Each rule has match-conditions (prefix-equals) and an action (summarize)
- The condition-logic should be "or" (match ANY of the prefixes)
"""

import json


def load_policy(file):
    """Load current CloudWAN policy JSON."""
    pass


def build_summarization_rule(rule_number, prefixes, summary_prefix):
    """Build a routing policy rule that summarizes multiple prefixes into one."""
    pass


def validate_summarization(prefixes, summary_prefix):
    """Verify all prefixes are contained within the summary prefix."""
    pass


def update_policy(policy, new_rules):
    """Add new summarization rules to the routing policy."""
    pass


def print_summary_comparison(original_rules, updated_rules):
    """Print before/after comparison of route advertisements."""
    pass


def main():
    pass


if __name__ == "__main__":
    main()

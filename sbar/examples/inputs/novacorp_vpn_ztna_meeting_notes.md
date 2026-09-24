# NovaCorp Architecture Working Session - Remote Access Future State

**FICTITIOUS DEMO CONTENT - COSAC 2026.** NovaCorp, all people, systems, vendors, and figures below are invented for demonstration purposes.

**Date:** 2026-09-15
**Meeting:** Architecture Working Session (not a decision forum)
**Attendees:** Enterprise Security Architect (facilitator), Director of Infrastructure, Network Operations Lead, Identity and Access Management Lead, IT Service Desk Manager, Finance Business Partner, Travel and Mobility Program Manager
**Notes taken by:** Security Architecture team (raw notes, lightly cleaned)

---

## Raw notes

- Kicked off 5 min late - room double-booked again. Facilities to fix the booking calendar (not our problem).
- Architect opened: purpose today is to frame the remote access decision for the CIO staff meeting on **2026-10-06**. Nothing gets decided today.

### Current state

- Remote access runs on **CorvusGate VPN** - two HA appliance pairs, one in the Phoenix DC, one in the Frankfurt DC.
- CorvusGate confirmed in writing (letter dated 2026-08-28) that the appliances reach **end of support on 2027-03-31**. No extended support option. No more security patches after that date.
- Last quarter: critical firmware CVE on CorvusGate. Emergency patch caused a **6-hour remote access outage** for EMEA users on 2026-06-11.
- **4,200** remote-capable users. About **1,100** are frequent travelers (Travel program estimate).
- VPN is full-tunnel, network-level access. Once connected, a user can reach **14 internal subnets**. Internal Audit finding **IA-2026-07** (issued 2026-07-22) rated this "High - excessive network access for remote users." Remediation plan due to Audit by **2026-12-31**.
- Service Desk: VPN issues = **38%** of all remote access tickets, roughly **310 tickets/month**. Top complaints: hotel Wi-Fi captive portals, slow reconnect after sleep, split-DNS problems.

### Applications

- **212** internal applications are only reachable over VPN today.
- Network Ops traffic analysis: the top **40** applications carry about **85%** of remote traffic. Almost all are web or HTTPS.
- About **25** legacy apps use thick clients or non-HTTP protocols (SMB file shares, a couple of SSH-based admin tools, one old ERP client). These will be hard to put behind ZTNA quickly.
- OT engineering remote access to fab tooling goes through a separate jump host process today. **Out of scope** for this decision - OT team has its own roadmap.

### Identity and device readiness

- IdP with MFA enforced for **100%** of workforce accounts.
- MDM device posture reporting covers **92%** of managed laptops. The other 8% are mostly older Macs in R&D.
- About **600** contractors use unmanaged personal devices. Today they get the same VPN access as employees (IAM Lead flagged this as a concern).

### Options discussed

- **Option A - Like-for-like VPN refresh.** Replace CorvusGate with a current VPN appliance. Estimated **$420K capex** plus ~$60K/yr support. Lowest change for users and Network Ops. Does **not** fix audit finding IA-2026-07 by itself - still network-level access.
- **Option B - Full cloud-delivered ZTNA.** App-centric access, identity + device posture per app, no network-level access. Estimated **$1.35M over 3 years** (subscription). Fixes the audit finding. Risk: the 25 legacy apps may not work on day one; cutover before 2027-03-31 is aggressive.
- **Option C - Phased hybrid.** Move the top 40 apps (85% of traffic) to ZTNA first. Keep a small, restricted VPN enclave for the legacy apps only, limited to named users, for up to **18 months** while legacy apps are remediated or retired. Estimated **$1.1M over 3 years** plus a small VPN footprint (~$90K). Addresses most of the audit finding, needs a documented exception for the residual VPN.

### Discussion

- Director of Infrastructure seemed positive on Option C. Said "this feels like the sensible path" - but also said he needs to see the numbers side by side before he supports anything.
- Network Ops Lead worried about skills: team has deep VPN/firewall experience, very little ZTNA. Asked for vendor-led training in any ZTNA option.
- Finance: **FY27 opex budget for a subscription is not confirmed.** CFO office wants a 3-year TCO comparison of A vs B vs C before CIO staff meeting. Finance can turn it around in ~1 week if architecture sends inputs by 2026-09-25.
- A ZTNA vendor told us in a sales call that customers see "up to 40% fewer remote access tickets." Nobody has validated this. Service Desk Manager wants to measure it in a pilot rather than trust it.
- Procurement lead time for either new platform is roughly **16 weeks**. If we don't decide on 2026-10-06, a pilot in Q4 2026 is unlikely and the 2027-03-31 end-of-support date gets very tight.
- Pilot idea: **200 users** (mix of travelers and IT staff) on ZTNA in Q4 2026.
- Travel and Mobility PM asked: what happens for travelers in restricted regions (some countries limit encrypted tunnels / certain cloud services)? **No one had an answer.** Needs follow-up with Legal/Trade Compliance.
- IAM Lead: whatever we pick, contractors on unmanaged devices should get browser-only access to specific apps, not network access. General agreement, but not formally decided.
- Side topic: team lunch next Thursday, pizza vs tacos. Tacos won.

### Action items

1. Security Architecture - send A/B/C cost inputs to Finance by 2026-09-25.
2. Security Architecture - prepare a decision brief for CIO staff meeting 2026-10-06.
3. Travel PM - raise restricted-region question with Legal/Trade Compliance.
4. Network Ops - list the 25 legacy apps with owners and protocol details.

**Status:** No decision made. Nothing approved. Recommendation still to be formed.

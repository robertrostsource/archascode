# [SBAR] Remote Access Future State - VPN to ZTNA - 2026-09-23

**Repository Location:** Architecture > Solution Architecture > SBAR
**Labels:** sbar, architecture, remote-access, network-security, zero-trust, decision-needed, adr-recommended
**ADR Need:** Yes - recommended via the ADR Agent

## BLUF

- **Decision needed:** Select the remote access future state at the CIO staff meeting on 2026-10-06.
- **Recommendation:** Option C, phased hybrid - Zero Trust Network Access (ZTNA) for the top 40 applications, plus a restricted, time-bound VPN enclave for legacy applications.
- **Primary impact:** CorvusGate VPN reaches end of support on 2027-03-31. With a 16-week procurement lead time, any later decision puts the cutover and audit remediation at risk.

## Situation

NovaCorp's CorvusGate VPN appliances lose vendor support, including security patches, on 2027-03-31, with no extended support option. Internal Audit finding IA-2026-07 rated remote network access "High" and requires a remediation plan by 2026-12-31. A decision on 2026-10-06 is needed to run a 200-user pilot in Q4 2026.

## Background

- **Users and access model:** 4,200 remote users, including about 1,100 frequent travelers, receive full-tunnel access to 14 internal subnets.
- **User experience:** VPN issues drive 38% of remote access tickets (about 310 per month). A June emergency firmware patch caused a 6-hour EMEA outage.
- **Dependencies and readiness:** 212 applications depend on VPN; the top 40 carry about 85% of traffic, and about 25 legacy applications use non-HTTP protocols. MFA covers 100% of workforce accounts, and device posture covers 92% of managed laptops. OT remote access is out of scope.

## Assessment

- **Option A - VPN refresh ($420K capex plus ~$60K/yr):** Lowest disruption. Primary risk: retains network-level access and does not remediate IA-2026-07.
- **Option B - Full ZTNA (~$1.35M over 3 years):** Fully remediates the finding. Primary risk: legacy application compatibility and the 2027-03-31 deadline create high cutover risk.
- **Option C - Phased hybrid (~$1.1M over 3 years plus ~$90K for the residual VPN):** Moves about 85% of traffic to application-centric access quickly and limits legacy VPN access to named users for up to 18 months, under a documented exception. Primary risks: FY27 opex is unconfirmed, and Network Operations has limited ZTNA experience.

## Recommendation

Select Option C. It balances deadline risk, audit remediation, and user experience better than a like-for-like refresh or a single cutover. Contractors on unmanaged devices should receive browser-only, application-specific access. The vendor's claim of up to 40% fewer tickets is unvalidated and should be measured during the pilot, not assumed in the business case.

## Decision Requested

Select Option C as the target remote access approach and authorize a 200-user Q4 2026 pilot, contingent on Finance confirming the 3-year TCO and FY27 opex.

## Open Questions

- How will travelers in restricted regions connect? Legal and Trade Compliance input is pending.
- Is FY27 subscription opex available? The Finance TCO is due after inputs on 2026-09-25.
- Which legacy applications can be remediated or retired within 18 months? The application owner inventory is pending.

## Sources

- **User-provided:** Draft SBAR dated 2026-09-22, based on NovaCorp Architecture Working Session notes from 2026-09-15 (fictitious demo content).
- **Referenced, not independently verified:** CorvusGate support letter (2026-08-28); Internal Audit finding IA-2026-07.
- **Assumption requiring validation:** All cost figures are working estimates pending the Finance TCO.

## ADR Follow-up

ADR Follow-up: Recommended via the ADR Agent. This is a long-lived, architecturally significant shift from network-centric to application-centric access, with options, tradeoffs, and an audit dependency that require durable traceability.

## Sharing Guidance

Share with the requester and authorized decision stakeholders for the 2026-10-06 CIO staff meeting. Highlight the **Decision Requested** section. No option has been approved; the working session made no decision.

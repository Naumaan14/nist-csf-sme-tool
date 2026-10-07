# ============================================================
# engine.py  —  NIST CSF 2.0 Risk Assessment Engine
# Nauman Salimbhai Shaikh | MSc Cybersecurity | CO7047
# ============================================================

# ── Questions (30 total, 5 per function) ────────────────────
QUESTIONS = {
    "Govern": [
        "Our organisation has a documented cybersecurity policy that is reviewed at least annually.",
        "Senior management are aware of and accountable for cybersecurity risks facing the organisation.",
        "Our organisation has defined a risk appetite for cybersecurity and uses it to guide security decisions.",
        "Cybersecurity responsibilities are clearly assigned to specific individuals or roles.",
        "Our organisation regularly reviews its cybersecurity strategy in light of changes to its business or threat environment.",
    ],
    "Identify": [
        "Our organisation maintains an up-to-date inventory of all hardware and software assets.",
        "We have identified and documented all data types we process, including their sensitivity and storage locations.",
        "Our organisation conducts regular risk assessments to identify potential cybersecurity threats.",
        "We have assessed the cybersecurity practices of our key suppliers and third-party service providers.",
        "Known vulnerabilities in our systems are tracked and addressed in a timely manner.",
    ],
    "Protect": [
        "Access to systems and data is controlled and limited to authorised users only.",
        "Multi-factor authentication is used for all accounts with access to sensitive or business-critical data.",
        "All staff receive regular cybersecurity awareness training.",
        "Sensitive data is encrypted both in transit and at rest.",
        "Our systems are regularly patched and updated to address known security vulnerabilities.",
    ],
    "Detect": [
        "Our organisation monitors its networks and systems for unusual or suspicious activity.",
        "Security events and logs are collected, reviewed, and retained for an appropriate period.",
        "We have defined criteria for what constitutes a security incident and how it should be escalated.",
        "We have the capability to detect unauthorised access to our systems or data.",
        "Security monitoring covers both on-premise and cloud-based systems and services.",
    ],
    "Respond": [
        "Our organisation has a documented incident response plan that is known to relevant staff.",
        "We have practised or tested our incident response procedures in the past 12 months.",
        "There is a clear process for communicating with affected parties following a security incident.",
        "Following a security incident, we conduct a formal review to identify causes and prevent recurrence.",
        "Our organisation knows which regulatory authorities to notify in the event of a significant breach.",
    ],
    "Recover": [
        "Our organisation has a business continuity or disaster recovery plan covering cybersecurity incidents.",
        "Data backups are performed regularly and tested to ensure they can be successfully restored.",
        "We have defined recovery time objectives for critical systems following a cybersecurity incident.",
        "Recovery plans are reviewed and updated following changes to our systems or business operations.",
        "Our organisation has arrangements in place to maintain essential services while recovering from an incident.",
    ],
}

# ── Function weights (%) derived from DCMS 2023 breach data ─
WEIGHTS = {
    "Govern":   0.20,
    "Identify": 0.20,
    "Protect":  0.25,
    "Detect":   0.15,
    "Respond":  0.10,
    "Recover":  0.10,
}

# ── Predefined impact values per function (1-5 scale) ────────
IMPACT = {
    "Govern":   4,
    "Identify": 4,
    "Protect":  5,
    "Detect":   4,
    "Respond":  3,
    "Recover":  3,
}

# ── Maturity tier thresholds ─────────────────────────────────
def get_maturity(avg_score):
    if avg_score <= 2.0:
        return "Level 1 — Partial"
    elif avg_score <= 3.0:
        return "Level 2 — Risk-Informed"
    elif avg_score <= 4.0:
        return "Level 3 — Repeatable"
    else:
        return "Level 4 — Adaptive"

# ── Risk level classification ────────────────────────────────
def get_risk_level(score):
    if score > 15:
        return "High"
    elif score >= 8:
        return "Medium"
    else:
        return "Low"

# ── Recommendation library ───────────────────────────────────
RECOMMENDATIONS = {
    "Govern": {
        "High": [
            "Develop and formally approve a cybersecurity policy document, signed by senior leadership, covering acceptable use, data handling, and incident reporting. Review it annually.",
            "Assign explicit cybersecurity accountability to a named individual or role — even in small organisations a part-time security lead provides significant governance improvement.",
            "Define and document a risk appetite statement that guides which security investments are prioritised. This gives decision-makers a framework for consistent choices.",
        ],
        "Medium": [
            "Ensure the existing cybersecurity policy is communicated to all staff and that acknowledgement is recorded annually.",
            "Schedule a quarterly senior management briefing on the current cybersecurity risk landscape and the organisation's posture against it.",
            "Review and update the risk appetite statement to reflect any changes in business operations, client base, or regulatory environment.",
        ],
        "Low": [
            "Continue current governance practices and schedule an annual policy review.",
            "Consider pursuing Cyber Essentials certification to formalise and validate existing governance arrangements.",
            "Document lessons learned from any near-miss events and incorporate them into the next governance review cycle.",
        ],
    },
    "Identify": {
        "High": [
            "Create a complete asset register listing all hardware, software, and cloud services used by the organisation, including those used remotely by staff. Review it quarterly.",
            "Conduct a data mapping exercise to identify where all personal and business-critical data is stored, processed, and transmitted. This is also required for UK GDPR compliance.",
            "Perform an immediate risk assessment covering the organisation's top ten most critical assets. Prioritise based on data sensitivity and business impact if the asset were compromised.",
        ],
        "Medium": [
            "Extend the existing asset inventory to include cloud services and remote devices used by home workers.",
            "Review third-party supplier security arrangements and ensure contracts include minimum security requirements and the right to audit.",
            "Establish a vulnerability management process: subscribe to NCSC alerts, apply critical patches within 14 days, and track outstanding patches in the asset register.",
        ],
        "Low": [
            "Schedule a six-monthly review of the asset inventory to capture any new systems or services.",
            "Formalise the risk assessment process with a standard template and annual review cycle.",
            "Expand supplier assessments to cover all suppliers with access to business-critical systems or data.",
        ],
    },
    "Protect": {
        "High": [
            "Implement multi-factor authentication (MFA) immediately for all accounts with access to email, cloud services, and business-critical systems. This single control prevents the majority of phishing-driven account compromises.",
            "Conduct an urgent review of user access privileges: remove accounts for leavers, reduce permissions to the minimum required for each role, and disable generic or shared accounts.",
            "Ensure all endpoint devices — including personal devices used for work — are protected by up-to-date antivirus or endpoint detection software, and apply outstanding security patches immediately.",
        ],
        "Medium": [
            "Extend MFA to cover all staff, not just administrators or senior management.",
            "Deliver mandatory annual cybersecurity awareness training to all staff, covering phishing recognition, password hygiene, and incident reporting. Record completion.",
            "Implement full-disk encryption on all laptops and mobile devices that access business data.",
        ],
        "Low": [
            "Review and test the effectiveness of existing access controls annually, including a review of all privileged accounts.",
            "Introduce phishing simulation exercises to maintain staff awareness and identify individuals who may benefit from additional training.",
            "Ensure data encryption covers all new systems and cloud services adopted by the organisation.",
        ],
    },
    "Detect": {
        "High": [
            "Enable and centralise logging across all critical systems — servers, cloud services, firewalls, and endpoint devices. Logs should be retained for a minimum of 90 days.",
            "Define clear criteria for what constitutes a security event requiring escalation, and ensure all staff know how to report suspicious activity. Even a simple email address or phone number for reporting is a significant improvement.",
            "Subscribe to free threat intelligence services such as the NCSC Early Warning service and CISA alerts to receive notification of threats relevant to your sector and technology stack.",
        ],
        "Medium": [
            "Implement automated alerting for high-priority events such as repeated failed login attempts, after-hours access to sensitive systems, or large data exports.",
            "Extend monitoring to cover cloud-based services and remote working environments, which are frequently excluded from on-premise monitoring tools.",
            "Review log retention policies to ensure logs are kept long enough to support incident investigation — NCSC recommends a minimum of 12 months for critical systems.",
        ],
        "Low": [
            "Review monitoring coverage quarterly to ensure new systems and services are included.",
            "Test alerting rules periodically to confirm they fire correctly and that alerts reach the right people.",
            "Consider a managed detection and response (MDR) service if internal monitoring capacity is limited.",
        ],
    },
    "Respond": {
        "High": [
            "Develop and document an incident response plan covering at minimum: how incidents are detected and reported, who is responsible for managing the response, how affected parties and regulators are notified, and how evidence is preserved.",
            "Identify the regulatory notification obligations relevant to your organisation — for personal data breaches, the ICO must be notified within 72 hours under UK GDPR. Ensure the relevant contact details are readily accessible.",
            "Conduct a tabletop exercise simulating a phishing or ransomware incident to test staff awareness of their response responsibilities and identify gaps in the plan.",
        ],
        "Medium": [
            "Test the incident response plan at least annually through a structured tabletop exercise and update it based on lessons learned.",
            "Establish a communication template for notifying affected clients and stakeholders in the event of a breach, to reduce decision-making pressure during an actual incident.",
            "Define escalation paths for incidents of different severity levels, including out-of-hours contact arrangements for critical incidents.",
        ],
        "Low": [
            "Review and update the incident response plan following any significant changes to the organisation's systems, staff, or business operations.",
            "Include cybersecurity incident response in staff induction training so all new joiners are aware of their responsibilities.",
            "Maintain an up-to-date contact list of relevant parties including legal counsel, cyber insurance provider, and key suppliers.",
        ],
    },
    "Recover": {
        "High": [
            "Implement and test a regular backup regime: critical data should be backed up daily, with at least one copy held offsite or in a separate cloud environment. Test restoration at least quarterly.",
            "Define recovery time objectives (RTOs) for each critical system — how long can the business operate without email, financial systems, client databases? Use these to prioritise recovery planning.",
            "Develop a basic business continuity plan covering how essential services will be maintained if primary systems are unavailable for 24 hours, 72 hours, and one week.",
        ],
        "Medium": [
            "Test backup restoration procedures quarterly rather than annually and document the results.",
            "Review recovery plans following any significant infrastructure change, such as migration to cloud services or adoption of new business applications.",
            "Ensure recovery procedures account for remote working scenarios — can staff access recovery systems and continue working from home during an incident?",
        ],
        "Low": [
            "Schedule an annual review of recovery time objectives to ensure they remain aligned with current business priorities.",
            "Consider cyber insurance as part of the organisation's financial recovery planning for major incidents.",
            "Share recovery plan summaries with key staff so they know what to do even if primary systems are unavailable.",
        ],
    },
}

# ── Main calculation function ────────────────────────────────
def calculate_results(responses: dict) -> dict:
    """
    responses: { "Govern": [1,2,3,4,5], "Identify": [...], ... }
    returns full results dict
    """
    results = {}
    overall_weighted = 0.0

    for fn, scores in responses.items():
        avg  = sum(scores) / len(scores)
        like = (5 - avg) + 1          # invert: low avg = high likelihood
        imp  = IMPACT[fn]
        raw  = like * imp              # 1-25 scale
        wgt  = WEIGHTS[fn]
        mat  = get_maturity(avg)
        lvl  = get_risk_level(raw)
        recs = RECOMMENDATIONS[fn][lvl]

        results[fn] = {
            "scores":        scores,
            "avg":           round(avg, 2),
            "likelihood":    round(like, 2),
            "impact":        imp,
            "risk_score":    round(raw, 2),
            "weight":        wgt,
            "weighted":      round(raw * wgt, 2),
            "maturity":      mat,
            "risk_level":    lvl,
            "recommendations": recs,
        }
        overall_weighted += raw * wgt

    overall_level = get_risk_level(overall_weighted)

    return {
        "functions": results,
        "overall_score":  round(overall_weighted, 2),
        "overall_level":  overall_level,
        "sorted_functions": sorted(
            results.keys(),
            key=lambda f: results[f]["risk_score"],
            reverse=True
        ),
    }

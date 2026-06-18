"""
evaluation_scenarios.py - Test Dataset for the Email Generation Assistant.

Contains 10 unique scenarios, each with:
  - intent: Core purpose of the email.
  - key_facts: Bullet points that must appear in the output.
  - tone: The desired writing style.
  - human_reference: A manually written ideal email (the gold standard).
"""

SCENARIOS = [
    # =========================================================================
    # Scenario 1: Requesting project proposal details
    # =========================================================================
    {
        "id": 1,
        "intent": "Request detailed project proposal from a vendor",
        "key_facts": [
            "Project is a website redesign for Q1 2025 launch",
            "Budget ceiling is $75,000",
            "Need proposal by December 15th",
            "Must include timeline, cost breakdown, and team composition",
        ],
        "tone": "formal",
        "human_reference": """Subject: Request for Proposal — Website Redesign Project

Dear Ms. Patel,

I hope this message finds you well. I am writing to formally request a detailed proposal for our upcoming website redesign project, which we are targeting for a Q1 2025 launch.

To help guide your proposal, please note that our budget ceiling for this initiative is $75,000. We kindly ask that your submission include a comprehensive timeline, a detailed cost breakdown, and the proposed team composition for the project.

We would appreciate receiving your proposal by December 15th to allow sufficient time for internal review and decision-making.

Please do not hesitate to reach out should you require any additional information or clarification. We look forward to reviewing your proposal.

Sincerely,
Alex Chen
Director of Digital Strategy""",
    },
    # =========================================================================
    # Scenario 2: Apologizing for a service outage
    # =========================================================================
    {
        "id": 2,
        "intent": "Apologize for a 6-hour service outage and communicate resolution",
        "key_facts": [
            "Outage lasted from 2:00 AM to 8:00 AM EST on November 10th",
            "Root cause was a database migration failure",
            "All affected customers will receive a one-month service credit",
            "New failover protocols have been implemented to prevent recurrence",
        ],
        "tone": "empathetic and urgent",
        "human_reference": """Subject: Service Disruption on November 10th — Our Apology and Next Steps

Dear Valued Customer,

I want to sincerely apologize for the service outage that occurred on November 10th, lasting from 2:00 AM to 8:00 AM EST. I understand how disruptive this was to your operations, and I want you to know that we take full responsibility.

After a thorough investigation, we identified the root cause as a database migration failure during a scheduled maintenance window. This is not the level of reliability you expect from us, and we are deeply sorry.

To make this right, all affected customers will automatically receive a one-month service credit on their next billing cycle. No action is needed on your part.

Additionally, we have implemented new failover protocols to ensure this type of disruption does not happen again. Our engineering team has conducted extensive testing on these safeguards.

If you have any questions or concerns, please don't hesitate to reach out to our support team. We are here for you.

With sincere apologies,
Jamie Rivera
VP of Customer Success""",
    },
    # =========================================================================
    # Scenario 3: Negotiating a contract extension
    # =========================================================================
    {
        "id": 3,
        "intent": "Negotiate a 2-year contract extension with improved terms",
        "key_facts": [
            "Current contract expires March 31, 2025",
            "Proposing a 2-year extension through March 2027",
            "Requesting a 10% volume discount due to increased order quantities",
            "Willing to commit to minimum quarterly purchase of $200,000",
        ],
        "tone": "firm and professional",
        "human_reference": """Subject: Contract Extension Proposal — Partnership Through 2027

Dear Mr. Thompson,

As our current agreement approaches its expiration on March 31, 2025, I would like to discuss a contract extension that reflects the growth of our partnership.

We are proposing a 2-year extension, carrying our agreement through March 2027. Given the significant increase in our order quantities over the past year, we believe a 10% volume discount is warranted and mutually beneficial.

In return, we are prepared to commit to a minimum quarterly purchase of $200,000, providing your team with predictable revenue and strengthened planning capability.

I am confident we can reach terms that serve both organizations well. I would welcome the opportunity to discuss this proposal at your earliest convenience.

Regards,
Morgan Blake
Head of Procurement""",
    },
    # =========================================================================
    # Scenario 4: Congratulating a colleague on a promotion
    # =========================================================================
    {
        "id": 4,
        "intent": "Congratulate a colleague on their promotion to Senior Director",
        "key_facts": [
            "Colleague's name is Priya and she was promoted to Senior Director of Engineering",
            "She led the successful cloud migration project last quarter",
            "She has been with the company for 7 years",
            "Team celebration is planned for Friday at 4 PM",
        ],
        "tone": "warm and casual",
        "human_reference": """Subject: Huge Congrats, Priya! 🎉

Hey Priya,

I just heard the amazing news — Senior Director of Engineering! Honestly, no one deserves this more than you.

Watching you lead the cloud migration project last quarter was truly inspiring. You kept the team motivated, hit every milestone, and made it look effortless. After 7 years of dedication and brilliance, this promotion is long overdue!

I'm so excited to celebrate with you at the team get-together on Friday at 4 PM. Bring your best smile — you've earned this moment!

Cheers to you and everything ahead,
Sam""",
    },
    # =========================================================================
    # Scenario 5: Rejecting a job applicant
    # =========================================================================
    {
        "id": 5,
        "intent": "Inform a job applicant that they were not selected for the role",
        "key_facts": [
            "Applicant's name is David Park",
            "Role was Senior Data Analyst",
            "Over 200 applicants were considered",
            "Encouraging him to apply for future openings",
        ],
        "tone": "polite but decisive",
        "human_reference": """Subject: Update on Your Application — Senior Data Analyst Position

Dear David,

Thank you for taking the time to apply for the Senior Data Analyst position and for your interest in joining our team. We truly appreciate the effort you put into the interview process.

After careful consideration of over 200 applicants, we have decided to move forward with another candidate whose experience more closely aligns with the specific needs of this role. This was not an easy decision, and your qualifications made a strong impression on our hiring panel.

We sincerely encourage you to keep an eye on our careers page and apply for future openings that match your skills and interests. We would welcome the opportunity to consider you again.

We wish you the very best in your career journey.

Kind regards,
Taylor Kim
Talent Acquisition Manager""",
    },
    # =========================================================================
    # Scenario 6: Requesting budget approval from CFO
    # =========================================================================
    {
        "id": 6,
        "intent": "Request budget approval for a new AI-powered customer support tool",
        "key_facts": [
            "Tool is Zendesk AI Suite costing $45,000 annually",
            "Projected to reduce ticket resolution time by 35%",
            "Expected ROI of 280% within 18 months based on labor savings",
            "Pilot program with 3 agents showed 40% improvement in first-response time",
        ],
        "tone": "direct and analytical",
        "human_reference": """Subject: Budget Approval Request — Zendesk AI Suite ($45,000/year)

Dear CFO Martinez,

I am requesting approval for the annual licensing of the Zendesk AI Suite at a cost of $45,000 per year.

Our analysis projects a 35% reduction in average ticket resolution time, translating to an expected ROI of 280% within 18 months, driven primarily by labor cost savings and increased throughput.

These projections are supported by data from our 3-agent pilot program, which demonstrated a 40% improvement in first-response time over a 60-day trial period.

I have attached the full cost-benefit analysis for your review. I would welcome the opportunity to walk through the numbers with you at your convenience.

Respectfully,
Dana Okafor
Director of Customer Operations""",
    },
    # =========================================================================
    # Scenario 7: Following up after a sales call
    # =========================================================================
    {
        "id": 7,
        "intent": "Follow up after an initial sales discovery call",
        "key_facts": [
            "Call was held on Tuesday, November 5th",
            "Prospect expressed interest in the Enterprise plan",
            "Main pain point is manual reporting consuming 15 hours per week",
            "Next step is a live product demo scheduled for November 12th",
        ],
        "tone": "enthusiastic and persuasive",
        "human_reference": """Subject: Great Connecting on Tuesday — Your Demo is Locked In!

Hi Rachel,

It was fantastic speaking with you on Tuesday, November 5th! I really appreciated you sharing the challenges your team is facing, and I'm excited about the opportunity to help.

I completely understand how frustrating it must be to lose 15 hours every week to manual reporting — that's nearly two full workdays! The good news is that our Enterprise plan is specifically designed to eliminate that bottleneck and give your team those hours back.

As we discussed, I've locked in your live product demo for November 12th. During the session, I'll walk you through exactly how the platform automates the reporting workflows you described, so you can see the impact firsthand.

In the meantime, feel free to reach out if any questions come up. I'm looking forward to showing you what's possible!

Best,
Casey Wright
Account Executive""",
    },
    # =========================================================================
    # Scenario 8: Internal memo about company policy changes
    # =========================================================================
    {
        "id": 8,
        "intent": "Announce a new hybrid work policy to all employees",
        "key_facts": [
            "Effective January 1, 2025",
            "Employees must be in-office a minimum of 3 days per week (Tuesday, Wednesday, Thursday)",
            "Remote work is allowed on Mondays and Fridays",
            "Exceptions require manager approval and HR documentation",
        ],
        "tone": "direct and authoritative",
        "human_reference": """Subject: Updated Hybrid Work Policy — Effective January 1, 2025

Dear Team,

I am writing to inform you of an important update to our hybrid work policy, effective January 1, 2025.

Going forward, all employees are required to be in the office a minimum of three days per week, specifically Tuesday, Wednesday, and Thursday. Remote work will continue to be available on Mondays and Fridays.

Any exceptions to this schedule must be approved by your direct manager and documented through HR. Please reach out to your manager or the HR team if you have questions about the exception process.

This policy reflects our commitment to fostering collaboration and maintaining the strong team culture that defines our organization. We appreciate your cooperation as we implement this change.

Regards,
Executive Leadership Team""",
    },
    # =========================================================================
    # Scenario 9: Rescheduling a client meeting
    # =========================================================================
    {
        "id": 9,
        "intent": "Reschedule a client meeting due to an internal conflict",
        "key_facts": [
            "Original meeting was scheduled for Thursday, November 14th at 2:00 PM",
            "Proposing to reschedule to Monday, November 18th at 10:00 AM",
            "The agenda (product roadmap review) remains unchanged",
            "Will send updated calendar invite once confirmed",
        ],
        "tone": "apologetic and professional",
        "human_reference": """Subject: Request to Reschedule Our November 14th Meeting

Dear Ms. Nakamura,

I hope you are doing well. I am writing to sincerely apologize for the need to reschedule our meeting originally planned for Thursday, November 14th at 2:00 PM. An internal scheduling conflict has arisen that unfortunately cannot be moved.

I would like to propose rescheduling to Monday, November 18th at 10:00 AM, if that works with your calendar. The agenda for our product roadmap review remains unchanged, so we will pick up right where we planned.

Once you confirm the new time, I will promptly send over an updated calendar invitation.

I apologize again for any inconvenience this may cause, and I truly appreciate your flexibility.

Warm regards,
Riley Cooper
Senior Account Manager""",
    },
    # =========================================================================
    # Scenario 10: Asking a teammate for help on a cross-functional project
    # =========================================================================
    {
        "id": 10,
        "intent": "Ask a teammate from the data team for help with analytics integration",
        "key_facts": [
            "Need help integrating Google Analytics 4 event tracking into the new checkout flow",
            "Launch deadline is November 22nd",
            "Estimated effort is about 4-6 hours of their time",
            "Product manager Lisa has already approved the cross-team collaboration",
        ],
        "tone": "collaborative and respectful",
        "human_reference": """Subject: Quick Favor — GA4 Integration Help for Checkout Flow

Hi Raj,

I hope your week is going well! I'm reaching out because I could really use your expertise on something.

We're in the final stretch of building the new checkout flow, and I need some help integrating Google Analytics 4 event tracking into it. You're the first person I thought of given your experience with GA4.

The estimated effort is about 4-6 hours, and our launch deadline is November 22nd, so there's a reasonable window to fit it in. I've already checked with Lisa (our PM), and she's fully on board with the cross-team collaboration.

I'd love to hop on a quick call to walk you through the specifics whenever you have a free moment. No pressure at all — if the timing doesn't work, I completely understand.

Thanks so much for considering it!

Best,
Avery
Frontend Engineering""",
    },
]

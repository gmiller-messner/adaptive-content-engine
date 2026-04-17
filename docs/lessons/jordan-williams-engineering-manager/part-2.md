---
title: "Part 2: Your Data Is the Risk"
layout: default
nav_order: 2
parent: "LLM Security for People Managers: Protecting Your Team's Data"
grand_parent: Lessons
---

Prompt injection is about what can happen *to* you through AI tools. But there's an equally important risk that runs in the other direction: what happens to the data you put *into* AI tools.

### The Samsung Lesson

In 2023, Samsung engineers pasted proprietary source code into ChatGPT for debugging help. The code left Samsung's control permanently. Samsung subsequently banned generative AI tools on internal networks.

According to LayerX's 2025 research, 77% of enterprise employees who use AI have pasted company data into chatbot queries, and 22% of those instances included confidential personal or financial data.

The Samsung incident wasn't an attack. Nobody hacked anything. Engineers used the tool exactly as intended, and confidential data left the organization because that's what happens when you paste it into an external service.

### What This Means for People Managers

Consider what you might paste into an AI tool on a given week:

- A draft performance improvement plan with specific behavioral concerns
- Compensation benchmarking notes with salary figures
- Notes from a difficult 1:1 about a team member's underperformance
- A disciplinary write-up
- Candidate resumes with personal contact information
- Hiring rubric criteria that reveal internal evaluation standards

Every one of those items contains data that your organization — and in many cases, employment law — expects you to handle with care. When that content goes into an AI tool, several things may be true:

- The tool's provider may store your input for model training or improvement
- The content may be accessible to the provider's employees during review processes
- The data has left your organization's security perimeter and you have no mechanism to retrieve it
- If you're using a personal AI account, your company's data handling agreements don't apply at all

### Shadow AI Is the Quiet Risk

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Shadow AI</strong> — The use of personal or unapproved AI tools for work tasks, bypassing company security policies and data handling agreements.</span>

If you sometimes use a personal ChatGPT or Claude account for work — especially late at night when the company-approved tool feels inconvenient — you're engaging in shadow AI usage. This isn't unusual. It's extremely common. But it means:

- Your company's enterprise agreements (which may prohibit training on submitted data) don't cover your personal account
- Your IT and security teams have no visibility into what data is leaving the organization
- You may be the only person who knows that a direct report's performance data is sitting in your personal chat history

The risk isn't that you're doing something malicious. The risk is that well-intentioned, routine tool usage can result in sensitive data leaving your control permanently.

### Building a Personal Data Policy

Rather than trying to remember security rules in the moment, it helps to have a clear personal policy you've thought through in advance. Here's a framework:

**Never paste into any AI tool — approved or otherwise:**
- Specific employee names paired with performance ratings, compensation figures, or disciplinary details
- Content from active HR investigations or legal matters
- Personal identifying information (Social Security numbers, home addresses, medical information)
- Content that would cause harm if it appeared in a data breach disclosure

**Consider carefully, and use only company-approved tools:**
- Anonymized performance review drafts ("an engineer on my team" rather than "Sarah Chen")
- General hiring rubric criteria without candidate-specific details
- Templates for difficult conversations, stripped of identifying information

**Generally lower risk:**
- Asking for help structuring a meeting agenda (without sensitive specifics)
- Drafting generic communication templates
- Brainstorming interview questions for a role

The key habit is the pause: *before you paste, ask yourself what would happen if this content became public.* If the answer involves legal liability, employee trust violations, or competitive harm, it doesn't go into the tool.

<div class="lesson-nav"><a href="../part-1/" class="lesson-nav-prev">← Part 1: Prompt Injection</a><a href="../part-3/" class="lesson-nav-next">Part 3: Supply Chain Attacks →</a></div>

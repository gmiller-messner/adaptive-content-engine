---
title: "Part 5: Your Defense Plan"
layout: default
nav_order: 5
parent: "AI Security for People Managers"
grand_parent: Lessons
---

### Human-in-the-Loop Is Your Superpower

For most technical security defenses — input sanitization, system prompt hardening, dependency pinning — you're relying on your team or your tools. But the single most important defense for a people manager is one you already have: human judgment applied at the right moment.

**For hiring:** If an AI tool ranks or summarizes candidates, treat the output as one input among many. Review the actual resumes yourself for any role you're making the final call on. The AI's recommendation may have been influenced by content you can't see.

**For performance management:** If you've used AI to help draft a performance review or summarize feedback, read the final version as if the employee will see it (they will). Does it reflect *your* assessment, or did you defer to the AI's framing?

**For sensitive communications:** If you've asked an AI to help you prepare for a difficult conversation — a PIP discussion, a termination, a complaint — make sure the AI's output didn't shape your conclusion. It should help you articulate a decision you've already made, not make the decision for you.

### Tool Hygiene

- **Use approved tools for work tasks.** If your organization has an enterprise AI tool, use it — even when it's less convenient. The data handling protections exist for a reason.
- **Check data retention policies.** If you're unsure whether a tool stores or trains on submitted content, find out before you paste sensitive information into it.
- **Separate personal and professional AI use.** A personal account for brainstorming weekend plans and a work account for personnel management serve different purposes and should stay separate.

### What to Tell Your Team

If you manage people who build or use AI tools, you're in a position to set norms. A few things worth reinforcing:

- Any document fed to an AI tool — a resume, a shared file, a Slack message — is a potential injection vector. Treat AI-generated summaries of external content with appropriate skepticism.
- Data pasted into AI tools doesn't disappear. Treat every paste as a potential disclosure.
- If something looks wrong — an AI recommendation that seems too confident, a summary that doesn't match what you read yourself, unexpected behavior from an AI-integrated tool — trust your instincts and verify.

### A Quick Gut Check

You can explain prompt injection to a colleague in one sentence: *"It's when someone hides instructions inside a document or message that trick an AI tool into doing something it shouldn't."*

You can explain the data risk in one sentence: *"Anything you paste into an AI tool might be stored, and you can't take it back."*

If those two ideas guide your daily AI usage, you're ahead of most.

---


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li><strong>Prompt injection</strong> exploits the fact that AI tools can't distinguish your instructions from instructions hidden in content they're asked to process — like a resume, a document, or a Slack message</li>
  <li><strong>Indirect injection is the variant that affects you most</strong> — you'll never see the attack, because the malicious instructions are invisible to humans but readable by the AI</li>
  <li><strong>The data you paste into AI tools is a security risk on its own</strong> — performance reviews, compensation details, and disciplinary records don't belong in personal AI accounts, and require caution even in approved tools</li>
  <li><strong>Shadow AI bypasses the protections your organization has put in place</strong> — using a personal AI account for work tasks means sensitive data is governed by consumer terms of service, not enterprise agreements</li>
  <li><strong>AI-generated recommendations on personnel decisions should never be final</strong> — treat them as drafts, not verdicts, especially for hiring, performance reviews, and disciplinary actions</li>
  <li><strong>Pause before pasting</strong> — the single highest-impact habit is a moment of friction before submitting sensitive content to any AI tool: "Should this data go into this tool?"</li>
  <li><strong>Supply chain attacks compromise trusted components</strong> — you don't need to understand the technical details, but knowing the concept helps you ask the right questions of your team about dependency management and build security</li>
  </ul>
</div>

<div class="lesson-nav">
<a href="../part-4/" class="lesson-nav-prev">← Part 4: Supply Chain Attacks — What Managers Need to Know</a>
</div>


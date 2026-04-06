Learning Objectives
LLM Security Threats: Prompt Injection and Supply Chain Vulnerabilities

Shared Learning Objectives
By the end of this lesson, all learners will be able to:

Define prompt injection and explain why LLMs are architecturally vulnerable to it
Distinguish between direct and indirect prompt injection, and explain why indirect injection is the more dangerous variant
Explain what a supply chain attack is and how it differs from a direct attack on an application
Identify at least two concrete behaviors they can adopt to reduce their personal exposure to these threats


Developer Learning Objectives (Alex Chen)
By the end of this lesson, Alex will be able to:

Explain the architectural reason LLMs cannot reliably distinguish instructions from data, and why this makes prompt injection a structural problem rather than a fixable bug
Identify the specific points in an agentic pipeline where prompt injection risk is highest — particularly where external content enters the context window
Implement input sanitization as a layered defense in an LLM application, using techniques appropriate to the content type — such as HTML stripping with BeautifulSoup, allowlist filtering, and regex pattern matching
⚑ SME REVIEW: Confirm which sanitization techniques are most effective and relevant for LLM applications specifically — security professional input needed
Write a system prompt defense that instructs the model to flag and refuse injected instructions found in external content
Explain what dependency pinning is and how to combine it with automated update tooling like Dependabot or Renovate so that updates happen deliberately and with review rather than silently at install time
Identify which credentials should never be exposed as environment variables in a CI/CD pipeline and explain why build environments are high-value targets in a supply chain attack


Manager Learning Objectives (Jordan Williams)
By the end of this lesson, Jordan will be able to:

Explain prompt injection in plain language to a non-technical colleague or report
Recognize that the content fed into AI tools — performance reviews, compensation notes, disciplinary records, candidate resumes — is itself a security and data exposure risk, independent of whether the tool itself is compromised
Recognize the specific ways their workflow creates data exposure risk — including feeding sensitive personnel information into AI tools, using personal AI accounts for work tasks (shadow AI), and relying on AI to screen candidate applications without human review
Internalize the lesson from real-world data leakage incidents and apply it to their own workflow — specifically, developing the habit of pausing before pasting any sensitive data into an AI tool
Articulate a personal policy for what data is and is not appropriate to paste into an AI tool
Identify the human-in-the-loop behaviors that reduce risk — specifically, pausing before approving AI-generated content that involves sensitive personnel decisions


Vibe-Coder Learning Objectives (Morgan Lee)
By the end of this lesson, Morgan will be able to:

Explain why LLMs cannot reliably distinguish trusted instructions from content they are asked to process
Internalize the lesson from supply chain attacks and apply it to their own workflow — specifically, treating every dependency installation as a security decision rather than a routine step
Adopt the highest-impact supply chain hygiene habits for their context, including checking version numbers before approving installs and auditing .env files for exposed credentials
⚑ SME REVIEW: Confirm which 2-3 habits have the highest impact for a non-engineer persona — security professional input needed
Pause and verify before approving any agentic action that installs packages, runs scripts, or accesses external systems
Identify credentials in their working environment — API keys, cloud credentials, .env files — that would be high-value targets in a supply chain attack
Apply a personal checkpoint: distinguish between "Claude Code suggested this" and "I have verified this is safe"
Identify the signs that a package or environment may have been compromised — such as unexpected CPU usage, unfamiliar files in site-packages, or unusual outbound network activity — and know the immediate steps to take
⚑ SME REVIEW: Confirm the most recognizable and actionable warning signs for a non-engineer persona — and verify the recommended immediate steps
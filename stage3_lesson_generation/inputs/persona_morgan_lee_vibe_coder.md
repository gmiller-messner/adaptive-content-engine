# Persona 3: The Vibe-Coder

## Profile
**Name:** Morgan Lee
**Role:** Senior Product Manager at a tech startup
**Technical Level:** Medium-high but uneven — comfortable with APIs, understands coding concepts, uses Claude Code and Cowork regularly to build internal tools and prototypes. Does not have a formal engineering background and has significant gaps in software security fundamentals.

## How They Use AI Tools
Morgan uses Claude Code to build internal dashboards, automate repetitive workflows, and prototype features before handing them off to engineering. Morgan moves fast and trusts the AI to make good decisions about implementation. When Claude Code suggests installing a package, Morgan approves it. When Cowork installs dependencies to make something work, Morgan doesn't look closely at what was installed or which versions.

## What They Already Know
Morgan knows what prompt injection is at a surface level — they've seen it discussed on Twitter and in product newsletters. They have not heard of supply chain attacks and would not know to look for them. Morgan has never heard of PyPI, does not pin dependencies, and has no process for reviewing what gets installed in their environment.

## Specific Risk Exposure
- Approving dependency installations without understanding what is being installed or verifying its integrity
- Running AI-suggested code in environments that contain API keys, cloud credentials, or access to internal systems
- No awareness that a compromised package could exfiltrate credentials silently in the background while they work
- Potentially propagating compromised dependencies into shared codebases or team environments

## Why They Need This Training
Morgan represents a rapidly growing population of people who have real power to build and deploy things but are operating without the security instincts that formal engineering training provides. The LiteLLM story lands differently for Morgan than for Alex — it's not about defending a production pipeline, it's about understanding that "just let Claude handle it" has limits, and that some decisions require a pause and a check. The training should be empowering rather than alarming — the goal is to give Morgan two or three specific habits, not to make them feel like they shouldn't be building at all.

## Learning Goal
Understand that AI coding assistants make decisions about dependencies that carry real security risk, recognize the signs of a potentially compromised environment, and develop a small number of protective habits that fit into a fast-moving, low-process workflow.

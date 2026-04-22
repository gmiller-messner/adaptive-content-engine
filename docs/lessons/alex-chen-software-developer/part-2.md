---
title: "Part 2: Prompt Injection — Where It Enters Your Pipeline"
layout: default
nav_order: 2
parent: "LLM Security for Developers: Prompt Injection and Supply Chain Attacks"
grand_parent: Lessons
---

### Hidden Content Techniques

Attackers exploit a fundamental asymmetry: humans skim rendered output and miss things. LLMs read everything with equal attention.



<div class="image-placeholder" data-caption="Side-by-side comparison showing hidden content techniques — white-on-white text revealed by selecting all, tiny text zoomed in, HTML comment visible only in source"></div>



Common techniques to be aware of when processing external content:

- **White text on white background** — invisible to a human reviewer, fully readable by any model processing the document or rendered page
- **Tiny text** — font size too small for a human to notice, but parsed identically by the model
- **HTML comments** — invisible in a browser, present in the raw HTML your scraper or retrieval tool passes to the model
- **File metadata** — hidden fields in documents (EXIF data, document properties) that humans never inspect
- **Steganography** — instructions encoded into pixel values of an image, undetectable by visual inspection but readable by vision-capable models

Each of these is a channel that your application might ingest without any human ever seeing the payload.

### Why Agentic Systems Raise the Stakes

A chatbot that only produces text has a limited blast radius — the worst outcome is a misleading response. If you're building agentic features, the calculus changes fundamentally because the model has access to tools.

When an agent is manipulated through prompt injection, it can take real, irreversible actions:

- **Email access** — forward sensitive data to an external address
- **Code execution** — run malicious scripts in a sandboxed or unsandboxed environment
- **Web access** — submit forms, make purchases, interact with APIs
- **Terminal access** — if you're using something like Claude Code, the terminal itself is exposed

The Auto-GPT cryptocurrency wallet demonstration illustrates the end state: researchers gave an agent control of a real wallet and email access. An attacker sent an email with hidden instructions disguised as newsletter content. The agent processed the email, absorbed the instructions, and initiated a funds transfer. Gone before any human reviewed what happened.

The ServiceNow Now Assist incident from late 2025 adds another dimension for multi-agent systems. Attackers fed a low-privilege agent a malformed request that tricked it into asking a higher-privilege agent to export case files to an external URL. The privileged agent trusted its peer and executed the request — bypassing checks that would have applied to a human user. If you're building systems where agents communicate with each other, trust between agents has to be enforced architecturally, not assumed.

<div class="lesson-nav"><a href="../part-1/" class="lesson-nav-prev">← Part 1: Prompt Injection — The Architectural Problem</a><a href="../part-3/" class="lesson-nav-next">Part 3: Prompt Injection — Layered Defenses →</a></div>

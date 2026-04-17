---
title: "Part 2: Supply Chain Attacks"
layout: default
nav_order: 2
parent: "AI Security for Builders: What Every Prompt and Every Install Costs You"
grand_parent: Lessons
---

### A Different Kind of Trust Problem

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply Chain Attack</strong> — An attack that targets not your application directly, but the tools, libraries, and dependencies it relies on. If an attacker compromises something your application trusts, they inherit that trust.</span>

Prompt injection exploits how LLMs process information. Supply chain attacks exploit how software gets built — specifically, the chain of packages and tools that your code depends on.

If you've used Claude Code or Cowork to build something, your project almost certainly has dependencies — packages that were installed to make things work. You may not have chosen those packages directly. You may not know their names. But they're running in your environment, and each one is a piece of software you're implicitly trusting.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>PyPI (Python Package Index)</strong> — The standard repository where Python developers download packages. When you or your AI tool runs `pip install something`, it's pulling from PyPI.</span>

### The LiteLLM Attack: March 2026



<div class="image-placeholder" data-caption="&quot;The call was coming from inside the house&quot; — illustration representing a trusted security tool becoming the attack vector"></div>



This is the story that makes supply chain risk concrete.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>LiteLLM</strong> — A popular Python package that serves as a unified gateway to multiple LLM providers, downloaded roughly 3.4 million times per day. It's a direct dependency of projects including CrewAI, DSPy, MLflow, and others.</span>

On March 24, 2026, a threat actor known as TeamPCP published two malicious versions of LiteLLM to PyPI. Within approximately three hours, those versions were downloaded 47,000 times. Here's how it happened:

LiteLLM used a security scanner called Trivy in its automated build process. TeamPCP had compromised Trivy weeks earlier. When LiteLLM ran its routine security scan, the compromised Trivy stole the credential that authorizes publishing new versions to PyPI. TeamPCP used that stolen credential to publish backdoored versions of LiteLLM within minutes.

The security tool designed to protect the pipeline became the key that unlocked it.

### What the Malware Actually Did

The malicious code ran a three-stage attack:

1. **Credential harvesting** — It grabbed environment variables, API keys, SSH keys, cloud credentials, Kubernetes secrets, and cryptocurrency wallet files
2. **Lateral movement** — It attempted to spread across any connected infrastructure
3. **Persistent backdoor** — It installed itself in a way designed to keep receiving attacker instructions even after the initial compromise was discovered

Version 1.82.8 was particularly aggressive. It installed itself as a <span class="term-callout"><span class="term-badge">TERM</span> <strong>.pth file</strong> — A Python path configuration file that executes automatically every time the Python interpreter starts</span>. Simply having the package installed meant the malware ran on every Python command, every test run, every build — whether or not you ever imported LiteLLM directly.

### Why This Matters for Your Workflow

Here's where this connects to how you might work day-to-day.

If you're using Claude Code or Cowork to build something, and the tool says "I need to install package X to make this work," you're making a trust decision in that moment. You're trusting that:

- The package is what it claims to be
- The version being installed hasn't been tampered with
- The package's own dependencies haven't been compromised

In the LiteLLM case, 88% of the 2,337 packages on PyPI that depended on LiteLLM had no version pin — meaning they would have automatically pulled the compromised version. Anyone who ran a routine `pip install` or `pip upgrade` during that three-hour window, or whose project pulled LiteLLM in as a <span class="term-callout"><span class="term-badge">TERM</span> <strong>Transitive Dependency</strong> — A dependency you didn't install directly, but that was pulled in because something you *did* install depends on it</span>, was potentially affected.

A compromised package running in your environment has access to everything your environment has access to. If your `.env` file contains API keys, cloud credentials, or access tokens, those are now accessible to the malware.



<div class="image-placeholder" data-caption="Example SBOM (Software Bill of Materials) showing a dependency tree with a compromised package highlighted — illustrating how a transitive dependency you didn't choose can be the one that's compromised"></div>



---

<div class="lesson-nav"><a href="../part-1/" class="lesson-nav-prev">← Part 1: Prompt Injection</a><a href="../part-3/" class="lesson-nav-next">Part 3: Your Environment Is the Target →</a></div>

---
title: "Part 2: Supply Chain Attacks — The Threat You Haven't Met"
layout: default
nav_order: 2
parent: "Security Decisions You're Already Making"
grand_parent: Lessons
---

### What a Supply Chain Attack Is

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply chain attack</strong> — an attack that targets not your application itself, but the tools, libraries, and dependencies it relies on. If an attacker compromises something your application trusts, they inherit that trust.</span>

When you build something with Claude Code or Cowork, you're almost never building from scratch. Your project depends on a stack of open-source packages — libraries that handle HTTP requests, parse data, connect to APIs, format output. Each of those packages might depend on other packages, which depend on still more packages. This is your supply chain.

A supply chain attack doesn't target your code. It targets something your code trusts. If an attacker can compromise a popular package — or even a tool used to build that package — they gain access to every environment that installs it.



<div class="image-placeholder" data-caption="&quot;The call was coming from inside the house&quot; — visual showing the security scanner as the attack vector"></div>



### The LiteLLM Story

On March 24, 2026, something went wrong with <span class="term-callout"><span class="term-badge">TERM</span> <strong>LiteLLM</strong> — a popular Python package that serves as a unified gateway to multiple LLM providers, downloaded approximately 3.4 million times per day</span>. Production systems running LiteLLM started showing runaway processes: CPUs pegged at 100%, containers crashing from memory exhaustion.

The cause: two malicious versions of LiteLLM had been quietly published to <span class="term-callout"><span class="term-badge">TERM</span> <strong>PyPI (Python Package Index)</strong> — the standard public repository where Python developers download packages, similar to an app store for Python libraries</span>. They were live for approximately three hours. In that window, they were downloaded roughly 47,000 times.

Here's where it gets unsettling: LiteLLM didn't have a gap in their security. They had a security scanner — a tool called Trivy — built into their automated build pipeline. Trivy was the attack vector.

A threat actor had compromised Trivy weeks earlier. When LiteLLM's pipeline ran its routine security scan on March 24th, it pulled the compromised version of Trivy. The malicious Trivy read the environment variables on the build server, found the <span class="term-callout"><span class="term-badge">TERM</span> <strong>PyPI publishing token</strong> — the credential that authorizes releasing new versions of a package to PyPI</span>, and used it to publish two backdoored versions of LiteLLM within minutes.

The security tool designed to protect the pipeline became the key that unlocked it.

### What the Malware Actually Did

The malicious code ran a three-stage attack:

1. **Credential harvesting** — it grabbed environment variables, API keys, SSH keys, cloud credentials, Kubernetes secrets, even cryptocurrency wallet files
2. **Lateral movement** — it attempted to spread across any connected infrastructure it could reach
3. **Persistence** — it installed a backdoor designed to keep receiving attacker instructions even after the initial malware was discovered

Version 1.82.8 was particularly aggressive. It installed itself as a <span class="term-callout"><span class="term-badge">TERM</span> <strong>.pth file</strong> — a Python path configuration file that executes automatically every time the Python interpreter starts</span>. Simply having the package installed meant the malware ran on every Python command, every test run, every build — without LiteLLM even being explicitly imported. And all harvested data was encrypted and sent to a domain designed to look like a legitimate LiteLLM service.

For anyone who had installed the compromised versions, every credential accessible from that system had to be treated as stolen — API keys, cloud credentials, SSH keys, database passwords, CI/CD secrets.

### This Is Your Ecosystem

If you've ever seen Claude Code or Cowork run `pip install` during a build, you're operating in the same ecosystem where this happened.

LiteLLM is a direct dependency of projects including CrewAI, DSPy, MLflow, and others. Any developer — or product manager building with AI tools — who ran a routine `pip install` or `pip upgrade` during that three-hour window was potentially affected. Of the 2,337 packages on PyPI that depend on LiteLLM, 88% had no <span class="term-callout"><span class="term-badge">TERM</span> <strong>version pin</strong> — specifying an exact version number for a dependency rather than allowing automatic resolution to the latest available version</span>. Those unpinned packages would have automatically pulled in the compromised versions.

The attackers didn't need to target each project individually. They compromised one widely trusted package and inherited access to everything downstream.

<div class="lesson-nav"><a href="../part-1/" class="lesson-nav-prev">← Part 1: Prompt Injection — The Core Problem</a><a href="../part-3/" class="lesson-nav-next">Part 3: Your Environment Is a Target →</a></div>

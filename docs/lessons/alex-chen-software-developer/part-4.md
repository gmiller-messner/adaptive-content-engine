---
title: "Part 4: Supply Chain Attacks — The LiteLLM Breach"
layout: default
nav_order: 4
parent: "LLM Security for Developers: Prompt Injection and Supply Chain Attacks"
grand_parent: Lessons
---

### How a Security Scanner Became the Attack Vector



<div class="image-placeholder" data-caption="&quot;The call was coming from inside the house&quot; — illustrating that the security tool itself was compromised"></div>



<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply chain attack</strong> — An attack that targets not the application itself but the tools, libraries, and infrastructure it depends on. If an attacker compromises something your application trusts, they inherit that trust.</span>

On March 24, 2026, production systems running LiteLLM started showing runaway processes — CPUs at 100%, containers crashing from memory exhaustion. The cause: two malicious versions of LiteLLM (1.82.7 and 1.82.8) had been published to PyPI.

LiteLLM is downloaded roughly 3.4 million times per day. The malicious versions were live for approximately three hours. In that window, 47,000 downloads occurred. Of those, 23,142 were pip installs of version 1.82.8 — environments where the malware executed automatically during installation.

Here's the part that should recalibrate your threat model: LiteLLM had a security scanner in their pipeline. They were running Trivy — a widely used vulnerability scanning tool. The threat actor, TeamPCP, had compromised Trivy weeks earlier. When LiteLLM's CI/CD pipeline ran its routine security scan on March 24th, the compromised Trivy read the environment variables on the build server, found the PyPI publishing token, and exfiltrated it. TeamPCP used that token to publish two backdoored versions within minutes.

The security tool designed to protect the pipeline became the attack vector.

### What the Malware Did

The attack executed in three stages:

1. **Credential harvesting** — environment variables, API keys, SSH keys, cloud credentials, Kubernetes secrets, cryptocurrency wallet files
2. **Lateral movement** — across any Kubernetes clusters accessible from the compromised environment
3. **Persistent backdoor** — designed to continue receiving instructions from attacker-controlled servers even after the initial payload was removed

Version 1.82.8 was particularly aggressive. It installed itself as a `.pth` file — a Python path configuration file that executes automatically every time the Python interpreter starts, regardless of whether LiteLLM is explicitly imported. Having the package installed meant the malware ran on every `python` command, every test run, every build.

All harvested data was encrypted and exfiltrated to a domain designed to look like an official LiteLLM service.

### The Blast Radius

LiteLLM is a direct dependency of CrewAI, DSPy, MLflow, OpenHands, Arize Phoenix, langwatch, strands-agents, and others. Nine major projects issued security PRs within hours.

Of the 2,337 packages on PyPI that depend on LiteLLM, **88% had no version pin** — meaning they would have automatically resolved to the compromised versions during the exposure window.

If you or your CI/CD pipeline ran `pip install litellm` or `pip install --upgrade litellm` during those three hours — or if any package in your dependency tree pulled LiteLLM as a transitive dependency without a pin — you were potentially affected.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Transitive dependency</strong> — A package your application doesn't depend on directly, but which is pulled in because one of your direct dependencies requires it. You may not know it's in your stack.</span>

FutureSearch published a dependency checker at futuresearch.ai/tools/litellm-checker if you want to verify whether specific packages in your stack were exposed.

<div class="lesson-nav">
<a href="../part-3/" class="lesson-nav-prev">← Part 3: Prompt Injection — Layered Defenses</a><a href="../part-5/" class="lesson-nav-next">Part 5: Supply Chain — Hardening Your Stack →</a>
</div>


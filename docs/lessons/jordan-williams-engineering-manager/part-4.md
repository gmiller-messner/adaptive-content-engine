---
title: "Part 4: Supply Chain Attacks — What Managers Need to Know"
layout: default
nav_order: 4
parent: "AI Security for People Managers"
grand_parent: Lessons
---

### The Concept

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply chain attack</strong> — An attack that targets the tools, libraries, or services an application depends on, rather than attacking the application directly. If the attacker compromises something your system trusts, they inherit that trust.</span>

You don't need to understand supply chain attacks at a technical level, but you do need to understand the concept, because it affects tools your team builds and tools you use.

Modern software isn't built from scratch. It's assembled from hundreds of pre-built components — open-source libraries, third-party packages, automated build tools. A supply chain attack compromises one of those components, and every application that depends on it is affected.

### The LiteLLM Attack

On March 24, 2026, a widely used AI infrastructure package called LiteLLM was compromised. LiteLLM is downloaded roughly 3.4 million times per day and serves as a dependency for many AI tools and platforms.



<div class="image-placeholder" data-caption="&quot;The call was coming from inside the house&quot; — illustrating that the security scanner itself was the attack vector"></div>



Here's what makes this case worth knowing: the attackers didn't break into LiteLLM directly. They compromised a *security scanner* — a tool called Trivy that LiteLLM used to check for vulnerabilities. When LiteLLM's automated build process ran its routine security scan, the compromised scanner stole the credentials needed to publish new versions of LiteLLM. The attackers then published two backdoored versions that harvested API keys, cloud credentials, and other secrets from anyone who installed them.

The malicious versions were live for about three hours. In that window, they were downloaded roughly 47,000 times. Of the 2,337 packages that depend on LiteLLM, 88% had no version restrictions — meaning they would have automatically pulled in the compromised version.

The security tool designed to protect the pipeline became the weapon that compromised it.

### Why This Matters to You

You probably don't install Python packages yourself. But your team might use tools built on packages like LiteLLM — and you might use AI-powered tools whose supply chains you've never thought about. The lesson for managers is about the nature of the risk: a single compromised component can cascade through thousands of downstream systems in hours. When your team talks about dependency management, version pinning, or build pipeline security, those conversations are about preventing exactly this kind of attack.

If you manage developers, the concrete questions worth asking:

- "Are our dependencies pinned to specific versions, or do we pull the latest automatically?"
- "What external tools run in our build pipeline, and how are they secured?"
- "When was the last time we rotated our CI/CD credentials?"

You don't need to know the answers yourself. You need to make sure someone on your team does.

<div class="lesson-nav"><a href="../part-3/" class="lesson-nav-prev">← Part 3: Your Data Is the Attack Surface</a><a href="../part-5/" class="lesson-nav-next">Part 5: Your Defense Plan →</a></div>

---
title: "LLM Security for Developers: Prompt Injection and Supply Chain Attacks"
layout: default
nav_order: 1
has_children: true
parent: Lessons
---

# LLM Security for Developers: Prompt Injection and Supply Chain Attacks

If you're building features that route LLM calls through LangChain or LiteLLM, you're working with infrastructure that processes external content, holds privileged credentials, and pulls dependencies from public registries on every build. You already think about input validation, dependency management, and least privilege — those instincts all apply here. What's different is *where* the vulnerabilities live and how fast the blast radius scales in AI tooling. This lesson covers the two highest-impact threat categories in that stack: prompt injection and supply chain attacks.

<div class="lesson-nav"><span class="lesson-nav-prev"></span><a href="../part-1/" class="lesson-nav-next">Part 1: Prompt Injection — The Architectural Problem →</a></div>

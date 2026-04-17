---
title: "requirements.txt — unpinned (dangerous)"
layout: default
nav_order: 1
has_children: true
parent: Lessons
---

## LLM Security Threats: Prompt Injection and Supply Chain Vulnerabilities

If you're building features that route LLM requests through packages like LangChain or LiteLLM, you're working at the intersection of two threat categories that behave differently from what most software security training covers. Prompt injection exploits the model itself. Supply chain attacks exploit the infrastructure around it. Both target trust relationships — but different ones, and with different blast radii.

This lesson covers both, with implementation-level detail. The goal is to leave you with defenses you can put into code, not just concepts you can recite.

---

<div class="lesson-nav"><span class="lesson-nav-prev"></span><a href="../part-1/" class="lesson-nav-next">Part 1: Prompt Injection →</a></div>

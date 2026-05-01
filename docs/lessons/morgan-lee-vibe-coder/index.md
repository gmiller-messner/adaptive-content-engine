---
title: "Security Decisions You're Already Making"
layout: default
nav_order: 3
has_children: true
parent: Lessons
---

# Security Decisions You're Already Making

Every time you approve a package install in Claude Code, let Cowork add a dependency, or run a script an AI agent wrote for you, you're making a security decision. You might not be framing it that way — it feels like just getting things done. But each of those moments involves trust: trust that the package is what it claims to be, trust that the code does what it says, trust that nothing in your environment is being quietly read by something that shouldn't have access to it.

This lesson covers two categories of threat that are directly relevant to how you work: prompt injection (which you may have encountered at a surface level) and supply chain attacks (which you probably haven't, but which touch your workflow every time a package gets installed). The goal isn't to slow you down or make you second-guess everything. It's to give you a few specific habits that protect you without breaking your stride.

<div class="lesson-nav">
<a href="part-1/" class="lesson-nav-next">Part 1: Prompt Injection — The Core Problem →</a>
</div>


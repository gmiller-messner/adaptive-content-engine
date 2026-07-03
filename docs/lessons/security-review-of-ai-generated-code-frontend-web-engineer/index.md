---
title: "Reviewing the Code Your Agent Writes for You"
layout: default
nav_order: 102
has_children: true
parent: Lessons
---

# Reviewing the Code Your Agent Writes for You

You reach for an agent to scaffold a component, refactor a hook, or stub out tests, and what comes back compiles, passes lint, reads like something you'd write, and renders correctly in the browser. That's exactly the problem. The defects that survive in AI-generated code aren't syntax errors — those get caught. What's left lives in the logic and the security properties: the component that renders fine but pipes untrusted data straight into the DOM, the API integration that assumes the caller is allowed to see what it fetches. This lesson is about reviewing generated code in your layer of the stack — the browser, the bundle, the npm tree — where the polish is highest and the quiet failures are yours to catch.

<div class="lesson-nav">
<a href="part-1/" class="lesson-nav-next">Part 1: Why Fluent Output Earns More Scrutiny →</a>
</div>


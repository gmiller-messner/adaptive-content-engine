---
title: "Part 1: Why Fluent Output Earns More Scrutiny"
layout: default
nav_order: 1
parent: "Reviewing the Code Your Agent Writes for You"
grand_parent: Lessons
---

### The "it renders fine" trap

A React component that displays correctly in the browser has cleared a very low bar. Rendering correctly tells you the JSX is valid and the props flow — it tells you nothing about whether the data reaching a sink is safe, or whether the user viewing it is allowed to.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Sink</strong> — a point where data leaves your control and does something consequential: written to the DOM, sent in an API call, interpolated into a query. Untrusted data reaching an unsafe sink is where most frontend vulnerabilities live.</span>

Most AI-generated defects are gaps between what the code was *supposed* to do and what it actually does. The code does something plausible — just not the right thing, or not the safe thing. An agent asked to render user-submitted comments will happily produce a component that displays them. Whether it escapes them first is a coin flip that depends on how it reached for the DOM.

### Automation bias, in your workflow

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Automation bias</strong> — the tendency to trust automated output more as it looks more polished, applying less scrutiny exactly when errors get harder to see.</span>

Here's the mechanism worth naming: reviewers rate fluent-looking code as safer than it is, and scrutinize AI output *less* than human-written code because it "reads well." When a teammate opens a PR, you might quietly check their assumptions. When the agent produces the same code, the clean formatting and idiomatic patterns read as competence.

The discipline is to invert the instinct. Treat "this looks fine" as a prompt to check, not a conclusion. Fluent output has earned skepticism, not a pass.

### Start with intent, not line one

Before reading a generated component line by line, decide what "right" looks like:

- **What is this supposed to do?** What data does it show, to whom, sourced from where?
- **What result is correct?** What should render for a logged-in user versus a stranger?
- **What would make it unsafe?** Untrusted HTML in the DOM? A field that should never leave the server?

Reviewers who skip straight to reading catch typos and miss the component that does the wrong thing convincingly. Two kinds of gap hide in generated code, and they're caught differently. **Security gaps** — a missing check, an unescaped sink — you can find with a repeatable lens. **Correctness gaps** — logic that computes the wrong result — surface only when you already understand the intended behavior well enough to notice the divergence. No checklist finds a correctness flaw for you.

<div class="lesson-nav">
<a href="./" class="lesson-nav-prev">← Introduction</a><a href="../part-2/" class="lesson-nav-next">Part 2: The Sinks That Matter in Your Layer →</a>
</div>


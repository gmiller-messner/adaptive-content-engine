---
title: "Part 1: Why Fluent Code Disarms You"
layout: default
nav_order: 1
parent: "Reviewing AI-Generated Backend Code: The Failure Modes Your Review Muscle Misses"
grand_parent: Lessons
---

### The defect is in the logic, not the syntax

When a junior engineer sends you a handler with a hand-rolled query and inconsistent naming, your skepticism fires before you've finished reading. That reaction is doing real work — the surface mess is a proxy signal that tells you to slow down.

AI-generated code removes the proxy signal. It compiles, passes linting, follows your naming conventions, and reads as idiomatic Go or Python. What remains wrong is underneath: the missing authorization check, the ORM escape hatch, the deserialization path that trusts its input. The output is surface-clean and subtly unsound at the same time, and that combination is what makes it a distinct review problem rather than just more code in the queue.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Automation bias</strong> — the tendency to apply less scrutiny to output that looks polished or comes from an automated system, exactly when the remaining errors are hardest to see.</span>

### Volume makes it systematic

Two forces compound. Fluent output invites more trust, so you scrutinize it less right when the errors are getting subtler. And generation volume means more code reaches your review than you have hours to absorb carefully. A single instance of "it reads fine, ship it" is a lapse. The same reflex applied across every generated PR you approve in a week is a systematic hole in your review coverage.

The discipline is to treat "it looks fine" as a prompt to check, not a conclusion — and to spend that check where the tools can't help you, which is the subject of the rest of this lesson.

<div class="lesson-nav">
<a href="./" class="lesson-nav-prev">← Introduction</a><a href="../part-2/" class="lesson-nav-next">Part 2: What AI Reintroduces in Service Code →</a>
</div>


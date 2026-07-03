---
title: "Part 4: A Review Workflow for Generated Components"
layout: default
nav_order: 4
parent: "Reviewing the Code Your Agent Writes for You"
grand_parent: Lessons
---

### The five-step lens

Apply this to any AI-generated component or API integration before merge:

1. **Establish intent.** What is this supposed to do, where does its data come from, and who should see it? This is the foundation — everything below depends on it.
2. **Trace untrusted input to its sink.** Follow every user-controlled or API-sourced value to where it lands: a render call, a `dangerouslySetInnerHTML`, an `href`, an outgoing request. Confirm it's escaped or sanitized at each.
3. **Check the authorization assumption.** What did the agent assume about who's allowed here? Is that assumption also enforced server-side, and does any sensitive value reach the browser at all? Look for the missing check, not just the wrong line.
4. **Spot-check what tooling covers.** Confirm `npm audit` / Dependabot and secret scanning flagged the dependency and secrets surface. Eyeball only the one thing they can miss — a hallucinated or typosquatted package name.
5. **Don't trust the generated tests.** More on this below.

### What generated tests skip

A passing suite is not evidence of safety, and not even of correctness. Agent-written tests tend to encode the *same* misunderstanding of intent the code does — so they pass while the logic is wrong. They routinely assert the happy path and skip:

- **XSS payloads as prop values** — a test passes `"hello"` as a comment, never `<img src=x onerror=alert(1)>`.
- **Unauthorized render paths** — tests render as an authorized user and never check what a stranger or wrong-role user sees.
- **API boundary conditions** — empty responses, unexpected shapes, oversized or malformed data from the endpoint.

Reason about what the tests actually check. A green run on a suite that never sends a hostile prop value tells you the component works, not that it's safe. If you'd want a test for the injection case, the absence of that test is itself a finding.

### Block versus fix forward

Not every finding stops a merge. Communicating the distinction clearly keeps you credible with your team.

**Block the merge:**

- **An active XSS sink** receiving untrusted, unsanitized data — a live vulnerability.
- **A secret hardcoded** in client code or exposed through a public build prefix.
- **A package** that won't resolve, looks like a typosquat, or can't be verified.
- **A rendered-but-hidden sensitive value** the browser can read regardless of the UI.

**Fix forward, flag in the PR:**

- Missing edge-case tests where the happy path is sound and no untrusted data reaches a sink.
- A `dangerouslySetInnerHTML` on content you've confirmed is trusted and static, but that would benefit from a sanitization pass for defense in depth.
- Lower-severity input validation gaps with no direct sink.

The framing that keeps this from being bureaucratic: security review here is the code review you already do, re-weighted for code that's fluent, plentiful, and untrustworthy by default. Your leverage is highest exactly where the tooling is weakest — judgment about intent, authorization, and what's missing.


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li>Rendering correctly and passing tests clears a low bar — fluent generated code has earned more scrutiny, not less, because its defects live in logic and security properties, not syntax.</li>
  <li>Lead every review with unsafe rendering sinks (<code>dangerouslySetInnerHTML</code>, <code>innerHTML</code>, URL sinks) and sanitize with DOMPurify when HTML rendering is genuinely required.</li>
  <li>Client-side authorization is UX, not security — confirm the server enforces the rule, and ensure no sensitive value reaches the browser at all, since the Network tab shows everything the API returned.</li>
  <li>No secret survives in a client bundle; treat any public build prefix (<code>NEXT_PUBLIC_</code>, <code>VITE_</code>, <code>REACT_APP_</code>) as a signal the value will ship, and confirm it's safe to expose.</li>
  <li>Verify every agent-suggested package by exact name with <code>npm view</code>, plus download count and maintenance, before install — hallucinated and typosquatted names slip past scanners that only know <em>known</em>-bad packages.</li>
  <li>Generated tests encode the same misunderstanding the code does; a green run that never sends an XSS payload or checks an unauthorized path is not a safety signal.</li>
  <li>Block on live XSS sinks, hardcoded or exposed secrets, and unverifiable packages; fix forward on missing edge-case tests and lower-severity gaps — and communicate which is which.</li>
  </ul>
</div>

<div class="lesson-nav">
<a href="../part-3/" class="lesson-nav-prev">← Part 3: Secrets and Supply Chain in the Bundle</a>
</div>


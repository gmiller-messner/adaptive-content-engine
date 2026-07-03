---
title: "Part 4: Tests and Merge Decisions"
layout: default
nav_order: 4
parent: "Reviewing AI-Generated Backend Code: The Failure Modes Your Review Muscle Misses"
grand_parent: Lessons
---

### Don't count green

Generated tests tend to assert the happy path: the endpoint returns 200 for valid input. They skip the cases that define your actual risk surface, and worse, they often encode the *same* misunderstanding of intent the code does — so they pass while the logic is wrong. A passing suite is not evidence of safety or of correctness.

For a backend endpoint, the security cases the generated suite almost certainly skipped:
- **Another user's resource ID** — call with a valid token but someone else's `invoice_id`; the ownership check should reject it.
- **No token** — confirm the unauthenticated path is actually closed.
- **Wrong scope or tenant** — a token valid for a different role or tenant should not succeed.

Reason about what the tests check, not how many are green. Use the gaps to drive what you require before merge.

### Fast, consistent merge/block calls

At volume, you need decisions that don't require re-litigating each time. A workable default:

**Unconditional merge-stoppers:**
- **Missing or bypassable authorization** — an endpoint that authenticates but doesn't check ownership or scope.
- **Unparameterized query construction** — any user-influenced value assembled into a query by string interpolation.

**Blockers with a clear remediation path:**
- **Data exposure in responses or logs** — over-broad serializers, secrets or tokens in structured logs. Block, name the field, point at the fix.

**Fix-forward — don't hold the review:**
- **Overly broad error messages, suboptimal retry logic, style nits.** Real, but they don't gate the merge.

Drawing this line consistently is what keeps your review both fast and safe. The stoppers are exactly the classes where the tools are weakest and the blast radius is largest; the fix-forward items are where a later PR is fine.


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li>Fluent AI output suppresses the skepticism that surface-messy code triggers; at review volume, that suppression becomes a systematic gap, not an occasional one.</li>
  <li>Your highest-leverage catch is broken authorization — the authenticated-but-not-authorized endpoint — because it depends on your business rules and scanners structurally can't find it.</li>
  <li>Injection reappears through ORM escape hatches (<code>raw()</code>, <code>execute()</code>, <code>fmt.Sprintf</code> into a query, <code>Statement</code> concatenation); scan for those patterns directly rather than re-reading every line.</li>
  <li>Review by intent and absence: decide what the endpoint should be allowed to do, trace untrusted input to its sinks, and look first for the missing check, not the malformed one.</li>
  <li>Generated tests assert the happy path and encode the same intent errors as the code; require the ownership, no-token, and wrong-scope cases before merge.</li>
  <li>Treat missing/bypassable authorization and unparameterized queries as unconditional merge-stoppers; data exposure as a blocker with a fix; error messages and retry logic as fix-forward.</li>
  <li>Let secret scanning and SCA own hardcoded secrets and known-bad dependencies; keep your own eye only on hallucinated or typosquatted package names.</li>
  </ul>
</div>

<div class="lesson-nav">
<a href="../part-3/" class="lesson-nav-prev">← Part 3: The "What's Missing" Discipline</a>
</div>


---
title: "Part 3: The \"What's Missing\" Discipline"
layout: default
nav_order: 3
parent: "Reviewing AI-Generated Backend Code: The Failure Modes Your Review Muscle Misses"
grand_parent: Lessons
---

Your existing review reflex is tuned to find what's *wrong* — the malformed line, the off-by-one. AI-generated defects are more often what's *absent*: the check that should be there and isn't. That requires a different pass.

### Establish intent before reading lines

Before you read the handler line by line, decide what "right" looks like: what should this endpoint be allowed to do, and for whom? What result is correct, and what would make it unsafe? Reviewers who skip straight to reading catch typos and miss the code that does the wrong thing convincingly. You can't spot an absent authorization check if you haven't decided what the authorization rule should be.

This is the same principle as writing the test before you trust the implementation — you need the spec in your head to see where the code quietly diverges from it.

### Trace the untrusted input path

Follow each input from entry to use. At every sink — the query, the shell call, the deserialize, the downstream service call, the file path — confirm it's handled safely. In a generated handler this is a short, targeted trace, not a full re-read: entry point, into the service layer, into the query. You're checking the specific hops where the model tends to cut corners.

### Look for the absent check first

Ask the authorization question before the injection question, because it's the higher-leverage catch: does this code confirm the caller is allowed to do what it does, against *your* rule? Then check input validation, error handling, and output encoding as the next possible absences. The mental move is "what should be here that isn't," not only "what here is wrong."

### Verify parameterization by pattern, not by reading

You don't need to re-read every query. You need to know the exact patterns where models cut corners — the escape hatches from Part 2 — and search for them directly: `raw(`, `execute(`, `fmt.Sprintf` near a `Query`, `Statement` without `Prepared`. That's a targeted scan you can run in seconds per PR, which is what makes it survivable at volume.

<div class="lesson-nav">
<a href="../part-2/" class="lesson-nav-prev">← Part 2: What AI Reintroduces in Service Code</a><a href="../part-4/" class="lesson-nav-next">Part 4: Tests and Merge Decisions →</a>
</div>


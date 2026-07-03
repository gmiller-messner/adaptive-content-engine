# Security Review of AI-Generated Code — Source Document

### Why AI-generated code carries security risk

Foundational AI tools let engineers generate working code fast. The risk is not that the code looks wrong; it's that it looks right. Current models produce output that compiles, passes linting, follows naming conventions, and reads as idiomatic. The defects that remain are in the logic and the security properties, not the syntax. That combination, surface-clean and subtly unsound, is what makes AI-generated code a distinct review problem rather than just "more code to review."

Two forces make this worse as models improve. First, better output invites more trust, so reviewers apply less scrutiny exactly when the errors are getting harder to see (automation bias). Second, higher generation volume means more code reaches review than human capacity can absorb. Industry data through 2026 shows security debt and high-risk vulnerabilities rising year over year, not falling, as adoption scales.

The reviewer's job shifts accordingly, and it starts with intent. Before checking anything, the reviewer has to know what the code is *supposed* to do, because most AI-generated defects are gaps between intent and implementation: the code does something plausible, just not the right thing, or not the safe thing. Two kinds of gap matter here, and they are not caught the same way. **Security gaps** (a missing authorization check, an unsafe input path) can be found with a pattern lens, the workflow described below. **Correctness gaps** (logic that computes the wrong result) cannot; they surface only when the reviewer understands the intended behavior well enough to notice the output diverges from it. No checklist finds a correctness flaw for you. Understanding intent well enough to see where the code quietly departs from it is the reviewer's core leverage, and it is the throughline of every step that follows.

### The vulnerability classes AI reproduces most, ordered by what the reviewer actually needs to catch

AI coding tools are trained on large bodies of public code, including insecure patterns, and reproduce those patterns fluently. But not every class needs the same attention from a human reviewer at a mature organization. The defenses that scale, automated scanning in CI and security-aware system prompts, already handle the pattern-level classes well. What they cannot handle is the class that depends on the organization's own rules about who is allowed to do what. So the classes below are ordered by *residual human-review leverage*: how much a careful reviewer adds after good tooling and prompting are in place.

**Assumption:** this ordering assumes a mature org already runs secret scanning, dependency/SCA scanning, and reasonable SAST in CI, and uses security-aware prompting. Where that tooling is weaker, the lower-leverage classes below move back up. Confirming that tooling baseline is one of the first things to check with the org.

**Lead here, highest human-review leverage:**
- **Broken access control / authorization.** Generated endpoints and handlers implement the happy path (does the thing) but omit the check for whether this caller is allowed to do it. Scanners largely cannot catch this, because the correct check depends on *your* business rules, not a general pattern; security-aware prompting doesn't reliably fix it for the same reason. And it shades into intent: a missing authorization check is a security-relevant logic gap. This is the class where the human reviewer is the only real defense, and it is consistently near the top of real-world breach data. It is the core of what this lesson should teach.

**Partially handled by tooling, meaningful residue for the reviewer:**
- **Injection (SQL, command, template).** Generated code concatenates input into queries or shell commands instead of using parameterized statements. SAST catches many cases, but not all, especially through ORMs, dynamic query building, or less common sinks.
- **Cross-site scripting (XSS) and unsafe rendering.** Untrusted data flowing into the DOM without escaping, or dangerous sinks (innerHTML, dangerouslySetInnerHTML). Framework defaults and linters catch much of it; the residue is deliberate use of escape hatches.
- **Insecure deserialization and unsafe parsing.** Deserializing untrusted input or using unsafe loaders without validation. Some SAST coverage, but context-dependent.

**Mostly handled upstream, know them but don't dwell:**
- **Secrets and sensitive data exposure.** Hardcoded credentials, keys in client code, secrets in logs. Secret scanning, pre-commit hooks, and platform secret managers catch most of this. Real, but largely an infrastructure problem, not a review-skill problem.
- **Vulnerable, outdated, hallucinated, or typosquatted dependencies.** The model may suggest a package that is outdated, known-vulnerable, nonexistent, or a typosquat. SCA scanning and an internal registry handle the known-CVE and version-currency cases. The one part worth a reviewer's eye is the hallucinated/typosquatted name, which is a supply-chain vector that scanning may miss because the package is new rather than known-bad.

**The core of the lesson:** the defenses that scale (tooling, prompting) handle the pattern-level classes; what's left for the human reviewer is authorization and intent, which is exactly where AI fails quietest. A lesson for a mature, well-tooled audience should lead with authorization and treat secrets and dependencies as context, not curriculum.

### Automation bias: the human failure mode

Reviewers rate plausible-looking code as safer than it is, and scrutinize AI output less than human-authored output because it "reads well." Naming this bias is part of the defense: the review discipline is to apply *more* skepticism to fluent output, not less, and to treat "it looks fine" as a prompt to check, not a conclusion.

### A security-review workflow for AI-generated code

A repeatable lens to apply to any AI-generated change, before merge:

1. **Establish intent first.** What is this code supposed to do, what result is correct, and what would make it unsafe? This is the foundation, not a warm-up. You cannot catch a logic flaw or a missing control if you haven't decided what "right" looks like. Reviewers who skip straight to reading line by line catch typos and miss the code that does the wrong thing convincingly. Everything below depends on this step.
2. **Trace untrusted input.** Follow every input from entry to use. At each use (query, command, render, deserialize, file path), confirm it's handled safely.
3. **Check for the missing control, authorization first.** The most common and most dangerous omission is the access-control check: does this code confirm the caller is allowed to do what it does? Scanners won't catch this, because the right rule is yours, not a general pattern, so you have to know the intended rule and look for its absence. Input validation, error handling, and output encoding are the next absences to check. Look for what's missing, not just what's wrong.
4. **Spot-check what tooling should already cover.** Dependencies and secrets are mostly caught upstream by SCA and secret scanning, so confirm the pipeline flagged them rather than re-doing that work by hand. The one thing to eyeball yourself is a hallucinated or typosquatted package name, which can be too new for a scanner to know is bad.
5. **Don't trust AI-written tests blindly.** Generated tests often assert the happy path and skip the security and edge cases. A passing suite is not evidence of safety, or of correctness: generated tests tend to encode the same misunderstanding of intent the code does, so they pass while the logic is wrong. Reason about what the tests actually check, don't count green.

### Tooling, and its limits

Automated scanning belongs in CI: SAST for static analysis, DAST for running behavior, SCA/dependency scanning for vulnerable and malicious packages, secret scanning for exposed credentials. These catch a meaningful share of issues and should gate merges. But no single scanner catches most AI-specific problems, and logic-level authorization gaps and business-logic flaws generally require human review. Tooling narrows the field; it doesn't replace the reviewer. Security-aware prompting also helps upstream: naive prompts produce measurably more vulnerabilities than security-framed ones, so asking the model for secure patterns is a first line, not a substitute for review.

### The takeaway

Security review of AI-generated code is not a new discipline bolted onto engineering; it's the existing discipline of code review, re-weighted for a world where the code is fluent, plentiful, and untrustworthy-by-default. The reviewer's leverage is highest exactly where the tools are weakest: judgment about intent, authorization, and what's missing.

# Security Review of AI-Generated Code — Learning Objectives

By the end of this lesson, the learner can:

1. Explain why AI-generated code is surface-clean but can be subtly unsafe, and why fluent output warrants more review scrutiny, not less (automation bias).
2. Identify which vulnerability classes actually warrant their attention: lead with broken access control / authorization, the class tooling and prompting cannot cover, recognize the stack-specific residue (XSS and client-side supply-chain for frontend; injection and access control for backend), and treat secrets and known-bad dependencies as mostly handled upstream.
3. Apply a security-review workflow to an AI-generated change: establish intent, trace untrusted input, check for the missing control (authorization first), and confirm tooling covered dependencies and secrets rather than re-doing that work by hand.
4. Recognize when a passing test suite is not evidence of safety, and identify the security cases generated tests tend to skip.
5. Decide what to escalate or block: which issues are merge-stoppers versus fix-forward, ranked by severity.

# Reviewing the Code Your Agent Writes for You

You reach for an agent to scaffold a component, refactor a hook, or stub out tests, and what comes back compiles, passes lint, reads like something you'd write, and renders correctly in the browser. That's exactly the problem. The defects that survive in AI-generated code aren't syntax errors — those get caught. What's left lives in the logic and the security properties: the component that renders fine but pipes untrusted data straight into the DOM, the API integration that assumes the caller is allowed to see what it fetches. This lesson is about reviewing generated code in your layer of the stack — the browser, the bundle, the npm tree — where the polish is highest and the quiet failures are yours to catch.

## Part 1: Why Fluent Output Earns More Scrutiny

### The "it renders fine" trap

A React component that displays correctly in the browser has cleared a very low bar. Rendering correctly tells you the JSX is valid and the props flow — it tells you nothing about whether the data reaching a sink is safe, or whether the user viewing it is allowed to.

[TERM: Sink — a point where data leaves your control and does something consequential: written to the DOM, sent in an API call, interpolated into a query. Untrusted data reaching an unsafe sink is where most frontend vulnerabilities live.]

Most AI-generated defects are gaps between what the code was *supposed* to do and what it actually does. The code does something plausible — just not the right thing, or not the safe thing. An agent asked to render user-submitted comments will happily produce a component that displays them. Whether it escapes them first is a coin flip that depends on how it reached for the DOM.

### Automation bias, in your workflow

[TERM: Automation bias — the tendency to trust automated output more as it looks more polished, applying less scrutiny exactly when errors get harder to see.]

Here's the mechanism worth naming: reviewers rate fluent-looking code as safer than it is, and scrutinize AI output *less* than human-written code because it "reads well." When a teammate opens a PR, you might quietly check their assumptions. When the agent produces the same code, the clean formatting and idiomatic patterns read as competence.

The discipline is to invert the instinct. Treat "this looks fine" as a prompt to check, not a conclusion. Fluent output has earned skepticism, not a pass.

### Start with intent, not line one

Before reading a generated component line by line, decide what "right" looks like:

- **What is this supposed to do?** What data does it show, to whom, sourced from where?
- **What result is correct?** What should render for a logged-in user versus a stranger?
- **What would make it unsafe?** Untrusted HTML in the DOM? A field that should never leave the server?

Reviewers who skip straight to reading catch typos and miss the component that does the wrong thing convincingly. Two kinds of gap hide in generated code, and they're caught differently. **Security gaps** — a missing check, an unescaped sink — you can find with a repeatable lens. **Correctness gaps** — logic that computes the wrong result — surface only when you already understand the intended behavior well enough to notice the divergence. No checklist finds a correctness flaw for you.

## Part 2: The Sinks That Matter in Your Layer

Not every vulnerability class needs equal attention. If your org runs `npm audit` or Dependabot, secret scanning, and lint rules in CI, a lot of the pattern-level risk is already handled. What's left for you concentrates in two places: unsafe rendering and client-side authorization.

### Unsafe rendering sinks

This is your highest-frequency exposure. [TERM: XSS (Cross-Site Scripting) — injecting attacker-controlled script into a page, executed in another user's browser, typically because untrusted data reached the DOM without escaping.]

React escapes by default — `{userComment}` in JSX is safe. The danger is the escape hatches an agent reaches for when the default doesn't fit the ask:

[ATTACK MODEL CARD: dangerouslySetInnerHTML with untrusted data]
Vector: User-controlled string passed to dangerouslySetInnerHTML
Mechanism: The agent renders rich text or HTML content and bypasses React escaping to do it
Example: <div dangerouslySetInnerHTML={{ __html: comment.body }} /> where comment.body came from an API
Risk level: High — active XSS if the data is attacker-influenced
Who's at risk: Any component rendering user-generated or externally-sourced HTML
[/ATTACK MODEL CARD]

Sinks to flag on sight in generated code:

- **`dangerouslySetInnerHTML`** — the React one. Ask immediately: where does `__html` come from, and is it sanitized?
- **`innerHTML` / `outerHTML`** — direct DOM writes, common when an agent drops out of the React model for a "quick" manipulation.
- **`document.write`, `insertAdjacentHTML`** — same class, less common, same question.
- **URL sinks** — a `href={userValue}` that could carry `javascript:`, or an agent-built redirect from a query param.

The defense is concrete: if content genuinely must render as HTML, sanitize it with **DOMPurify** before it hits the sink — `DOMPurify.sanitize(comment.body)` — rather than trusting the source. If it doesn't need to be HTML, push back to plain `{text}` interpolation. An agent will reach for `dangerouslySetInnerHTML` because it satisfies the prompt, not because it weighed the risk.

[IMAGE: side-by-side of the same comment component — left uses dangerouslySetInnerHTML with a raw string, right pipes it through DOMPurify — with an injected <img onerror=...> payload firing on the left only]

### Client-side authorization is not authorization

This is the class where you are the only real defense, because the answer depends on *your* application's rules, not a general pattern a scanner knows.

An agent will generate a component that conditionally renders an admin panel based on a `user.role` prop, and it will look correct. Two failures hide here:

- **The check is the only check.** Hiding a button client-side is UX, not security. If the underlying API endpoint doesn't enforce the same rule server-side, anyone can call it directly through dev tools or `fetch`. The agent cannot know whether the server enforces the rule — only you and the server-side contract can.
- **The component fetches data it then hides.** A generated dashboard might request the full dataset and filter it in the client. Everything in that response is visible in the Network tab regardless of what renders. If a user shouldn't *see* a value, it must never reach the browser.

[TERM: Broken access control — code that implements the action but omits the check for whether the caller is allowed to perform it. Consistently near the top of real-world breach data.]

When you review a generated API integration, the question isn't "does the UI hide this correctly?" It's "does the client assume an authorization the server actually enforces, and does any sensitive value ride along in a response the browser can read?" That's a conversation with your backend contract, not something the agent reasoned about.

## Part 3: Secrets and Supply Chain in the Bundle

These two classes are mostly handled by tooling at a mature org — know them, confirm the pipeline caught them, and don't re-do that work by hand. But each has one residue that lands on your desk specifically.

### Secrets that ship to the browser

Anything in your client bundle is readable by anyone who opens dev tools. There is no such thing as a secret in frontend code.

An agent doesn't reliably distinguish server-only from client-safe values. Ask it to wire up an API call and it may inline a key it saw in context, or reach for an environment variable without knowing which side of the build it lives on. Patterns to catch:

- **Hardcoded keys or tokens** in a component or service file — `const API_KEY = "sk_live_..."`.
- **`process.env` values that get bundled.** In many setups, only prefixed vars (`REACT_APP_`, `NEXT_PUBLIC_`, `VITE_`) reach the client — the prefix is a signal that the value *will* ship. An agent may add the prefix to make a value "available" without registering that it's now public.
- **Secrets in error handling or logging** the agent added for debugging.

The defense is layered and mostly not manual: **git-secrets** or a pre-commit hook and CI secret scanning should catch hardcoded credentials before merge. Your job is to confirm the pipeline flagged them, and to apply the one rule tooling can't reason about — any value with a public build prefix must actually be safe to expose. If it's a real secret, it belongs behind a server route, not in the bundle.

### npm packages, including ones that don't exist

[TERM: Typosquatting — publishing a malicious package under a name close to a popular one (reactt, lodahs) hoping an install typo or a confident wrong suggestion pulls it in.]

SCA tooling — `npm audit`, Dependabot, Renovate, or an internal registry — handles the known-vulnerable and outdated cases well. Confirm those ran; don't hand-audit CVEs the scanner already covers.

The residue that's genuinely yours is the **hallucinated or typosquatted package name.** An agent may confidently suggest `npm install` for a package that:

- **Doesn't exist** — the model invented a plausible-sounding name.
- **Exists but isn't what it seems** — a typosquat sitting one character off a real package.

Scanning can miss both because a brand-new malicious package isn't yet *known*-bad. Before any `npm install` an agent proposes:

- **Confirm the exact name** resolves on the registry — `npm view <package>`.
- **Check download count and maintenance** — a "utility" with 40 weekly downloads and no commits in two years is a flag.
- **Compare against what you already use** — if the agent suggested a new package to do something an existing dependency handles, question why.

[ATTACK MODEL CARD: Hallucinated package install]
Vector: Agent suggests an import and matching npm install command
Mechanism: The model produces a plausible package name that is nonexistent or a typosquat; an attacker may have pre-registered the hallucinated name
Example: import { debounce } from 'react-use-debounce-hook' — a name that sounds real and may not be
Risk level: High — arbitrary code execution at install time via postinstall scripts
Who's at risk: Any project where agent-suggested dependencies get installed without a name check
[/ATTACK MODEL CARD]

## Part 4: A Review Workflow for Generated Components

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

[TAKEAWAYS]
- Rendering correctly and passing tests clears a low bar — fluent generated code has earned more scrutiny, not less, because its defects live in logic and security properties, not syntax.
- Lead every review with unsafe rendering sinks (`dangerouslySetInnerHTML`, `innerHTML`, URL sinks) and sanitize with DOMPurify when HTML rendering is genuinely required.
- Client-side authorization is UX, not security — confirm the server enforces the rule, and ensure no sensitive value reaches the browser at all, since the Network tab shows everything the API returned.
- No secret survives in a client bundle; treat any public build prefix (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`) as a signal the value will ship, and confirm it's safe to expose.
- Verify every agent-suggested package by exact name with `npm view`, plus download count and maintenance, before install — hallucinated and typosquatted names slip past scanners that only know *known*-bad packages.
- Generated tests encode the same misunderstanding the code does; a green run that never sends an XSS payload or checks an unauthorized path is not a safety signal.
- Block on live XSS sinks, hardcoded or exposed secrets, and unverifiable packages; fix forward on missing edge-case tests and lower-severity gaps — and communicate which is which.
[/TAKEAWAYS]
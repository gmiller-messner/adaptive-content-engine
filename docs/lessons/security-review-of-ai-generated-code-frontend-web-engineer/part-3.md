---
title: "Part 3: Secrets and Supply Chain in the Bundle"
layout: default
nav_order: 3
parent: "Reviewing the Code Your Agent Writes for You"
grand_parent: Lessons
---

These two classes are mostly handled by tooling at a mature org — know them, confirm the pipeline caught them, and don't re-do that work by hand. But each has one residue that lands on your desk specifically.

### Secrets that ship to the browser

Anything in your client bundle is readable by anyone who opens dev tools. There is no such thing as a secret in frontend code.

An agent doesn't reliably distinguish server-only from client-safe values. Ask it to wire up an API call and it may inline a key it saw in context, or reach for an environment variable without knowing which side of the build it lives on. Patterns to catch:

- **Hardcoded keys or tokens** in a component or service file — `const API_KEY = "sk_live_..."`.
- **`process.env` values that get bundled.** In many setups, only prefixed vars (`REACT_APP_`, `NEXT_PUBLIC_`, `VITE_`) reach the client — the prefix is a signal that the value *will* ship. An agent may add the prefix to make a value "available" without registering that it's now public.
- **Secrets in error handling or logging** the agent added for debugging.

The defense is layered and mostly not manual: **git-secrets** or a pre-commit hook and CI secret scanning should catch hardcoded credentials before merge. Your job is to confirm the pipeline flagged them, and to apply the one rule tooling can't reason about — any value with a public build prefix must actually be safe to expose. If it's a real secret, it belongs behind a server route, not in the bundle.

### npm packages, including ones that don't exist

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Typosquatting</strong> — publishing a malicious package under a name close to a popular one (reactt, lodahs) hoping an install typo or a confident wrong suggestion pulls it in.</span>

SCA tooling — `npm audit`, Dependabot, Renovate, or an internal registry — handles the known-vulnerable and outdated cases well. Confirm those ran; don't hand-audit CVEs the scanner already covers.

The residue that's genuinely yours is the **hallucinated or typosquatted package name.** An agent may confidently suggest `npm install` for a package that:

- **Doesn't exist** — the model invented a plausible-sounding name.
- **Exists but isn't what it seems** — a typosquat sitting one character off a real package.

Scanning can miss both because a brand-new malicious package isn't yet *known*-bad. Before any `npm install` an agent proposes:

- **Confirm the exact name** resolves on the registry — `npm view <package>`.
- **Check download count and maintenance** — a "utility" with 40 weekly downloads and no commits in two years is a flag.
- **Compare against what you already use** — if the agent suggested a new package to do something an existing dependency handles, question why.


<div class="attack-card" data-name="Hallucinated package install">
<p><strong>Vector:</strong> Agent suggests an import and matching npm install command</p>
<p><strong>Mechanism:</strong> The model produces a plausible package name that is nonexistent or a typosquat; an attacker may have pre-registered the hallucinated name</p>
<p><strong>Example:</strong> import { debounce } from 'react-use-debounce-hook' — a name that sounds real and may not be</p>
<p><strong>Risk level:</strong> High — arbitrary code execution at install time via postinstall scripts</p>
<p><strong>Who's at risk:</strong> Any project where agent-suggested dependencies get installed without a name check</p>
</div>

<div class="lesson-nav">
<a href="../part-2/" class="lesson-nav-prev">← Part 2: The Sinks That Matter in Your Layer</a><a href="../part-4/" class="lesson-nav-next">Part 4: A Review Workflow for Generated Components →</a>
</div>


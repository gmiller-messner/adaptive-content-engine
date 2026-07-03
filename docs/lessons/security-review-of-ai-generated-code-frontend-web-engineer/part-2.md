---
title: "Part 2: The Sinks That Matter in Your Layer"
layout: default
nav_order: 2
parent: "Reviewing the Code Your Agent Writes for You"
grand_parent: Lessons
---

Not every vulnerability class needs equal attention. If your org runs `npm audit` or Dependabot, secret scanning, and lint rules in CI, a lot of the pattern-level risk is already handled. What's left for you concentrates in two places: unsafe rendering and client-side authorization.

### Unsafe rendering sinks

This is your highest-frequency exposure. <span class="term-callout"><span class="term-badge">TERM</span> <strong>XSS (Cross-Site Scripting)</strong> — injecting attacker-controlled script into a page, executed in another user's browser, typically because untrusted data reached the DOM without escaping.</span>

React escapes by default — `{userComment}` in JSX is safe. The danger is the escape hatches an agent reaches for when the default doesn't fit the ask:


<div class="attack-card" data-name="dangerouslySetInnerHTML with untrusted data">
<p><strong>Vector:</strong> User-controlled string passed to dangerouslySetInnerHTML</p>
<p><strong>Mechanism:</strong> The agent renders rich text or HTML content and bypasses React escaping to do it</p>
<p><strong>Example:</strong> <div dangerouslySetInnerHTML={{ __html: comment.body }} /> where comment.body came from an API</p>
<p><strong>Risk level:</strong> High — active XSS if the data is attacker-influenced</p>
<p><strong>Who's at risk:</strong> Any component rendering user-generated or externally-sourced HTML</p>
</div>


Sinks to flag on sight in generated code:

- **`dangerouslySetInnerHTML`** — the React one. Ask immediately: where does `__html` come from, and is it sanitized?
- **`innerHTML` / `outerHTML`** — direct DOM writes, common when an agent drops out of the React model for a "quick" manipulation.
- **`document.write`, `insertAdjacentHTML`** — same class, less common, same question.
- **URL sinks** — a `href={userValue}` that could carry `javascript:`, or an agent-built redirect from a query param.

The defense is concrete: if content genuinely must render as HTML, sanitize it with **DOMPurify** before it hits the sink — `DOMPurify.sanitize(comment.body)` — rather than trusting the source. If it doesn't need to be HTML, push back to plain `{text}` interpolation. An agent will reach for `dangerouslySetInnerHTML` because it satisfies the prompt, not because it weighed the risk.



<div class="image-placeholder" data-caption="side-by-side of the same comment component — left uses dangerouslySetInnerHTML with a raw string, right pipes it through DOMPurify — with an injected <img onerror=...> payload firing on the left only"></div>



### Client-side authorization is not authorization

This is the class where you are the only real defense, because the answer depends on *your* application's rules, not a general pattern a scanner knows.

An agent will generate a component that conditionally renders an admin panel based on a `user.role` prop, and it will look correct. Two failures hide here:

- **The check is the only check.** Hiding a button client-side is UX, not security. If the underlying API endpoint doesn't enforce the same rule server-side, anyone can call it directly through dev tools or `fetch`. The agent cannot know whether the server enforces the rule — only you and the server-side contract can.
- **The component fetches data it then hides.** A generated dashboard might request the full dataset and filter it in the client. Everything in that response is visible in the Network tab regardless of what renders. If a user shouldn't *see* a value, it must never reach the browser.

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Broken access control</strong> — code that implements the action but omits the check for whether the caller is allowed to perform it. Consistently near the top of real-world breach data.</span>

When you review a generated API integration, the question isn't "does the UI hide this correctly?" It's "does the client assume an authorization the server actually enforces, and does any sensitive value ride along in a response the browser can read?" That's a conversation with your backend contract, not something the agent reasoned about.

<div class="lesson-nav">
<a href="../part-1/" class="lesson-nav-prev">← Part 1: Why Fluent Output Earns More Scrutiny</a><a href="../part-3/" class="lesson-nav-next">Part 3: Secrets and Supply Chain in the Bundle →</a>
</div>


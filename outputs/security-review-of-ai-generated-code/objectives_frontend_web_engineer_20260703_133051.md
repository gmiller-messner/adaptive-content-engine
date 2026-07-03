## Security Review of AI-Generated Code — Objectives for Frontend / Web Engineers

By the end of this lesson, you can:

1. **Explain why fluent-looking React components and clean TypeScript deserve *more* scrutiny, not less.** Articulate why an agent-generated component that renders correctly in the browser, passes your test suite, and looks idiomatic can still contain a real vulnerability — and why that polished output is exactly what triggers automation bias.

2. **Identify the vulnerability classes that matter most in your layer of the stack.** Lead every review with unsafe rendering sinks (`dangerouslySetInnerHTML`, `innerHTML`, direct DOM writes) and missing or bypassable client-side authorization checks on what gets rendered or exposed. Recognize that your agent cannot reason about whether a user *should* see a piece of data — only you and the server-side contract can answer that.

3. **Catch secrets and sensitive values before they ship in the bundle.** Identify the patterns by which API keys, tokens, and environment values get embedded in client-side code — including those an agent may inline without flagging — and verify that values intended to stay server-side are never reachable in the browser build.

4. **Audit npm packages an agent introduces, including ones that may not exist.** For every dependency added or suggested by the agent: confirm the package exists on the registry under that exact name, check its download count and maintenance status, and flag anything that looks like a typosquat or a hallucinated package name before `npm install` runs.

5. **Apply a focused review workflow to any AI-generated component or API integration.** For each change: establish what the component is supposed to do and where its data comes from, trace every untrusted or user-controlled value to its rendering sink or API call, check for the authorization assumption the agent made on the client side, and confirm that your tooling (linter rules, `npm audit`, secret scanning) has already covered the dependency and secrets surface rather than re-doing that work manually.

6. **Recognize what your generated test suite does *not* cover from a security perspective.** Identify the cases agent-written tests routinely skip: XSS payloads as prop values, unauthenticated or unauthorized render paths, and boundary conditions on data flowing in from APIs — and know when the absence of those cases means a green test run is not a safety signal.

7. **Decide what to block at review versus fix forward.** Distinguish merge-stopping issues (an active XSS sink receiving untrusted data, a secret hardcoded in client code, an unresolvable or suspicious package) from lower-severity findings that can be addressed in a follow-up, and know how to communicate that call to your team.
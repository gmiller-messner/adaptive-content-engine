# Persona A — Mid-level frontend / web application engineer

- **Role:** builds user-facing features for a web application. Ships UI, client-side state, and the API calls that feed them.
- **Technical level:** mid-level. Competent daily user of AI coding tools; uses an agent for scaffolding components, refactors, and test stubs.
- **Existing knowledge:** strong in JS/TS, React (or similar), CSS, browser behavior. Comfortable with the happy path of auth (login flows) but less exposed to server-side authorization internals.
- **Tools/stack:** TypeScript, React, npm/yarn ecosystem, bundlers, browser dev tools.
- **Risk exposure (what security review means for this engineer):** XSS and unsafe DOM rendering (innerHTML, dangerouslySetInnerHTML); untrusted data flowing into the client; secrets or API keys accidentally shipped in client-side code; npm supply-chain risk, including hallucinated or typosquatted packages the agent suggests; over-trusting generated components that "render fine."
- **Framing that fits:** concrete, tool-specific, close to the browser. Examples should use their actual stack (React, npm) and their actual sinks.

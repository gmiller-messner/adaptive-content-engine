# Stage 3 Revision Notes
*Based on review of lesson output for Alex Chen (Software Developer) persona*

---

## Promptable Style Changes
- Soften presumptive language — use "if you're using X" and "you might" instead of stating the learner's situation as fact
- Avoid LLM writing tics — specific avoid list:
  - "This isn't theoretical" / "This is real"
  - "It's worth noting"
  - "In today's rapidly evolving landscape"
  - Rhetorical questions used as section transitions
  - Forward-looking nudges at the end of sections ("Now let's turn to...")
  - Urgency language that sounds like a mandate ("You should implement today")
- Section headings should be short, punchy, scannable — no more than 6-7 words
- Don't manufacture urgency — let the specifics create it
- Avoid commanding tone in defense sections — frame defenses as informed professional choices, not orders
- In bullet lists, lead with the key term rather than repeating a sentence structure across every item
- For technical personas, every defense must include at least one concrete implementation example — not just the concept
- For technical personas, name specific tools rather than describing actions abstractly (e.g. BeautifulSoup for HTML stripping, LangSmith for agentic logging, Dependabot/Renovate for dependency updates)
- Draw explicit connections between security concepts and general engineering principles the persona already knows — "security is just good engineering"
- Define acronyms and specialized terms on first use (e.g. SBOM)
- Where appropriate, connect individual defenses to broader trends in the field (e.g. observability)
- Parallel concepts must have consistent visual hierarchy (e.g. direct injection and indirect injection should be treated as equals visually)

---

## Source Document Gaps
- Add real-world documented examples of prompt injection attacks:
  - Bing Chat (2023) — indirect injection via webpage manipulated user interactions
  - ChatGPT plugin attacks — injection via malicious web content retrieved by plugins
  - GitHub Copilot — injection via malicious comments in code the model was asked to complete
  - Resume injection — hidden instructions in resumes submitted to AI-powered screening tools
- Clarify the actual number of affected downloads during the LiteLLM exposure window — 3.4M is total daily downloads, not affected users; malicious versions were live only a few hours
- Add remediation details and current status of the LiteLLM backdoors — were they fully closed?
- Add the full list of frameworks affected by LiteLLM as a transitive dependency (link to reference)
- Refine the dependency pinning section — the manual vs. automatic framing is a false binary; include automated tools (Dependabot, Renovate) that make deliberate updates sustainable
- Refine the supply chain summary framing — it's not that the trust model is entirely new, it's that familiar trust model failures (data/instruction confusion, implicit trust in dependencies) now have a larger and less predictable attack surface
- Add nuance about CI/CD defenses for developers who work with a dedicated security team vs. those who implement defenses themselves — knowing enough to have the right conversation with a security team is a valid learning outcome
- Clarify what "treat external content as untrusted" actually means operationally — name specific sanitization steps and tools

---

## Pipeline Features (Future Stages)
- Image/media placeholder tags at identified insertion points:
  - "Ignore all previous instructions" meme — direct injection section
  - Hidden content techniques — one image per technique showing the "invisible made visible" (e.g. white-on-white text reveal gif)
  - "The call was coming from inside the house" — LiteLLM section opener
  - Example SBOM with a compromised package highlighted
- Attack Model card visual treatment — consistent tagged block:
  ```
  [ATTACK MODEL CARD: Indirect Injection]
  ...content...
  [/ATTACK MODEL CARD]
  ```
- Glossary term callout treatment for specialized terms on first use:
  ```
  [TERM: SBOM — Software Bill of Materials]
  ...definition...
  [/TERM]
  ```
- Structured takeaways block at lesson end:
  ```
  [TAKEAWAYS]
  - Key takeaway 1
  - Key takeaway 2
  [/TAKEAWAYS]
  ```
- Rendering stage that styles all placeholder tags into formatted visual output
- Editing stage (Stage 4) for language refinement that can't be reliably prompted away

---

## Persona Profile Updates
- For technical personas, the lesson should present both implementation paths for defenses: one for developers who own their own pipeline and implement defenses directly, and one for developers who work with a dedicated security team. Knowing enough to ask the right questions and flag the right risks is a valid and important learning outcome for the latter group.

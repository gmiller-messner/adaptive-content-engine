Stage 3b Generation Standards
Applied to all lesson generation — all personas

Style Standards

Soften presumptive language — use "if you're using X" and "you might" instead of stating the learner's situation as fact
Avoid LLM writing tics — specific avoid list:

"This isn't theoretical" / "This is real"
"It's worth noting"
"In today's rapidly evolving landscape"
Rhetorical questions used as section transitions
Forward-looking nudges at the end of sections ("Now let's turn to...")
Urgency language that sounds like a mandate ("You should implement today")


Section headings should be short, punchy, scannable — no more than 6-7 words
Don't manufacture urgency — let the specifics create it
Avoid commanding tone in defense sections — frame defenses as informed professional choices, not orders
In bullet lists, lead with the key term rather than repeating a sentence structure across every item
For technical personas, every defense must include at least one concrete implementation example — not just the concept
For technical personas, name specific tools rather than describing actions abstractly (e.g. BeautifulSoup for HTML stripping, LangSmith for agentic logging, Dependabot/Renovate for dependency updates)
Draw explicit connections between security concepts and general engineering principles the persona already knows — "security is just good engineering"
Define acronyms and specialized terms on first use using the TERM tag convention below
Where appropriate, connect individual defenses to broader trends in the field (e.g. observability)
Parallel concepts must have consistent visual hierarchy (e.g. direct injection and indirect injection should be treated as equals visually)


Output Conventions
All lessons should use the following structured placeholder tags:
Image placeholders:
[IMAGE: description of recommended visual]
Suggested insertion points:

Direct injection section — "Ignore all previous instructions" meme
Hidden content techniques — one image per technique showing the "invisible made visible" (e.g. white-on-white text reveal gif)
LiteLLM section opener — "The call was coming from inside the house"
Supply chain section — example SBOM with a compromised package highlighted

Attack model cards:
[ATTACK MODEL CARD: Attack Name]
...content...
[/ATTACK MODEL CARD]
Glossary term callouts — use on first appearance of any specialized term:
[TERM: Term — Definition]
Structured takeaways block at lesson end:
[TAKEAWAYS]
- Key takeaway 1
- Key takeaway 2
[/TAKEAWAYS]

Persona-Specific Standards
For technical personas (Alex, Morgan):
Present both implementation paths for each defense:

Path 1: For developers who own their pipeline and implement defenses directly — include concrete code-level examples and specific tools
Path 2: For developers who work with a dedicated security team — frame as knowing enough to ask the right questions and flag the right risks; knowing enough to have the right conversation is a valid and important learning outcome
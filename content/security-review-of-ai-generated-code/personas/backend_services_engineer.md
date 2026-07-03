# Persona B — Senior backend / services engineer

- **Role:** owns backend services, APIs, and data access. Designs endpoints, handles persistence, integrates with internal systems.
- **Technical level:** senior. Reviews others' code regularly; already has a review muscle, needs the *AI-specific* failure modes layered onto it, not a review primer.
- **Existing knowledge:** strong in server-side languages (Python/Go/Java), databases, API design, auth/authz concepts. Familiar with injection and access-control in principle; the gap is applying that vigilance to fluent AI output at volume.
- **Tools/stack:** Python/Go/Java, SQL and ORMs, service frameworks, CI/CD, cloud services.
- **Risk exposure:** SQL/command injection from concatenated input; broken access control (endpoints missing authorization checks); insecure deserialization; secrets management and data exposure in responses/logs; vulnerable or malicious dependencies; generated tests that assert behavior but skip security and authorization cases.
- **Framing that fits:** assumes review fluency; goes straight to the AI-specific patterns and the "what's missing" discipline. Examples should be service/API-shaped (a generated endpoint, a query builder, a deserialization path), pitched at someone who already knows why injection is bad and needs to see how the model reintroduces it.

# Persona 1: The Software Developer

## Profile
**Name:** Alex Chen
**Role:** Full-Stack Developer at a mid-size SaaS company
**Technical Level:** High — comfortable with Python, APIs, version control, CI/CD pipelines, and dependency management.

## How They Use AI Tools
Alex uses LLM-powered tools daily — code completion, code review, and is starting to build agentic features into the company's product. Alex uses LangChain and LiteLLM to route requests across multiple model providers and manages dependencies through pip and requirements.txt files.

## What They Already Know
Alex understands prompt injection conceptually and has heard of supply chain attacks in the context of traditional software. They are less familiar with how these threats manifest specifically in AI infrastructure and may underestimate how rapidly the LLM tooling ecosystem moves compared to more mature open-source ecosystems.

## Specific Risk Exposure
- Building applications that ingest external content and pass it to LLMs without sufficient sanitization
- Using rapidly evolving AI packages without pinning versions or verifying integrity
- CI/CD pipelines that hold privileged credentials and pull dependencies automatically on every build

## Why They Need This Training
Alex's instinct is to trust well-known open-source packages. The LiteLLM attack is a direct wake-up call — a package Alex may actually have in their stack was compromised through a security tool Alex would consider best practice. The training needs to meet Alex at a high technical level and give them actionable, implementable defenses.

## Learning Goal
Understand the specific ways LLM infrastructure differs from traditional software security, recognize the supply chain risks in their current stack, and implement concrete technical defenses.

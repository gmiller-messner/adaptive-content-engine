# Securing Your LLM Stack: Prompt Injection and Supply Chain Attacks for Developers

## Introduction

You're building with LangChain, routing through LiteLLM, and probably pulling in a dozen transitive dependencies you've never audited. You understand prompt injection as a concept and you've seen supply chain advisories before. But the AI tooling ecosystem has its own attack surface — one that moves faster, trusts more broadly, and fails differently than the traditional open-source stack you're used to. This lesson covers two critical threat categories and gives you specific, implementable defenses for the code you're shipping today.

---

## Part 1: Prompt Injection — The Threat That Lives in Your Input Data

### You Know the Concept. Here's What You Might Be Missing.

You've probably seen the "ignore all previous instructions" meme. Direct injection — where a user tries to override the system prompt — is the version most developers encounter first. It's visible, it's testable, and you can build reasonable defenses against it.

The variant that should concern you more is **indirect injection**, because it targets exactly the kind of application you're building: one that ingests external content and passes it to an LLM for processing.

Here's the attack model. Your application retrieves a webpage, a document, an email, a file uploaded by an end user. It passes that content to an LLM — maybe for summarization, maybe for extraction, maybe as context for an agent to act on. The LLM processes all of that text with the same weight it gives your system prompt. It has no reliable mechanism to distinguish "instructions from my developer" from "instructions embedded in this PDF by someone who anticipated I'd read it."

An attacker who knows your application reads external content can embed instructions in that content and effectively hijack your model's behavior.

### Hidden Instruction Techniques You Need to Know

These aren't theoretical. They exploit the gap between what a human reviewer sees and what an LLM processes:

- **White-on-white text** in documents or webpages — invisible when rendered, fully readable by the model
- **HTML comments** — stripped from browser rendering, present in raw HTML your scraper feeds to the LLM
- **File metadata** — fields in PDFs, DOCX files, or images that no user would inspect but the model ingests
- **Sub-pixel or tiny text** — too small to notice visually, parsed perfectly by a vision-capable model
- **Steganography** — instructions encoded in image pixel values, invisible to any visual inspection

If your application processes any user-supplied or externally fetched content, every one of these is a potential injection vector.

### Why This Gets Worse When Your App Has Agency

If you're building a chatbot that only returns text, the blast radius of a successful injection is limited — bad output, maybe a leaked system prompt. Unpleasant, but contained.

The moment your application has tool access — and if you're building agentic features, it does — the calculus changes completely. A manipulated agent doesn't just produce bad text. It takes actions:

- An agent with email access can be instructed to exfiltrate contacts or sensitive data to an external address
- An agent with code execution can run malicious scripts in your environment
- An agent with web access can submit forms, make API calls, or initiate transactions
- A coding assistant with terminal access can execute destructive commands on the host system

Think about the agents you're building. What tools do they have access to? What's the worst action they could take if an attacker controlled their next instruction? That's your threat model.

### Defenses You Can Implement Now

**1. Treat all external content as untrusted input.**
This is the same principle you apply to user input in a web application, but developers routinely forget it when the consumer is an LLM rather than a SQL parser. Any content your application retrieves — from the web, from file uploads, from email — should be treated as potentially hostile before it reaches your model.

**2. Apply the principle of least privilege to your agents.**
If your agent only needs to read emails, don't give it send access. If it needs to query a database, give it read-only credentials. Scope every tool permission to the minimum required for the task. This doesn't prevent injection — it limits the damage.

**3. Add human-in-the-loop checkpoints for irreversible actions.**
Before your agent sends an email, executes code, makes a purchase, or modifies data — require a human confirmation step. This is your circuit breaker.

**4. Sanitize and scan content before it hits the model.**
Where feasible, strip HTML comments, metadata, and hidden formatting from ingested content. This won't catch everything, but it eliminates the low-hanging injection vectors.

**5. Use explicit system prompt defenses.**
Instruct the model to flag and refuse suspicious instructions found in external content. This is not bulletproof — it's a probabilistic defense — but it raises the bar.

**6. Log everything your agent does.**
Maintain detailed records of agent actions, tool calls, and the content that triggered them. When something goes wrong, you need the forensic trail to understand what happened and why.

---

## Part 2: Supply Chain Attacks — The LiteLLM Compromise

### This One Hits Close to Home

On March 24, 2026, LiteLLM — the package you likely have in your `requirements.txt` right now, downloaded roughly 3.4 million times per day — was compromised. Two malicious versions (1.82.7 and 1.82.8) were published to PyPI and were live for only a few hours. That was enough.

If your instinct is "well, LiteLLM should have had better security" — here's the part that should unsettle you: they did. They had a security scanner (Trivy) integrated into their CI/CD pipeline. **Trivy was the attack vector.**

### The Kill Chain, Step by Step

This is worth walking through carefully because it maps directly to how your own build pipeline probably works:

1. **Weeks before the attack:** A threat actor known as TeamPCP compromised Trivy — the security scanning tool LiteLLM used in their automated build pipeline.

2. **March 24, build trigger:** LiteLLM's CI/CD pipeline ran a routine build. As part of that build, it pulled and executed the compromised version of Trivy.

3. **Credential harvest:** The malicious Trivy payload read the build server's environment variables. Sitting in those variables: the **PyPI publishing token** — the credential that authorizes pushing new package versions.

4. **Malicious publish:** Within minutes, TeamPCP used the stolen token to publish two backdoored versions of LiteLLM to PyPI.

5. **Downstream infection:** Anyone who ran `pip install litellm`, `pip install --upgrade litellm`, or whose build pipeline pulled the latest version during the exposure window got the malicious package. This includes anyone who depended on LiteLLM *transitively* — through CrewAI, DSPy, or dozens of other frameworks.

### What the Malware Actually Did

The injected code executed a three-stage attack:

- **Stage 1 — Credential harvesting:** Environment variables, API keys, SSH keys, cloud credentials, Kubernetes secrets, cryptocurrency wallet files. Everything accessible from the runtime environment.
- **Stage 2 — Lateral movement:** Attempted to reach across Kubernetes clusters the compromised system had access to.
- **Stage 3 — Persistent backdoor:** Installed a mechanism to continue receiving attacker instructions even after the initial compromise was discovered and the malicious versions were pulled.

Version 1.82.8 was especially aggressive: it installed itself as a **`.pth` file** — a Python path configuration file that executes automatically every time the Python interpreter starts. Not when you import LiteLLM. Every time Python runs. Every test, every build, every script. If the package was installed in your environment, the malware ran regardless of whether your code ever referenced it.

All exfiltrated data was encrypted and sent to a domain designed to look like a legitimate LiteLLM service.

### Why This Is Different From Traditional Supply Chain Attacks

You've seen npm and PyPI supply chain attacks before. What makes the AI ecosystem particularly vulnerable:

- **Velocity of change.** AI packages release far more frequently than mature libraries. Version churn is constant, and developers are conditioned to stay on the latest release because features and model support evolve weekly.
- **Deep transitive dependency chains.** LiteLLM is a dependency of CrewAI, DSPy, and dozens of other frameworks. You might not even know it's in your stack.
- **CI/CD as a high-value target.** Your build pipeline typically holds your most privileged credentials — publishing tokens, cloud credentials, deployment keys. It's the single point of compromise that unlocks everything downstream.
- **Trusted tools as attack surface.** The security scanner itself was the entry point. The tool that was supposed to *protect* the pipeline became the key that unlocked it.

### Defenses You Should Implement Today

**1. Pin your dependencies. All of them.**

Stop using version ranges or unpinned packages in your `requirements.txt`.

```
# Don't do this
litellm>=1.80.0

# Do this
litellm==1.82.6
```

A pinned version can't be silently replaced by a malicious release. Yes, you'll need to update manually. That's the point — updates should be deliberate, not automatic.

Use `pip freeze > requirements.txt` to capture your exact current state, then audit it.

**2. Verify package integrity with hashes.**

pip supports hash verification. Generate hashes for your pinned dependencies and enforce them:

```
litellm==1.82.6 --hash=sha256:abc123...
```

This ensures that the package you download is byte-for-byte what the maintainer published. If someone publishes a tampered version with the same version number, the hash check fails and the install aborts.

**3. Maintain a Software Bill of Materials (SBOM).**

Know every dependency in your stack — including transitive ones. Tools like `pip-audit`, `syft`, or `cyclonedx-bom` can generate an SBOM for your Python projects. When an advisory drops, you need to answer "am I affected?" in minutes, not hours.

**4. Treat your CI/CD pipeline as a high-security environment.**

Your build server probably has access to publishing tokens, cloud credentials, database secrets, and deployment keys. Treat it accordingly:

- Don't store long-lived credentials in environment variables. Use short-lived tokens or a secrets manager with scoped access.
- Audit what your pipeline downloads and executes on every run.
- Run build tools from pinned, hash-verified versions — the same discipline you apply to your application dependencies.

**5. Rotate credentials on a schedule.**

Don't wait for a known compromise. If your PyPI token, cloud credentials, or API keys are rotated regularly, a stolen credential has a limited window of usefulness. Set a rotation cadence and automate it where possible.

**6. Monitor for anomalous build behavior.**

The LiteLLM compromise was first noticed because of runaway CPU and memory in production. Build-time monitoring — unexpected network calls, abnormal resource usage, new outbound connections — can catch compromises before they reach production.

---

## Summary

Two threat categories, one underlying lesson: **the trust model that worked for traditional software doesn't hold in the LLM ecosystem.**

Your LLM-powered application trusts external content enough to pass it to a model that can't distinguish it from your instructions — that's the prompt injection surface. Your build pipeline trusts upstream packages and tools enough to pull and execute them automatically — that's the supply chain surface.

The defenses are concrete and implementable: sanitize external content before it reaches your models, scope agent permissions to the minimum, pin and hash-verify every dependency, and treat your CI/CD pipeline with the same security rigor you'd apply to a production server.

The LiteLLM attack wasn't caused by negligence. It was caused by a trust model that couldn't survive a sophisticated adversary. Audit yours before someone else does.
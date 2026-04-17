---
title: "Part 2: Supply Chain Attacks"
layout: default
nav_order: 2
parent: "requirements.txt — unpinned (dangerous)"
grand_parent: Lessons
---

### The LiteLLM Attack



<div class="image-placeholder" data-caption="&quot;The call was coming from inside the house&quot; — representing a security tool becoming the attack vector"></div>



<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply chain attack</strong> — An attack that targets not your application directly, but the dependencies, tools, or infrastructure your application trusts. If an attacker compromises something in your supply chain, they inherit the trust you've placed in it.</span>

On March 24, 2026, two malicious versions of LiteLLM were published to <span class="term-callout"><span class="term-badge">TERM</span> <strong>PyPI</strong> — Python Package Index, the standard repository where Python developers download packages via pip</span>. LiteLLM is downloaded roughly 3.4 million times per day. Within about three hours, 47,000 downloads occurred — 23,142 of those were pip installs of version 1.82.8, where the malware executed automatically during installation.

If you've used LiteLLM to route requests across model providers, this may have directly affected your stack. If you depend on CrewAI, DSPy, MLflow, OpenHands, or Arize Phoenix, LiteLLM may have been a transitive dependency you didn't even know about.

### How the Attackers Got In

This is the part that should change how you think about CI/CD security.

LiteLLM had a security scanner — Trivy — built into their automated build pipeline. Trivy was best practice. A threat actor called TeamPCP had compromised Trivy weeks earlier. When LiteLLM's pipeline ran its routine security scan on March 24, it pulled the compromised Trivy. The malicious Trivy payload read the environment variables on the build server. Sitting in those environment variables: the PyPI publishing token.

TeamPCP used that token to publish two backdoored versions within minutes.


<div class="attack-card" data-name="LiteLLM Supply Chain Attack">
<p><strong>Vector:</strong> Compromised security scanner (Trivy) in the CI/CD pipeline</p>
<p><strong>Mechanism:</strong> Malicious Trivy payload harvested the PyPI publishing token from build environment variables. Attacker used the token to publish backdoored package versions.</p>
<p><strong>Example:</strong> LiteLLM versions 1.82.7 and 1.82.8 published to PyPI on March 24, 2026</p>
<p><strong>Risk level:</strong> Critical — 47,000 downloads in ~3 hours; 88% of downstream dependents had no version pin</p>
<p><strong>Who's at risk:</strong> Any developer who ran pip install or pip upgrade during the exposure window, or whose project pulled LiteLLM as a transitive dependency</p>
</div>


### What the Malware Did

The malicious payload operated in three stages:

1. **Credential harvesting** — environment variables, API keys, SSH keys, cloud credentials, Kubernetes secrets, cryptocurrency wallet files
2. **Lateral movement** — attempted to spread across any Kubernetes clusters it could reach
3. **Persistent backdoor** — designed to survive discovery and removal of the initial payload

Version 1.82.8 was especially aggressive. It installed itself as a `.pth` file — a Python path configuration file that executes automatically every time the Python interpreter starts, regardless of whether LiteLLM is explicitly imported. Having the package installed meant the malware ran on every `python` command, every test run, every build. The persistence mechanism: `litellm_init.pth` in the Python path, and `~/.config/sysmon/sysmon.py` on systems where Kubernetes was detected.

All harvested data was encrypted and exfiltrated to a domain designed to look like an official LiteLLM service.

### Why This Matters for Your Stack

The pattern here is worth studying carefully, because it's not exotic — it's a normal supply chain operating as expected, except one link was compromised.

**Transitive dependencies are invisible attack surface.** Of the 2,337 packages on PyPI that depend on LiteLLM, 88% had no version pin. They would have automatically resolved to the compromised version. You might not even list LiteLLM in your `requirements.txt` — it might come in through LangChain, CrewAI, or another framework. Run `pip show litellm` or check `pip freeze | grep litellm` to know.

[You can check whether a specific package was affected using the FutureSearch dependency checker at futuresearch.ai/tools/litellm-checker.]

**CI/CD pipelines are the highest-value targets.** They typically hold the most privileged credentials in an organization — publishing tokens, cloud provider keys, deployment credentials. If your pipeline holds credentials as environment variables and pulls external tools without pinning, the attack surface is the same one TeamPCP exploited.

**The security tool was the attack vector.** The instinct to add a security scanner to your pipeline is correct. The instinct to trust that scanner implicitly is not. Every tool that runs in your build environment — scanners, linters, formatters — has the same access as your build scripts.

### Defense: Pin Dependencies

Pinning means specifying exact version numbers in your dependency files rather than allowing pip to resolve to the latest:

```
# requirements.txt — unpinned (dangerous)
litellm
langchain

# requirements.txt — pinned (deliberate)
litellm==1.83.0
langchain==0.2.14
```

A pinned version can't be silently replaced by a compromised release. But pinning alone creates drift — you stop getting security patches and updates. The full pattern is pinning combined with automated update tooling:

- **Dependabot** (GitHub-native) or **Renovate** (platform-agnostic) — these tools monitor your pinned dependencies and open PRs when new versions are available. Updates happen deliberately, with a diff you can review, rather than silently at install time.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

This gives you the security of pinning with the currency of automated updates. You review and merge dependency updates the same way you review code changes.

**If you work with a dedicated security team**, the question to raise: "Are our Python dependencies pinned in production, and do we have automated tooling to surface updates for review?"

### Defense: Secure Your Build Environment

CI/CD pipelines deserve the same security attention as production infrastructure. Concrete steps:

- **Scope credentials to minimum permissions.** If a build step only needs to publish packages, it doesn't need cloud deployment keys. If it only needs to run tests, it doesn't need the publishing token.
- **Don't store long-lived secrets in environment variables if you can avoid it.** Use short-lived, scoped credentials — OIDC tokens for cloud access, per-job publishing tokens that expire. GitHub Actions supports OIDC for AWS, GCP, and Azure. PyPI supports trusted publishing via OIDC, eliminating the need for a stored API token entirely.
- **Pin your build tools, not just your dependencies.** The Trivy compromise worked because the pipeline pulled the latest version of the scanner. Pin your scanners, linters, and build tools to specific versions or verified hashes.
- **Audit what runs with elevated access.** Every external tool in your pipeline — security scanners, code formatters, dependency analyzers — has access to the same environment variables as your build scripts. Catalog what tools run and what they can see.
- **Monitor for unexpected outbound connections.** The LiteLLM malware exfiltrated data to an attacker-controlled domain. Network egress monitoring in your build environment can flag this.

**If you work with a dedicated security team**, the questions to bring: "What external tools run in our build pipeline, and how are they pinned?" and "What credentials are available as environment variables during builds, and do they all need to be?"

### Defense: Verify and Monitor

- **Hash verification** — use `--require-hashes` with pip to confirm that downloaded packages match known-good digests. This detects tampering between the maintainer publishing a version and you installing it.

```
# requirements.txt with hash verification
litellm==1.83.0 \
    --hash=sha256:abc123...
```

- **<span class="term-callout"><span class="term-badge">TERM</span> <strong>SBOM</strong> — Software Bill of Materials, a comprehensive record of every component and dependency in your software stack</span>** — maintain one so you know immediately what's in your stack when a vulnerability is announced. Tools like `syft`, `cyclonedx-bom`, or GitHub's built-in dependency graph can generate these.
- **Credential rotation on a schedule** — don't wait for a known compromise. If credentials are rotated regularly, stolen tokens have a shorter useful life. The LiteLLM attackers needed the PyPI token to be valid at the moment they stole it. Frequent rotation narrows that window.

### The Broader Pattern

The LiteLLM attack didn't reveal a new kind of trust failure. Implicit trust in dependencies and the confusion between data and instructions are problems software engineering has always navigated. What's different is the blast radius. AI development stacks are deep, move fast, and chain together packages that themselves chain together other packages. A compromised security scanner in one project's pipeline becomes a backdoor in thousands of downstream environments within hours.

The trust model isn't new. The attack surface is.

---

## Summary

Prompt injection and supply chain attacks exploit different trust boundaries, but the engineering response is similar: treat trust as something that must be verified, not assumed.

For prompt injection: the LLM cannot distinguish instructions from data. Every piece of external content entering the context window is a potential injection vector. Defense is layered — structural separation in prompts, input sanitization, system prompt hardening, least privilege for tool access, and human-in-the-loop checkpoints for irreversible actions.

For supply chain: every dependency you install, every tool that runs in your build, inherits a level of trust. The LiteLLM attack demonstrated that a single compromised link — a security scanner — could cascade into 47,000 infected installations in three hours. Defense is also layered — pinning with automated update review, scoped and rotated credentials, hash verification, and treating build environments as high-security infrastructure.


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li>LLMs cannot distinguish instructions from data — this is architectural, not a bug to be patched. Every piece of external content in the context window is a potential injection vector.</li>
  <li>Indirect injection is the higher-risk variant because the user is the victim, not the attacker — and it scales through any content the LLM retrieves.</li>
  <li>Sanitize before the context window: strip HTML with BeautifulSoup, scan for injection patterns with regex, and structurally separate retrieved content from instructions using explicit delimiters.</li>
  <li>System prompt defenses add a layer but are not sufficient alone — layer them with sanitization and structural separation.</li>
  <li>Grant agents only the permissions they need. Require human approval before irreversible actions. Log everything.</li>
  <li>Pin your dependencies to exact versions and use Dependabot or Renovate to surface updates for deliberate review.</li>
  <li>Treat CI/CD pipelines as high-security environments: scope credentials, pin build tools, audit what runs with elevated access.</li>
  <li>The LiteLLM attack compromised 47,000 installations in three hours through a trusted security scanner. Check your transitive dependencies — <code>pip freeze | grep litellm</code> — and verify whether your downstream packages pin their LiteLLM version.</li>
  <li>Every tool that runs in your build environment has access to your build environment's secrets. Audit accordingly.</li>
  </ul>
</div>

<div class="lesson-nav"><a href="../part-1/" class="lesson-nav-prev">← Part 1: Prompt Injection</a><span class="lesson-nav-next"></span></div>

---
title: "Part 5: Supply Chain — Hardening Your Stack"
layout: default
nav_order: 5
parent: "LLM Security for Developers: Prompt Injection and Supply Chain Attacks"
grand_parent: Lessons
---

### Pin Dependencies and Automate Updates

If your `requirements.txt` says `litellm>=1.80.0` or just `litellm`, you're telling pip to resolve to the latest version at install time. During the LiteLLM exposure window, "latest" meant "compromised."

Pin to exact versions:

```
# requirements.txt
litellm==1.82.6
langchain==0.2.14
beautifulsoup4==4.12.3
```

The obvious objection: pinning means you fall behind on updates. That's solved with automated update tooling:

- **Dependabot** (GitHub-native) or **Renovate** (self-hosted or GitHub App) — both monitor your pinned dependencies and open PRs when new versions are available
- Updates arrive as reviewable PRs with changelogs, not as silent resolution changes at install time
- You can configure update schedules, auto-merge policies for patch versions, and require CI to pass before merging

The full pattern is pinning + automated update tooling. Pinning alone without an update strategy leads to dependency drift. Automated updates without pinning gives you no control over what version you're actually running.

**If you work with a security team:** The question to raise is whether your team's dependency management policy distinguishes between AI infrastructure packages (which move fast and have deep dependency trees) and more stable dependencies. An update that's routine for `requests` might be high-risk for a package in the LLM tooling ecosystem that releases multiple times per week.

### Protect Your Build Environment

<span class="term-callout"><span class="term-badge">TERM</span> <strong>CI/CD pipeline</strong> — Continuous Integration / Continuous Deployment. The automated system that builds, tests, and deploys your code. Typically holds the most privileged credentials in an organization.</span>

CI/CD pipelines were the highest-risk targets in the LiteLLM attack because they hold publishing tokens, cloud credentials, and API keys — usually as environment variables.

**If you own your pipeline directly:**

- **Audit what runs with elevated access.** The LiteLLM attack worked because Trivy — an external tool — ran inside the build environment with access to environment variables. List every external tool in your pipeline and ask: does this need access to credentials? Can it be run in an isolated stage?
- **Scope credentials to the minimum needed.** A build step that runs tests doesn't need a PyPI publishing token. Publishing tokens should only be available in the publishing step, not the entire pipeline.
- **Pin your CI/CD tools too.** If your pipeline pulls `trivy:latest`, you get whatever was most recently published. Pin to a specific version and hash:

```yaml
# GitHub Actions example
- uses: aquasecurity/trivy-action@0.28.0
  with:
    image-ref: 'your-image:latest'
```

- **Rotate credentials on a schedule.** Don't wait for a known compromise. If publishing tokens are rotated regularly, a stolen token has a shorter useful life. Build this into your operational cadence.
- **Monitor for unexpected outbound connections.** The LiteLLM malware exfiltrated data to an attacker-controlled domain. Network monitoring on build environments can catch this pattern.

**If you work with a security team:** The questions to surface:

- "What external tools run in our build pipeline, and how are they pinned?"
- "What credentials are available as environment variables during builds, and do they need to be?"
- "Do we have network egress monitoring on build environments?"
- "How often are publishing tokens and CI/CD secrets rotated?"

Understanding enough to ask these questions is a legitimate and important security contribution. Many CI/CD vulnerabilities persist not because security teams don't know how to fix them, but because no one raised the specific risk.

### Maintain a Software Bill of Materials

<span class="term-callout"><span class="term-badge">TERM</span> <strong>SBOM (Software Bill of Materials)</strong> — A record of every dependency in your application stack, including transitive dependencies. Analogous to an ingredients list — it tells you what's actually in the build.</span>



<div class="image-placeholder" data-caption="Example SBOM output with a compromised package version highlighted"></div>



When a supply chain attack drops, the first question is always: "Are we affected?" An SBOM lets you answer that in minutes rather than hours. Tools like `pip-audit`, `syft`, or `cyclonedx-bom` can generate SBOMs from your Python environment.

If 88% of LiteLLM's downstream dependents had no version pin, a significant number of those teams probably also didn't know LiteLLM was in their dependency tree at all.

### Verify Package Integrity

Use hash verification to confirm that what you downloaded is what the maintainer published:

```
# requirements.txt with hashes
litellm==1.83.0 \
    --hash=sha256:abc123...
```

`pip install --require-hashes -r requirements.txt` will refuse to install any package whose hash doesn't match. This means that even if an attacker publishes a malicious version under a legitimate version number, the install fails if the hash doesn't match what you've recorded.

---


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li><strong>Prompt injection is a structural problem, not a fixable bug.</strong> LLMs cannot architecturally distinguish instructions from data. Every defense is a mitigation that raises the cost of attack — not a solution that eliminates the vulnerability class.</li>
  <li><strong>Every piece of external content is a potential injection vector.</strong> If your application retrieves web pages, documents, emails, or code and passes them to an LLM, treat all of that content as untrusted. Sanitize it, delimit it structurally in your prompts, and never pass raw retrieved content into system prompts.</li>
  <li><strong>Agentic systems need least privilege and human checkpoints.</strong> The more tools an agent can access, the higher the impact of a successful injection. Scope permissions tightly and require human approval before any irreversible action.</li>
  <li><strong>Pin your dependencies, automate your updates.</strong> <code>litellm>=1.80.0</code> in a requirements file is an open invitation for a compromised version to enter your stack silently. Pin exact versions and use Dependabot or Renovate so updates arrive as reviewable PRs.</li>
  <li><strong>Your CI/CD pipeline is a high-value target.</strong> Audit what external tools run in your build environment, what credentials they can access, and whether those credentials are scoped to only the stages that need them. The LiteLLM attack worked because a security scanner had access to a publishing token.</li>
  <li><strong>Know your dependency tree.</strong> Maintain an SBOM. If you can't answer "does my project depend on package X?" in under five minutes, you can't respond effectively when that package is compromised.</li>
  </ul>
</div>

<div class="lesson-nav">
<a href="../part-4/" class="lesson-nav-prev">← Part 4: Supply Chain Attacks — The LiteLLM Breach</a>
</div>


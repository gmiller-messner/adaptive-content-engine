---
title: "Part 4: Three Habits That Change Everything"
layout: default
nav_order: 4
parent: "AI Security for Builders: What Every Prompt and Every Install Costs You"
grand_parent: Lessons
---

You don't need to become a security engineer. You need a small number of habits that interrupt the moments where trust gets extended without verification.

### Habit 1: The Verification Pause

Before approving any action where Claude Code or Cowork wants to:
- Install a package
- Run a script
- Access an external system
- Execute a terminal command you don't fully understand

Pause. Ask yourself: **"Do I understand what this is doing, or am I just trusting that the AI knows best?"**

This is the single highest-impact habit. The distinction between "Claude Code suggested this" and "I have verified this is safe" is the difference between implicit trust and informed consent.

Concrete things to check:
- **For package installs:** What package is being installed? What version? Have you heard of it? A quick search for "[package name] security" or checking the package's PyPI page (look at download counts, maintenance activity, and recent version history) takes 30 seconds and can surface obvious problems.
- **For scripts and commands:** If the command includes `curl | bash`, `wget`, `eval`, or downloads and executes something from a URL, that's a higher-risk action that deserves scrutiny.
- **For environment access:** If the tool wants to read or use credentials, ask whether it actually needs that access for the task at hand.

### Habit 2: Know and Protect Your Credentials

Your `.env` files and environment variables are the highest-value targets in your working environment. A few practices that make a real difference:

- **Audit what's in your `.env` files.** Open them. Know what credentials are there. Ask yourself: does this project actually need all of these, or did they accumulate over time?
- **Don't store credentials you're not actively using.** If a project doesn't need your AWS keys, don't leave them in the environment.
- **Use scoped credentials when possible.** If a service lets you create API keys with limited permissions (many do), use a key that can only do what this specific project needs — not your all-access admin key.
- **Rotate credentials periodically.** Even without a known compromise, regularly generating new API keys and tokens means that if one was stolen at some point, its useful life is limited. Set a calendar reminder if that helps.

If you manage your own infrastructure:
These practices apply directly. Consider using a secrets manager (like `dotenv-vault`, AWS Secrets Manager, or 1Password's developer tools) instead of raw `.env` files, which adds a layer between your credentials and anything running in the environment.

If you work with a security or engineering team:
Flagging the right questions is valuable. "What credentials are exposed in our build environments?" and "Do our development environments have access to production credentials?" are the kinds of questions that help security teams prioritize.

### Habit 3: Check Versions Before You Install

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Dependency Pinning</strong> — Specifying an exact version number for a package instead of pulling whatever the latest version is. A pinned version can't be silently replaced by a compromised newer release.</span>

When Claude Code or Cowork installs a dependency, it might pull the latest version by default. In the LiteLLM case, that default behavior is exactly what delivered the compromised package to 88% of downstream projects.

What you can do:
- **When you see a package being installed, note the version number.** If something gets installed and you later need to reinstall or share the project, you want to be able to specify "install version X" rather than "install latest."
- **Use `pip freeze > requirements.txt`** after your project is working. This captures the exact versions of everything installed, so the environment can be reproduced precisely. If you're sharing the project or deploying it, this file is what prevents "install latest" from pulling something unexpected.
- **When reviewing a `requirements.txt` or `pyproject.toml`, look for pinned vs. unpinned entries.** `litellm==1.82.6` is pinned (safe version, exact). `litellm` or `litellm>=1.80` is unpinned — it will resolve to whatever is newest, which might be compromised.

If you want to stay current without pulling blindly:
Tools like <span class="term-callout"><span class="term-badge">TERM</span> <strong>Dependabot</strong> — A GitHub tool that automatically opens pull requests when your dependencies have updates available, so you can review and approve updates deliberately</span> and Renovate automate the process of checking for updates and presenting them for review. Pinning + automated update tooling is the full pattern: you get stability by default and updates by choice.

---

## Pulling It Together

Two categories of threat, one shared root cause: misplaced trust.

**Prompt injection** exploits the LLM's inability to distinguish your instructions from instructions hidden in content it processes. When your AI tools have access to your terminal, your files, and your credentials, a successful injection can take real actions — not just generate bad text.

**Supply chain attacks** exploit the chain of dependencies your projects rely on. When a package you trust — or a package that something you trust depends on — gets compromised, the malware inherits all the access your environment provides. The LiteLLM attack reached 47,000 downloads in three hours because the ecosystem's default behavior is to trust and install the latest version without verification.

Both threats are amplified by speed. Moving fast is your strength — and it's exactly what these attacks exploit. The goal isn't to slow you down across the board. It's to identify the specific moments where a five-second pause makes a meaningful difference.


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li>LLMs cannot distinguish trusted instructions from malicious content they're asked to process — this is architectural, not a bug to be fixed. Every time your AI tool reads external content, that content could contain injected instructions.</li>
  <li>Every dependency installation is a security decision. When Claude Code suggests installing a package, you're extending trust to that package and everything it depends on.</li>
  <li>Your <code>.env</code> files and environment variables are the first thing malware targets. Know what's in them, remove what you don't need, and rotate credentials on a schedule.</li>
  <li>Pin your dependency versions. Use <code>pip freeze > requirements.txt</code> to capture exact versions, and don't default to "install latest" in projects that matter.</li>
  <li>Apply the verification pause: before approving installs, scripts, or system access, distinguish between "Claude Code suggested this" and "I have verified this is safe."</li>
  <li>Know the signs of compromise: unexpected CPU spikes, unfamiliar files, unusual network activity. If something looks wrong, treat all credentials in that environment as compromised and rotate immediately.</li>
  </ul>
</div>

<div class="lesson-nav"><a href="../part-3/" class="lesson-nav-prev">← Part 3: Your Environment Is the Target</a><span class="lesson-nav-next"></span></div>

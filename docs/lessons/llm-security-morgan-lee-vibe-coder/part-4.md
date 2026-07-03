---
title: "Part 4: Habits That Fit How You Work"
layout: default
nav_order: 4
parent: "Security Decisions You're Already Making"
grand_parent: Lessons
---

### Before Approving an Install

When Claude Code or Cowork suggests installing a package, that's a security decision point. You don't need to audit the source code — but you do need a moment of verification.

**If you manage your own environment:**

- **Read the package name carefully.** Typosquatting — publishing a malicious package with a name nearly identical to a popular one — is a common attack. `reqeusts` instead of `requests`. One character difference, completely different code.
- **Check the version.** If the tool is installing a specific version, a quick search can tell you whether that version is current and legitimate. If it's installing "latest" with no version specified, that's the unpinned dependency pattern that exposed 88% of LiteLLM's downstream users.
- **Ask what it's installing and why.** Claude Code can explain what a package does and why it's needed. If the answer is vague or the package isn't well-known, that's a reason to look more closely before approving.
- **Consider pinning versions in your requirements files.** Instead of `litellm` (which resolves to whatever the latest version is), `litellm==1.83.0` locks to a specific, verified version. Tools like <span class="term-callout"><span class="term-badge">TERM</span> <strong>Dependabot</strong> — an automated tool that monitors your dependencies and opens pull requests when updates are available, so you update deliberately rather than silently</span> or Renovate can notify you when a pinned dependency has a newer version, so you're choosing when to update rather than getting whatever's newest at install time.

**If you work with an engineering team:**

The habits above still apply to your own prototyping environment. When handing prototypes off to engineering, flag what dependencies you've added and whether they're pinned. Useful questions for your engineering team: "Do we have a process for reviewing new dependencies before they go into production?" and "Are our requirements files pinned, and do we have automated update tooling running?"

### Before Approving Agentic Actions

Any time an AI agent wants to do something beyond generating text — install a package, run a script, make a network request, access an external system — that's a moment to pause.

The distinction that matters: **"Claude Code suggested this" is not the same as "I have verified this is safe."**

This isn't about distrust. Claude Code is a powerful tool, and most of the time its suggestions are exactly right. But the model doesn't have security context about your environment. It doesn't know what credentials are in your `.env` file, what systems your machine has access to, or whether the code it's about to run came from a source that might have been tampered with.

A practical checkpoint before approving consequential actions:

- **What is this action doing?** Can you describe it in plain language?
- **What does it have access to?** Will it run in an environment with API keys, cloud credentials, or access to internal systems?
- **Is it reversible?** Installing a package, sending an email, writing to a database — these are harder to undo than generating a text file.
- **Did it come from external content?** If the agent is acting on instructions it found in a document, webpage, or code file it retrieved, that content could contain indirect injection.

If you're building prototypes that interact with real services — sending emails, hitting APIs, writing to databases — consider whether the AI agent needs access to production credentials, or whether a test environment with limited permissions would work. This is the <span class="term-callout"><span class="term-badge">TERM</span> <strong>principle of least privilege</strong> — granting a system or tool only the minimum permissions it needs to do its job, so that if it's compromised, the damage is contained</span>.

### Your Personal Security Checklist

Three habits that protect you without slowing you down:

**1. Audit your `.env` file this week.** Open it. Read what's in it. For each credential, ask: does this project actually need this? Remove anything that's there from a previous project or that you added while experimenting. Every credential in that file is reachable by any code that runs in that environment — including any package you install.

**2. Pin your dependencies.** Next time you set up a project or hand one off to engineering, use exact version numbers in your requirements file. `package==1.2.3` instead of just `package`. This one change would have protected 88% of LiteLLM's downstream users.

**3. Make "approve" a conscious verb.** When Claude Code asks to install something or run something, let that be a moment — not a speed bump, but a checkpoint. Read what it's asking. If it's installing packages, check the names and versions. If it's running a script, understand what it does. If it's accessing an external system, consider what credentials are exposed.

### Summary

Prompt injection exploits the fact that LLMs can't distinguish your instructions from instructions hidden in content they process. This is an architectural property of how these models work, not a bug. Indirect injection — where malicious instructions are embedded in external content the model reads — is the more dangerous variant because you won't see it coming.

Supply chain attacks target the tools and packages your projects depend on. The LiteLLM attack demonstrated how a single compromised package, live for just three hours, could reach 47,000 environments — and how the lack of version pinning amplified the blast radius to thousands of downstream projects.

Both of these threats intersect with how you work. Every package install and every agentic action is a security decision. The good news: a few specific habits — auditing your credentials, pinning your dependencies, and making "approve" a conscious checkpoint — meaningfully reduce your exposure without changing how you build.


<div class="takeaways">
  <p class="takeaways-header">Key Takeaways</p>
  <ul>
  <li>LLMs cannot reliably distinguish between your instructions and instructions hidden in external content — this is architectural, not a fixable bug</li>
  <li>Indirect prompt injection is the more dangerous variant: malicious instructions embedded in documents, web pages, or code that the model processes without your knowledge</li>
  <li>Coding agents with terminal access amplify the risk — a successful injection can execute real commands, install packages, and access credentials in your environment</li>
  <li>A supply chain attack targets something your project trusts (a package, a tool) rather than your project itself — compromising one popular package can reach thousands of downstream environments</li>
  <li>Every dependency installation is a security decision: check the package name, check the version, and understand why it's being installed</li>
  <li>Pin your dependency versions — <code>package==1.2.3</code> instead of <code>package</code> — so that a compromised release can't silently enter your environment</li>
  <li>Audit your <code>.env</code> file and remove credentials you don't actively need — every credential in that file is reachable by any code that runs in that environment</li>
  <li>"Claude Code suggested this" is not the same as "I have verified this is safe" — make approval a conscious checkpoint, especially for installs, script execution, and external system access</li>
  <li>Know the warning signs of a compromised environment: unexpected CPU usage, unfamiliar files, processes you didn't start, unusual outbound network connections</li>
  <li>If you suspect a compromise: disconnect from the network, stop running commands, inventory your exposed credentials, rotate them immediately, and notify your engineering or security team</li>
  </ul>
</div>

<div class="lesson-nav">
<a href="../part-3/" class="lesson-nav-prev">← Part 3: Your Environment Is a Target</a>
</div>


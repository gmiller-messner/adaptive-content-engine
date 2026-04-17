---
title: "Part 3: Supply Chain Attacks"
layout: default
nav_order: 3
parent: "LLM Security for People Managers: Protecting Your Team's Data"
grand_parent: Lessons
---

<span class="term-callout"><span class="term-badge">TERM</span> <strong>Supply chain attack</strong> — An attack that targets not your application or tool directly, but the dependencies, libraries, or build tools it relies on. If the attacker compromises something your tool trusts, they inherit that trust.</span>

You don't need to understand supply chain attacks at a technical level, but you should know they exist and why they matter for your team.

### The Short Version

Modern software is built on layers of open-source packages. A supply chain attack compromises one of those packages — often a widely trusted one — and every application that depends on it inherits the compromise.

In March 2026, a popular AI package called LiteLLM was compromised through its own security scanner. For about three hours, anyone who installed or updated the package received a version that stole credentials, API keys, and cloud access tokens. The package is downloaded roughly 3.4 million times per day and is a dependency of major AI projects. 88% of the packages that depend on LiteLLM had no version controls that would have prevented them from automatically pulling the compromised version.

The attackers didn't need to attack thousands of applications individually. They attacked one trusted package and gained access to everything downstream.

### Why This Matters for You

You probably aren't installing Python packages. But your team might be. And the tools you use — including AI assistants, Slack integrations, and internal platforms — all depend on supply chains like this.

Two things you can do with this knowledge:

- **Ask your team and your security partners the right questions.** "What external tools and packages run in our build pipelines? Are dependency versions pinned? What happens if one of our dependencies is compromised — would we know?" These questions signal that you understand the risk and help your security team prioritize.
- **Recognize the signs if your team encounters something unusual.** If a team member reports unexpected CPU spikes, unfamiliar processes, or strange network activity after a routine update, take it seriously and escalate to your security team immediately. The LiteLLM compromise was first noticed because systems started crashing from resource exhaustion.

<div class="lesson-nav"><a href="../part-2/" class="lesson-nav-prev">← Part 2: Your Data Is the Risk</a><a href="../part-4/" class="lesson-nav-next">Part 4: What You Can Do →</a></div>

---
title: "Part 3: Your Environment Is a Target"
layout: default
nav_order: 3
parent: "Security Decisions You're Already Making"
grand_parent: Lessons
---

### Credentials Hiding in Plain Sight

If you're building tools and prototypes, your working environment likely contains credentials that would be valuable to an attacker. Take a moment to think about what's accessible from the machine or environment where you run Claude Code:

- **API keys** — for OpenAI, Anthropic, Stripe, Twilio, or other services you've integrated
- **Cloud credentials** — AWS, GCP, or Azure tokens that might live in environment variables or config files
- <span class="term-callout"><span class="term-badge">TERM</span> <strong>.env files</strong> — configuration files commonly used to store environment variables including API keys, database URLs, and other secrets, usually kept in a project's root directory</span> containing secrets for the tools and services your prototypes connect to
- **Database connection strings** — URLs with embedded usernames and passwords
- **Access tokens** for GitHub, Slack, or internal systems

These are exactly what the LiteLLM malware harvested first. A compromised package running in your environment doesn't need special access — if a credential is available as an environment variable or in a file the process can read, it's reachable.

This extends beyond malicious packages. If you're pasting code snippets, error logs, or configuration details into AI tools, consider what's included. Samsung engineers pasted proprietary source code into ChatGPT for debugging help and inadvertently exposed confidential intellectual property. According to research from 2025, 77% of enterprise employees who use AI have pasted company data into chatbot queries. Some of that data leaves the organization permanently.

### Signs Something Might Be Wrong

If a compromised package does end up in your environment, there are observable signals. None of these individually confirms a compromise, but they're reasons to stop and investigate:

- **Unexpected CPU usage** — your fan spinning up when you're not running anything intensive, or processes pegging CPU at 100%. The LiteLLM malware caused exactly this.
- **Unfamiliar files** — files you don't recognize appearing in your project directory, your Python site-packages, or your home directory. The LiteLLM malware specifically created a `litellm_init.pth` file in the Python path and a persistence script at `~/.config/sysmon/sysmon.py`.
- **Processes you didn't start** — background processes or network connections that don't correspond to anything you're running.
- **Unexpected outbound network activity** — if you have a network monitor, connections to domains you don't recognize. The LiteLLM malware exfiltrated data to a domain designed to look like a legitimate LiteLLM service.

### What to Do If Something Looks Wrong

If you see multiple warning signs and suspect your environment may be compromised, here's the sequence:

1. **Disconnect from the network** — if malware is exfiltrating data, cutting the connection limits what can be sent out
2. **Stop running commands** — don't run more code, builds, or installs in that environment until you've investigated
3. **Inventory your exposed credentials** — identify every API key, cloud credential, and access token that was accessible from that environment
4. **Rotate those credentials** — change every key and token that was accessible, even if you're not certain they were stolen. Assume they were.
5. **Tell your engineering or security team** — they can do forensic analysis, check for persistence mechanisms, and help determine the scope

If you work with an engineering team, this is exactly the kind of situation where knowing what to report matters as much as knowing how to fix it. "I noticed unexpected CPU usage and unfamiliar files after a package install — here's what I was working on and what credentials were in that environment" gives a security team everything they need to start investigating.

<div class="lesson-nav"><a href="../part-2/" class="lesson-nav-prev">← Part 2: Supply Chain Attacks — The Threat You Haven't Met</a><a href="../part-4/" class="lesson-nav-next">Part 4: Habits That Fit How You Work →</a></div>

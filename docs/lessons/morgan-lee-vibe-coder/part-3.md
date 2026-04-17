---
title: "Part 3: Your Environment Is the Target"
layout: default
nav_order: 3
parent: "AI Security for Builders: What Every Prompt and Every Install Costs You"
grand_parent: Lessons
---

### What's Sitting in Your Working Environment

Take a mental inventory. If you're building tools and prototypes with Claude Code, your working environment might contain:

- **API keys** for services like OpenAI, Anthropic, Stripe, Twilio, or others — often stored in `.env` files or set as environment variables
- **Cloud credentials** for AWS, GCP, or Azure
- **Database connection strings** with usernames and passwords
- **Access tokens** for internal tools, CI/CD pipelines, or third-party services
- **SSH keys** that grant access to servers or repositories

These are exactly what the LiteLLM malware was designed to harvest. Environment variables and `.env` files are the first thing credential-stealing malware looks for, because developers routinely store secrets there for convenience.

### What Compromise Looks Like

A compromised package doesn't announce itself. But there are signs you can learn to notice:

- **Unexpected CPU usage or memory spikes** — the LiteLLM malware caused runaway processes and containers crashing from memory exhaustion. If your machine suddenly slows down or fans spin up when you haven't changed anything, that's worth investigating.
- **Unfamiliar files** — the LiteLLM malware specifically created a `litellm_init.pth` file in the Python path and a persistence script at `~/.config/sysmon/sysmon.py`. More generally, unfamiliar files appearing in your `site-packages` directory, your Python path, or config directories are a red flag.
- **Unusual outbound network activity** — malware needs to send stolen data somewhere. If you notice unexpected network connections (tools like Little Snitch on macOS or `netstat` on any system can help), that warrants investigation.
- **Packages you don't recognize** in your installed dependencies — run `pip list` periodically and look for anything you don't remember installing or can't explain.

### If You Suspect Compromise

If something looks wrong, these are the immediate steps:

1. **Disconnect from the network** if possible — this limits further data exfiltration
2. **Don't just uninstall the suspect package** — as the LiteLLM case showed, malware can establish persistence mechanisms that survive package removal
3. **Treat every credential accessible from that environment as compromised** — rotate API keys, cloud credentials, access tokens, database passwords. All of them.
4. **If you're at a company with a security team, contact them immediately** — they need to know, and they'll have a process for this
5. **If you're working solo or at an early-stage startup**, rotate all credentials, rebuild the environment from scratch (don't just clean the existing one), and audit what the compromised environment had access to

The remediation bar is high because the consequences of assuming "it's probably fine" are worse than the cost of rotating credentials.

---

<div class="lesson-nav"><a href="../part-2/" class="lesson-nav-prev">← Part 2: Supply Chain Attacks</a><a href="../part-4/" class="lesson-nav-next">Part 4: Three Habits That Change Everything →</a></div>

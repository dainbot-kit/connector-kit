# Connecting tools, apps and agents on a Mac + GitHub
Researched 13 Nov 2026 (AWST) from current official docs. Research only; nothing built or changed.

## Bottom line
For a private local AI agent on a Mac: run things on the Mac, call GitHub outbound (API, gh CLI, GitHub MCP server), and avoid opening a public hole into the machine. Poll the API or use GitHub Actions instead of inbound webhooks.

## 1. Plain API calls
- GitHub REST (https://api.github.com) and GraphQL; official `gh` CLI (`gh auth login`, `gh api`).
- Tokens: fine-grained personal access token (one owner, selected repos, expiry) for personal use; GitHub App for long-running services (1-hour tokens).
- Works today: yes. Cost: free; 5,000 requests/hour authenticated.
- Risk: a stolen broad token can change repos. Keep it narrow, store in Keychain/env.
- Fit: the foundation. Docs: https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api , https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

## 2. MCP (Model Context Protocol)
- Open standard so an AI app (host) can use tools/data from programs (servers). JSON-RPC; local "stdio" or remote "Streamable HTTP" (with OAuth).
- Current spec 2026-07-28; governed under the Agentic AI Foundation (Linux Foundation). https://modelcontextprotocol.io/specification/2026-07-28
- GitHub official MCP server: remote https://api.githubcopilot.com/mcp/ (OAuth, can be read-only) or local Docker image. https://github.com/github/github-mcp-server
- Verified Mac hosts: VS Code, Xcode (xcrun mcpbridge), LM Studio (0.3.17+). Ollama itself isn't a host; the client app talking to it is.
- Pros: one plug for many tools, read-only/toolset limits, works with local models.
- Risks: prompt injection, tool poisoning, over-broad tokens. Use trusted servers only, start read-only, approve writes. https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html
- Cost: free (some GitHub tools need paid Copilot). Fit: very good.

## 3. Webhooks
- GitHub POSTs to a public URL on events. A home Mac needs a tunnel: smee.io (testing only, not private), Cloudflare Tunnel, ngrok (free tier with caps), Tailscale Funnel.
- Works today: yes. Risk: public attack surface; always verify signatures.
- Fit: weak as a default. Prefer GitHub Actions or polling.

## 4. Local bridges on macOS
- launchd/LaunchAgents: keep the agent running at login (won't run if Mac sleeps).
- Shortcuts CLI (`shortcuts run "Name"`), App Intents, AppleScript/JXA (needs Automation permission), Hammerspoon (Accessibility; powerful, riskier), localhost-only HTTP or sockets, folder watchers.
- Cost: free. Fit: launchd + Shortcuts + a localhost API covers most of a local agent.

## 5. Automation tools
- n8n: self-hosted Community Edition free (Docker; AI starter kit with Ollama), cloud from EUR 20/mo annual. Best for private local setup; better on the 64GB Studio than the 16GB Air. https://n8n.io/pricing/
- Apple Shortcuts: free, on-device, can call HTTPS. Strong Mac glue, weak as a full agent.
- Zapier: cloud; free 100 tasks/mo; from US$19.99/mo annual. Data leaves the Mac.
- Make: cloud; free 1,000 credits/mo; from US$9/mo. Same privacy issue.
- Raycast MCP support: unverified.

## 6. Agent-to-agent links
- A2A protocol (stable v1.0.1, under the Agentic AI Foundation; SDKs in several languages). Adoption still uneven; not needed to start. https://a2a-protocol.org/latest/roadmap/
- IBM's ACP merged into A2A (Aug 2025).
- Practical today: shared folder/queue, local HTTP API, GitHub issues/PRs as a job queue.

## 7. Browser automation (last resort)
- Playwright, Puppeteer, computer-use agents. Free tools, high fragility, site terms may restrict bots; unattended clicks can buy/delete/send. Use only when there's no API, MCP server or Shortcut.

## 8. Other methods worth knowing
- GitHub Actions self-hosted runner on the Mac: free minutes, but ONLY on private repos (public PRs can run code on your Mac).
- GitHub Copilot coding agent: cloud agent opens PRs; Pro US$10/mo, Pro+ $39, Max $100.
- Codespaces: cloud VS Code, 120 core-hours/mo free.
- Tailscale (private VPN, not Funnel): reach your Mac from your phone; free personal plan. Excellent fit.
- SSH: pair with Tailscale, don't expose port 22.
- Ollama (localhost:11434/v1) and LM Studio (localhost:1234/v1): local models with OpenAI-compatible APIs - the "brain".
- Apple Foundation Models: on-device Apple model via Swift; smaller than what a 64GB Studio can run.

## Recommended starter stacks (opinion)
A. Start now on the Air: LM Studio or Ollama + LM Studio/VS Code as MCP host + GitHub MCP server read-only (or a one-repo fine-grained token) + gh + Shortcuts. Prove it can read a repo before giving write access.
B. Keep running: A + a LaunchAgent + no-sleep energy settings + (on the Studio) self-hosted n8n with Ollama and GitHub; GitHub issues as the job queue; poll, no public webhook.
C. While you're away: B + Tailscale to check in; self-hosted Actions runner only on private repos; no public tunnel unless unavoidable.

What no model decides for you: which folders/apps it may touch, macOS permission clicks, and a test that means "done".

## Couldn't verify
Official AUD prices; Raycast MCP from Raycast's docs; full Apple Foundation Models capability list; complete list of every Mac app's MCP support; Cloudflare Tunnel free-tier limits; independent A2A adoption numbers; per-site Playwright terms.

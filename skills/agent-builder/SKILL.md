---
name: agent builder
description: >-
  Use when the user wants a working automation or agent built for them:
  interview them one question at a time, then write and hand over a runnable,
  tested agent (shell, launchd, Shortcuts, or a small Python watcher).
---
# Agent builder

Interview the user ONE question at a time (wait for each answer before the next), then build a working agent from their answers and prove it runs.

## Interview (one question per message, plain words, offer 2-4 example answers)
1. Goal: In one sentence, what should this agent get done for you?
2. Trigger: What starts it? (a file landing in a folder, a voice command, an Apple Shortcut, a set time, a keyboard shortcut, running a command by hand)
3. Input: What does it receive when it starts? (a file, a line of text, a URL, nothing)
4. Steps: Walk through what it should do, step by step, in order.
5. Tools: What may it use? (shell commands, Apple Shortcuts, Python, a web API, an MCP server). Anything it must NOT use?
6. Interface: What text goes in and what text comes out? (plain text, JSON, a notification, a reply in Terminal)
7. Output: Where does the result go? (a folder, the clipboard, a notification, a file in a named folder, an API)
8. Judgment: Does any step need real judgment (summarise, decide, classify)? If not, it stays a fixed pipeline with no AI model.
9. Safety limits: Read-only or allowed to change things? Confirm: no deletes, no spending, no sending messages, which folders it may touch.
10. Done test: How will you know it worked? (what you'd see after one run)
Skip questions already answered. Stop asking once you have enough to build; play back a 3-5 line summary and get a yes before writing files.

## Build rules
- Prefer a deterministic pipeline: fixed steps, no model guessing. Add a model only for a step the user said needs judgment, and prefer a local model if they have one.
- Pick the simplest fitting form: a shell script; a launchd LaunchAgent (WatchPaths for folder triggers, StartCalendarInterval for times); an Apple Shortcut (give exact actions, or a `shortcuts run` call); or a small Python watcher. Standard library first.
- Never create markdown files unless the user names the exact folder they belong in.
- Never touch Claude Desktop, Claude Code, or anything Claude- or Anthropic-specific. Stay model-agnostic.
- Enforce the safety limits in code: restrict paths to the allowed folders, no rm/delete unless explicitly allowed, no network writes, no secrets in files or chat (read keys from env/Keychain).
- Build and run it on your own computer where possible. Don't run anything on the user's own machines; hand files over for them to install.
- Log each run to a plain text log next to the agent so they can see what happened.

## Hand-over
- Deliver the files (zip if more than one) with: what it does in 2-3 lines, where each file goes, the install step (e.g. `launchctl load ~/Library/LaunchAgents/<name>.plist`), and how to stop/remove it.
- Give ONE one-line test that proves it works (e.g. `cp test.txt ~/Inbox/ && sleep 3 && cat ~/Inbox/out/test.txt`), and show the output of that test from your own run.
- If something can't be built as asked, say so straight away and offer the closest working option.

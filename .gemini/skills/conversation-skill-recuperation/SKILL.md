---
name: conversation-skill-recuperation
description: >-
  Search, list, and recover lost or archived IDE conversations across the 3-tier architecture (SQLite DBs and JSONL log files).
---

# Conversation Recovery Copilot

## Overview

This skill allows the agent to bypass visual IDE limitations, page truncation limits, and orphaned trajectories by listing, searching, and recovering entire past conversations across the **3-tier persistence architecture** of the Antigravity IDE:

1. **Active Conversations (`Active (SQLite)`):** Standard `.db` files located in the `~/.gemini/antigravity-ide/conversations` folder. Used for currently active and recent sessions.
2. **Historical Active Conversations (`Historical Active (JSONL)`):** Full, untruncated `transcript.jsonl` text logs located in `~/.gemini/antigravity-ide/brain/<id>/.system_generated/logs/`. Retained even when database connections are closed.
3. **Archived Trajectories (`Archived (Protobuf)`):** Compressed `.pb` binary snapshots stored inside `conversations/` to save memory. 

By querying both SQL tables and scanning JSONL streams fully offline, this skill indexes search results and compiles complete transcripts with **zero remote API calls** and **zero token costs**.

## Quick Start

You can run this skill instantly using `uv run` to ensure dependency isolation (like the `rich` UI library) without activating manual virtual environments:

```bash
# 1. List all active and historical conversations
uv run /Users/arianstoned/Developer/uni_semestre_4/EpidemicResearch/.gemini/skills/conversation-skill-recuperation/scripts/recover_conversations.py list

# 2. Search all logs (DBs & JSONLs) for a phrase
uv run /Users/arianstoned/Developer/uni_semestre_4/EpidemicResearch/.gemini/skills/conversation-skill-recuperation/scripts/recover_conversations.py search "Alcon"

# 3. Recover a specific chat (either DB or JSONL) as Markdown
uv run /Users/arianstoned/Developer/uni_semestre_4/EpidemicResearch/.gemini/skills/conversation-skill-recuperation/scripts/recover_conversations.py recover b4bc22b4-fbd0-4f85-923d-22d15ca21447 -o /Users/arianstoned/Developer/Workspace/conversacion_completa_oftalmologia.md
```

## Utility Scripts

### Subcommand: `list`

Scans the local `.gemini/antigravity-ide/conversations` and `.gemini/antigravity-ide/brain` folders, extracts metadata (IDs, modification times, sizes, step counts), parses step 0 (USER prompt) to extract objectives, and prints a beautiful unified table of all available local records.

### Subcommand: `search <query>`

Iterates through active database files (instantiating local SQLite FTS5 in-memory tables) and reads JSONL transcripts sequentially to identify match lines. Returns step indices, roles, and highlighted context snippets of all matching entries.

### Subcommand: `recover <id> --output <path.md>`

Determines the storage tier of the conversation. Decodes protobuf payloads (for `.db` files) or reads JSON lines (for `.jsonl` files) to reconstruct steps, map roles (`USER` vs. `MODEL`), strip internal system flags, and format them into a clean Markdown file in the workspace.

## Common Mistakes

1. **Wrong directory parameters:** By default, it assumes standard paths. Use `--db-dir` and `--brain-dir` to override path pointers.
2. **Database locked/wal state:** Active SQLite databases might be locked if the IDE is performing writes. The script reads through SQLite read-only mode to prevent thread blockings.

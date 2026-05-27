#!/usr/bin/env python3
# /// script
# dependencies = [
#   "rich",
# ]
# ///

import os
import sys
import sqlite3
import re
import json
import argparse
from datetime import datetime
from pathlib import Path

# Try importing rich for enhanced terminal prints, fallback to standard prints if unavailable
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

DEFAULT_DB_DIR = "/Users/arianstoned/.gemini/antigravity-ide/conversations"
DEFAULT_BRAIN_DIR = "/Users/arianstoned/.gemini/antigravity-ide/brain"

# --- PROTOBUF WIRE-FORMAT PARSER (For Active .db Payloads) ---

def parse_varint(data, pos):
    val = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        val |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return val, pos

def parse_proto(data, pos=0, end=None, depth=0):
    if end is None:
        end = len(data)
    results = {}
    if depth > 10:  # Prevent stack overflow
        return results
    while pos < end:
        try:
            key, pos = parse_varint(data, pos)
            if pos > end:
                break
        except Exception:
            break
        wire_type = key & 0x7
        field_num = key >> 3
        
        if wire_type == 0:  # Varint
            try:
                val, pos = parse_varint(data, pos)
            except Exception:
                break
            results[f"field_{field_num}_varint"] = val
        elif wire_type == 1:  # 64-bit
            pos += 8
        elif wire_type == 2:  # Length-delimited
            try:
                length, pos = parse_varint(data, pos)
                if pos + length > end:
                    break
                val_bytes = data[pos:pos+length]
                pos += length
            except Exception:
                break
            try:
                decoded = val_bytes.decode("utf-8")
                printable_ratio = sum(1 for c in decoded if c.isprintable() or c in "\n\r\t") / max(1, len(decoded))
                if len(decoded) > 0 and printable_ratio > 0.9 and any(c.isalpha() for c in decoded):
                    results[f"field_{field_num}_string"] = decoded
                else:
                    try:
                        sub = parse_proto(val_bytes, 0, len(val_bytes), depth + 1)
                        if sub:
                            results[f"field_{field_num}_sub"] = sub
                    except Exception:
                        pass
            except Exception:
                try:
                    sub = parse_proto(val_bytes, 0, len(val_bytes), depth + 1)
                    if sub:
                        results[f"field_{field_num}_sub"] = sub
                except Exception:
                    pass
        elif wire_type == 5:  # 32-bit
            pos += 4
        else:
            pos += 1
    return results

def extract_strings(parsed_dict, out_list):
    for k, v in parsed_dict.items():
        if isinstance(v, str):
            out_list.append(v)
        elif isinstance(v, dict):
            extract_strings(v, out_list)

def get_largest_string(payload):
    if not payload:
        return ""
    parsed = parse_proto(payload)
    strings = []
    extract_strings(parsed, strings)
    longest_string = ""
    for s in strings:
        if len(s) > len(longest_string):
            longest_string = s
    return longest_string

# --- UTILITIES TO CLEAN TEXT ---

def clean_text_markers(text):
    if not text:
        return ""
    text = text.replace("<USER_REQUEST>", "").replace("</USER_REQUEST>", "").strip()
    text = text.split("<ADDITIONAL_METADATA>")[0].strip()
    return text

# --- SEARCH & RECOVERY CORE ---

def get_all_conversations(db_dir, brain_dir):
    """
    Scans the 3-tier architecture of Antigravity IDE:
    1. Conversations directory (SQLite .db files) -> Active (SQLite)
    2. Brain directory (transcript.jsonl files) -> Historical Active (JSONL)
    3. Conversations directory (.pb files) -> Archived (Protobuf)
    """
    db_path = Path(db_dir)
    brain_path = Path(brain_dir)
    
    conversations = {}
    
    # Tier 1: Active Conversations (SQLite .db)
    if db_path.exists() and db_path.is_dir():
        for db in db_path.glob("*.db"):
            conv_id = db.stem
            mtime = datetime.fromtimestamp(db.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            size_kb = db.stat().st_size / 1024
            
            try:
                conn = sqlite3.connect(db)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM steps")
                step_count = cursor.fetchone()[0]
                
                # Fetch first user objective
                cursor.execute("SELECT step_payload FROM steps WHERE step_type=14 ORDER BY idx LIMIT 1")
                row = cursor.fetchone()
                objective = ""
                if row:
                    objective = clean_text_markers(get_largest_string(row[0]))
                    objective = (objective[:90] + "...") if len(objective) > 90 else objective
                
                conversations[conv_id] = {
                    "id": conv_id,
                    "type": "Active (SQLite)",
                    "path": str(db),
                    "mtime": mtime,
                    "size": f"{size_kb:.1f} KB",
                    "steps": step_count,
                    "objective": objective or "[No text objective found]"
                }
                conn.close()
            except sqlite3.Error:
                continue

    # Tier 2: Historical Active Conversations (JSONL Logs in Brain)
    if brain_path.exists() and brain_path.is_dir():
        for log_file in brain_path.glob("**/transcript.jsonl"):
            try:
                conv_id = log_file.parents[2].name
            except IndexError:
                continue
            
            # Skip if already listed as active SQLite DB to avoid duplication
            if conv_id in conversations:
                continue
                
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            size_kb = log_file.stat().st_size / 1024
            
            step_count = 0
            objective = ""
            try:
                with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        step_count += 1
                        try:
                            data = json.loads(line)
                            if not objective and data.get("type") == "USER_INPUT":
                                objective = clean_text_markers(data.get("content", ""))
                                objective = (objective[:90] + "...") if len(objective) > 90 else objective
                        except Exception:
                            pass
                
                conversations[conv_id] = {
                    "id": conv_id,
                    "type": "Historical Active (JSONL)",
                    "path": str(log_file),
                    "mtime": mtime,
                    "size": f"{size_kb:.1f} KB",
                    "steps": step_count,
                    "objective": objective or "[No text objective found]"
                }
            except Exception:
                continue

    # Tier 3: Archived Conversations (.pb Protobuf files)
    if db_path.exists() and db_path.is_dir():
        for pb in db_path.glob("*.pb"):
            conv_id = pb.stem
            
            # Skip if already listed as SQLite DB or JSONL log to avoid duplication
            if conv_id in conversations:
                continue
                
            mtime = datetime.fromtimestamp(pb.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            size_kb = pb.stat().st_size / 1024
            
            conversations[conv_id] = {
                "id": conv_id,
                "type": "Archived (Protobuf)",
                "path": str(pb),
                "mtime": mtime,
                "size": f"{size_kb:.1f} KB",
                "steps": 0,  # Structurally packed
                "objective": "[Index anchor - Rebuild state.vscdb to view content]"
            }
                
    return conversations

def list_conversations(db_dir, brain_dir, filter_tier="all"):
    conversations = get_all_conversations(db_dir, brain_dir)
    if not conversations:
        print("No conversation files (SQLite, JSONL or PB) found.", file=sys.stderr)
        return
        
    # Map tier argument to internal formats
    type_mapping = {
        "active": "Active (SQLite)",
        "historical": "Historical Active (JSONL)",
        "archived": "Archived (Protobuf)"
    }
    
    # Filter list
    if filter_tier != "all":
        target_type = type_mapping.get(filter_tier.lower())
        filtered_convs = [c for c in conversations.values() if c["type"] == target_type]
    else:
        filtered_convs = list(conversations.values())
        
    if not filtered_convs:
        print(f"No conversations found matching tier: '{filter_tier}'", file=sys.stderr)
        return
        
    # Sort: modification time (newest first)
    sorted_convs = sorted(filtered_convs, key=lambda x: x["mtime"], reverse=True)
    
    if HAS_RICH:
        table = Table(title="Antigravity Unified Conversation History", header_style="bold magenta")
        table.add_column("Conversation ID", style="cyan")
        table.add_column("State / Format", style="green")
        table.add_column("Last Modified", style="yellow")
        table.add_column("Steps", justify="right", style="cyan")
        table.add_column("Size", justify="right")
        table.add_column("Objective Summary", style="white")
        
        for c in sorted_convs:
            table.add_row(c["id"], c["type"], c["mtime"], str(c["steps"]), c["size"], c["objective"])
        console.print(table)
    else:
        print(f"{'Conversation ID':<38} | {'State / Format':<25} | {'Last Modified':<19} | {'Steps':<5} | {'Objective Summary'}")
        print("-" * 120)
        for c in sorted_convs:
            print(f"{c['id']:<38} | {c['type']:<25} | {c['mtime']:<19} | {c['steps']:<5} | {c['objective']}")

def search_conversations(db_dir, brain_dir, query, filter_tier="all"):
    conversations = get_all_conversations(db_dir, brain_dir)
    
    # Map tier argument to internal formats
    type_mapping = {
        "active": "Active (SQLite)",
        "historical": "Historical Active (JSONL)",
        "archived": "Archived (Protobuf)"
    }
    
    # Filter list
    if filter_tier != "all":
        target_type = type_mapping.get(filter_tier.lower())
        filtered_convs = {k: v for k, v in conversations.items() if v["type"] == target_type}
    else:
        filtered_convs = conversations
        
    matches = []
    
    for c in filtered_convs.values():
        c_id = c["id"]
        c_path = c["path"]
        c_type = c["type"]
        
        # 1. Search SQLite Active DB
        if c_type == "Active (SQLite)":
            try:
                conn = sqlite3.connect(c_path)
                cursor = conn.cursor()
                cursor.execute("SELECT idx, step_type, step_payload FROM steps")
                rows = cursor.fetchall()
                
                mem_conn = sqlite3.connect(":memory:")
                mem_cursor = mem_conn.cursor()
                mem_cursor.execute("CREATE VIRTUAL TABLE fts_idx USING fts5(idx UNINDEXED, role, content)")
                
                inserted = 0
                for idx, step_type, payload in rows:
                    if not payload:
                        continue
                    content = get_largest_string(payload)
                    if content:
                        role = "USER" if step_type == 14 else "MODEL"
                        mem_cursor.execute("INSERT INTO fts_idx(idx, role, content) VALUES(?, ?, ?)", (idx, role, content))
                        inserted += 1
                
                if inserted > 0:
                    mem_cursor.execute("SELECT idx, role, snippet(fts_idx, 2, '***', '***', '...', 10) FROM fts_idx WHERE content MATCH ?", (query,))
                    search_rows = mem_cursor.fetchall()
                    for idx, role, snippet in search_rows:
                        matches.append({
                            "id": c_id,
                            "type": c_type,
                            "step": idx,
                            "role": role,
                            "snippet": clean_text_markers(snippet).replace("\n", " ")
                        })
                mem_conn.close()
                conn.close()
            except sqlite3.Error:
                continue
                
        # 2. Search JSONL Log File (Historical Active)
        elif c_type == "Historical Active (JSONL)":
            try:
                with open(c_path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            content = data.get("content", "")
                            idx = data.get("step_index", 0)
                            role = "USER" if data.get("type") == "USER_INPUT" else "MODEL"
                            
                            # Case-insensitive substring match
                            if query.lower() in content.lower():
                                start_idx = max(0, content.lower().find(query.lower()) - 40)
                                end_idx = min(len(content), start_idx + len(query) + 80)
                                snippet = content[start_idx:end_idx]
                                if start_idx > 0:
                                    snippet = "..." + snippet
                                if end_idx < len(content):
                                    snippet = snippet + "..."
                                    
                                matches.append({
                                    "id": c_id,
                                    "type": c_type,
                                    "step": idx,
                                    "role": role,
                                    "snippet": clean_text_markers(snippet).replace("\n", " ")
                                })
                        except Exception:
                            pass
            except Exception:
                continue
                
        # 3. Search PB Files (Archived) - Text not indexed locally
        elif c_type == "Archived (Protobuf)":
            # We skip searching the inner contents since PB files are structurally locked,
            # but we report that it is skipped.
            continue
                
    if not matches:
        if HAS_RICH:
            console.print(Panel(f"[bold red]No conversations matched the keyword: '{query}'[/bold red]"))
        else:
            print(f"No conversations matched the keyword: '{query}'")
        return
        
    if HAS_RICH:
        table = Table(title=f"Unified search matches for query: '{query}'", header_style="bold magenta")
        table.add_column("Conversation ID", style="cyan")
        table.add_column("State / Format", style="green")
        table.add_column("Step", justify="right", style="yellow")
        table.add_column("Role", style="green")
        table.add_column("Snippet Match", style="white")
        
        for m in matches:
            table.add_row(m["id"], m["type"], str(m["step"]), m["role"], m["snippet"])
        console.print(table)
    else:
        print(f"{'Conversation ID':<38} | {'State':<20} | {'Step':<4} | {'Role':<5} | {'Snippet'}")
        print("-" * 120)
        for m in matches:
            print(f"{m['id']:<38} | {m['type']:<20} | {m['step']:<4} | {m['role']:<5} | {m['snippet']}")

def recover_conversation(db_dir, brain_dir, conv_id, output_file):
    conversations = get_all_conversations(db_dir, brain_dir)
    
    if conv_id not in conversations:
        print(f"Error: Conversation ID '{conv_id}' not found in active databases or brain logs.", file=sys.stderr)
        sys.exit(1)
        
    c = conversations[conv_id]
    c_path = c["path"]
    c_type = c["type"]
    
    transcript = []
    
    # 1. Recover from SQLite active DB
    if c_type == "Active (SQLite)":
        try:
            conn = sqlite3.connect(c_path)
            cursor = conn.cursor()
            cursor.execute("SELECT idx, step_type, step_payload FROM steps ORDER BY idx")
            rows = cursor.fetchall()
            for idx, step_type, payload in rows:
                if not payload:
                    continue
                content = get_largest_string(payload)
                if content:
                    transcript.append({
                        "idx": idx,
                        "step_type": step_type,
                        "content": content
                    })
            conn.close()
        except sqlite3.Error as e:
            print(f"Error reading SQLite database: {e}", file=sys.stderr)
            sys.exit(1)
            
    # 2. Recover from JSONL logs (Historical Active)
    elif c_type == "Historical Active (JSONL)":
        try:
            with open(c_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        idx = data.get("step_index", 0)
                        role = data.get("type", "")
                        step_type = 14 if role == "USER_INPUT" else 15
                        content = data.get("content", "")
                        if content:
                            transcript.append({
                                "idx": idx,
                                "step_type": step_type,
                                "content": content
                            })
                    except Exception:
                        pass
        except Exception as e:
            print(f"Error reading JSONL transcript: {e}", file=sys.stderr)
            sys.exit(1)
            
    # 3. Recover Archived (Protobuf) - Instruct to rebuild
    elif c_type == "Archived (Protobuf)":
        print("Error: Conversation is Archived (Protobuf) and its raw text logs have been cleaned up.", file=sys.stderr)
        print("Please run 'rebuild_conversations.py' to restore this conversation into your active IDE index first.", file=sys.stderr)
        sys.exit(1)
            
    # Format and save as Markdown
    md_lines = []
    md_lines.append(f"# Unified Recovered Conversation: {conv_id}\n")
    md_lines.append(f"*Recovered on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Format: {c_type}*\n")
    md_lines.append("--- \n")
    
    for entry in transcript:
        idx = entry["idx"]
        step_type = entry["step_type"]
        content = entry["content"]
        
        if step_type == 14:  # USER
            role = "👤 USER (Arian)"
            content = clean_text_markers(content)
            md_lines.append(f"\n### {role} (Step {idx})")
            md_lines.append("```markdown")
            md_lines.append(content)
            md_lines.append("```")
            md_lines.append("\n---")
        elif step_type == 15:  # MODEL
            role = "🤖 MODEL (J.A.R.V.I.S.)"
            md_lines.append(f"\n### {role} (Step {idx})\n")
            md_lines.append(content)
            md_lines.append("\n---")
            
    output_path = Path(output_file)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write("\n".join(md_lines))
        
        if HAS_RICH:
            console.print(Panel(f"[bold green]Success![/bold green] Recovered conversation written to:\n[cyan]{output_path.resolve()}[/cyan]"))
        else:
            print(f"Success! Recovered conversation written to: {output_path.resolve()}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

# --- CLI INITIALIZATION ---

def main():
    parser = argparse.ArgumentParser(
        description="conversation-skill-recuperation CLI: Reconstruct lost and archived trajectories."
    )
    parser.add_argument(
        "--db-dir", 
        default=DEFAULT_DB_DIR, 
        help=f"Path to the conversations SQLite directory (default: {DEFAULT_DB_DIR})"
    )
    parser.add_argument(
        "--brain-dir", 
        default=DEFAULT_BRAIN_DIR, 
        help=f"Path to the brain logs directory (default: {DEFAULT_BRAIN_DIR})"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all conversations in specified tiers")
    list_parser.add_argument(
        "--tier", 
        choices=["active", "historical", "archived", "all"], 
        default="all",
        help="Filter conversations by storage tier (default: all)"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search query inside active and historical text logs")
    search_parser.add_argument("query", help="Keyword or phrase to search")
    search_parser.add_argument(
        "--tier", 
        choices=["active", "historical", "all"], 
        default="all",
        help="Filter search scope by storage tier (default: all)"
    )
    
    # Recover command
    recover_parser = subparsers.add_parser("recover", help="Extract and compile the unified trajectory to Markdown")
    recover_parser.add_argument("id", help="Conversation ID (uuid stem)")
    recover_parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Target absolute path to write the formatted markdown file"
    )
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_conversations(args.db_dir, args.brain_dir, args.tier)
    elif args.command == "search":
        search_conversations(args.db_dir, args.brain_dir, args.query, args.tier)
    elif args.command == "recover":
        recover_conversation(args.db_dir, args.brain_dir, args.id, args.output)

if __name__ == "__main__":
    main()

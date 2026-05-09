#!/usr/bin/env python3
"""
Export the current Claude Code session transcript as a numbered session file.

Reads from: ~/.claude/projects/<cwd-hash>/<latest-session>.jsonl
Writes to:  <cwd>/sessions/session-NNN.txt
Prints the output path on success; writes error to stderr and exits 1 on failure.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def _project_dir(cwd: str) -> Path:
    name = cwd.replace("/", "-")
    return Path.home() / ".claude" / "projects" / name


def _latest_jsonl(project_dir: Path) -> Path | None:
    files = list(project_dir.glob("*.jsonl"))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def _extract(jsonl_path: Path) -> list[tuple[str, str]]:
    """Return ordered (role, text) pairs for human/assistant turns only.

    Skips tool calls, tool results, thinking blocks, and hook messages.
    Deduplicates assistant messages by message id (streaming sends multiple
    entries with the same id, each carrying different content block types).
    """
    order: list[tuple[str, str]] = []
    seen_asst_ids: set[str] = set()
    asst_texts: dict[str, list[str]] = defaultdict(list)

    with open(jsonl_path, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError:
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content", "")
            msg_id = msg.get("id", "")

            if role == "user" and isinstance(content, str):
                text = content.strip()
                if text:
                    order.append(("human", text))

            elif role == "assistant" and isinstance(content, list):
                texts = [
                    b["text"].strip()
                    for b in content
                    if isinstance(b, dict)
                    and b.get("type") == "text"
                    and b.get("text", "").strip()
                ]
                if texts:
                    asst_texts[msg_id].extend(texts)
                    if msg_id not in seen_asst_ids:
                        seen_asst_ids.add(msg_id)
                        order.append(("asst", msg_id))

    return [
        (role, text if role == "human" else "\n\n".join(asst_texts[text]))
        for role, text in order
        if role == "human" or asst_texts.get(text)
    ]


def _next_number(sessions_dir: Path) -> int:
    return len(list(sessions_dir.glob("session-*.txt"))) + 1


def main() -> None:
    cwd = os.getcwd()
    proj_dir = _project_dir(cwd)

    if not proj_dir.is_dir():
        print(f"error: project dir not found: {proj_dir}", file=sys.stderr)
        sys.exit(1)

    jsonl = _latest_jsonl(proj_dir)
    if not jsonl:
        print("error: no session file found", file=sys.stderr)
        sys.exit(1)

    turns = _extract(jsonl)
    if not turns:
        print("error: no conversation turns extracted", file=sys.stderr)
        sys.exit(1)

    sessions_dir = Path(cwd) / "sessions"
    sessions_dir.mkdir(exist_ok=True)

    num = _next_number(sessions_dir)
    out = sessions_dir / f"session-{num:03d}.txt"
    date = datetime.now().strftime("%Y-%m-%d")

    blocks = [f"Session {num:03d} — {date}\n{'=' * 40}"]
    for role, text in turns:
        label = "You" if role == "human" else "Tutor"
        blocks.append(f"[{label}]\n{text}")

    out.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

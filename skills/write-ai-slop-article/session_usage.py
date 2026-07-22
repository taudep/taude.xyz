#!/usr/bin/env python3
"""Sum token usage from a Claude Code session transcript.

Reads ~/.claude/projects/<slug-of-cwd>/<session>.jsonl, where each line
is a JSON event and assistant-message events carry a message.usage
object shaped like the Claude API's usage field. This is Claude Code's
internal transcript format, not a stable public API - if this breaks
after a Claude Code update, that's why.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def project_dir(cwd: Path) -> Path:
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
    return Path.home() / ".claude" / "projects" / slug


def find_transcript(cwd: Path, session_id: str) -> Path:
    path = project_dir(cwd) / f"{session_id}.jsonl"
    if not path.exists():
        raise SystemExit(f"no transcript at {path}")
    return path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: session_usage.py <session-id>\n"
            "Multiple transcripts in the same project directory can share "
            "an mtime (e.g. a bridged companion session), so this requires "
            "an explicit session id rather than guessing the newest file. "
            "Get it from the current session's own scratchpad path, not by "
            "picking whichever .jsonl looks newest."
        )
    transcript = find_transcript(Path.cwd(), sys.argv[1])

    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    messages = 0
    first_ts = last_ts = None

    with transcript.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = event.get("timestamp")
            if ts:
                first_ts = first_ts or ts
                last_ts = ts
            msg = event.get("message")
            if isinstance(msg, dict) and isinstance(msg.get("usage"), dict):
                messages += 1
                for k in totals:
                    v = msg["usage"].get(k)
                    if isinstance(v, (int, float)):
                        totals[k] += v

    print(f"transcript: {transcript}")
    print(f"assistant messages with usage: {messages}")
    for k, v in totals.items():
        print(f"{k}: {v:,}")
    print(f"total tokens (all categories): {sum(totals.values()):,}")
    if first_ts and last_ts:
        print(f"session span: {first_ts} .. {last_ts}")


if __name__ == "__main__":
    main()

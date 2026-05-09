"""Tests for export_session.py — session transcript exporter."""
import importlib.util
import json
from pathlib import Path

import pytest

# Load the script as a module (hyphen-free name but import by path for safety)
_SCRIPT = Path(__file__).parent.parent / "export_session.py"
_spec = importlib.util.spec_from_file_location("export_session", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_project_dir = _mod._project_dir
_latest_jsonl = _mod._latest_jsonl
_extract = _mod._extract
_next_number = _mod._next_number


# ── helpers ──────────────────────────────────────────────────────────────────

def _user(text: str) -> dict:
    return {"message": {"role": "user", "content": text}}


def _tool_result(tool_id: str = "t1") -> dict:
    return {"message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tool_id, "content": "ok"}
    ]}}


def _assistant(text: str, msg_id: str = "msg-1") -> dict:
    return {"message": {"role": "assistant", "id": msg_id,
                        "content": [{"type": "text", "text": text}]}}


def _tool_use(msg_id: str = "msg-1") -> dict:
    return {"message": {"role": "assistant", "id": msg_id,
                        "content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": {}}]}}


def _thinking(msg_id: str = "msg-1") -> dict:
    return {"message": {"role": "assistant", "id": msg_id,
                        "content": [{"type": "thinking", "thinking": "hmm..."}]}}


def _write_jsonl(path: Path, entries: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


# ── _project_dir ─────────────────────────────────────────────────────────────

class TestProjectDir:
    def test_replaces_slashes_with_dashes(self):
        result = _project_dir("/Users/alice/my-project")
        assert result == Path.home() / ".claude" / "projects" / "-Users-alice-my-project"

    def test_leading_slash_becomes_leading_dash(self):
        result = _project_dir("/a/b")
        assert str(result).endswith("-a-b")


# ── _latest_jsonl ─────────────────────────────────────────────────────────────

class TestLatestJsonl:
    def test_returns_none_when_no_files(self, tmp_path):
        assert _latest_jsonl(tmp_path) is None

    def test_returns_most_recently_modified(self, tmp_path):
        old = tmp_path / "old.jsonl"
        new = tmp_path / "new.jsonl"
        old.write_text("{}")
        new.write_text("{}")
        new.touch()  # ensure newer mtime
        assert _latest_jsonl(tmp_path) == new


# ── _extract ──────────────────────────────────────────────────────────────────

class TestExtract:
    def test_extracts_plain_user_message(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_user("Hello")])
        assert _extract(f) == [("human", "Hello")]

    def test_skips_user_tool_results(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_tool_result()])
        assert _extract(f) == []

    def test_extracts_assistant_text(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_assistant("Hello student")])
        assert _extract(f) == [("assistant", "Hello student")]

    def test_skips_assistant_tool_use(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_tool_use()])
        assert _extract(f) == []

    def test_skips_thinking_blocks(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_thinking()])
        assert _extract(f) == []

    def test_deduplicates_streaming_chunks_by_message_id(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [
            _thinking(msg_id="m1"),
            _assistant("Part one", msg_id="m1"),
            _assistant("Part two", msg_id="m1"),
        ])
        turns = _extract(f)
        assert len(turns) == 1
        assert "Part one" in turns[0][1]
        assert "Part two" in turns[0][1]

    def test_preserves_conversation_order(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [
            _user("Q1"),
            _assistant("A1", msg_id="m1"),
            _user("Q2"),
            _assistant("A2", msg_id="m2"),
        ])
        roles = [r for r, _ in _extract(f)]
        assert roles == ["human", "assistant", "human", "assistant"]

    def test_skips_blank_lines(self, tmp_path):
        f = tmp_path / "s.jsonl"
        f.write_text(
            json.dumps(_user("hi")) + "\n\n" + json.dumps(_user("bye")) + "\n",
            encoding="utf-8",
        )
        assert len(_extract(f)) == 2

    def test_skips_malformed_json(self, tmp_path):
        f = tmp_path / "s.jsonl"
        f.write_text("not-json\n" + json.dumps(_user("valid")) + "\n", encoding="utf-8")
        assert _extract(f) == [("human", "valid")]

    def test_strips_whitespace_from_messages(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [_user("  hello  ")])
        assert _extract(f) == [("human", "hello")]

    def test_ignores_entries_without_message_key(self, tmp_path):
        f = tmp_path / "s.jsonl"
        _write_jsonl(f, [
            {"type": "last-prompt", "leafUuid": "abc"},
            _user("real message"),
        ])
        assert _extract(f) == [("human", "real message")]


# ── _next_number ──────────────────────────────────────────────────────────────

class TestNextNumber:
    def test_returns_1_when_empty(self, tmp_path):
        assert _next_number(tmp_path) == 1

    def test_increments_past_existing(self, tmp_path):
        (tmp_path / "session-001.txt").touch()
        (tmp_path / "session-002.txt").touch()
        assert _next_number(tmp_path) == 3

    def test_ignores_non_session_files(self, tmp_path):
        (tmp_path / "notes.txt").touch()
        (tmp_path / "README.md").touch()
        assert _next_number(tmp_path) == 1

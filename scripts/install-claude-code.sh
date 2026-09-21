#!/usr/bin/env bash
set -euo pipefail

PROJECT_PATH="${1:-}"
if [[ -z "$PROJECT_PATH" ]]; then
  echo "Usage: $0 /path/to/project" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$PROJECT_PATH/.claude/skills/chomview"
AGENT_DIR="$PROJECT_PATH/.claude/agents"
RUNTIME_DIR="$PROJECT_PATH/.claude/chomview"

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/schemas" "$AGENT_DIR" "$RUNTIME_DIR"
cp "$ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$ROOT/references/"*.md "$SKILL_DIR/references/"
cp "$ROOT/schemas/"*.json "$SKILL_DIR/schemas/"
cp "$ROOT/agents/chomview-second-thought.md" "$AGENT_DIR/chomview-second-thought.md"
cp "$ROOT/runtime/chomview_guard.py" "$RUNTIME_DIR/chomview_guard.py"
if [[ ! -f "$RUNTIME_DIR/behavioral-contract.json" ]]; then
  cp "$ROOT/config/behavioral-contract.default.json" "$RUNTIME_DIR/behavioral-contract.json"
fi
chmod +x "$RUNTIME_DIR/chomview_guard.py"

python3 "$ROOT/scripts/configure_claude_hooks.py" "$PROJECT_PATH" --python python3

# Materialize core correction state without inventing project-specific rules.
CLAUDE_PROJECT_DIR="$PROJECT_PATH" python3 "$RUNTIME_DIR/chomview_guard.py" status >/dev/null

echo "Installed ChomView v0.4.0 into $PROJECT_PATH"
echo "Behavioral Continuity + Compatibility Guard enabled via SessionStart, UserPromptSubmit, and PreToolUse hooks."

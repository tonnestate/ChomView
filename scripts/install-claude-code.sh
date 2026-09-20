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

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/schemas" "$AGENT_DIR"
cp "$ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$ROOT/references/"*.md "$SKILL_DIR/references/"
cp "$ROOT/schemas/"*.json "$SKILL_DIR/schemas/"
cp "$ROOT/agents/chomview-second-thought.md" "$AGENT_DIR/chomview-second-thought.md"

echo "Installed ChomView into $PROJECT_PATH"

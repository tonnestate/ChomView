#!/usr/bin/env bash
set -euo pipefail

PROJECT_PATH="${1:-}"
if [[ -z "$PROJECT_PATH" ]]; then
  echo "Usage: $0 /path/to/project" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SKILL="$ROOT/.claude/skills/chomview"
SRC_AGENT="$ROOT/.claude/agents/chomview-second-thought.md"
DST_SKILL="$PROJECT_PATH/.claude/skills/chomview"
DST_AGENT_DIR="$PROJECT_PATH/.claude/agents"

if [[ ! -f "$SRC_SKILL/SKILL.md" ]]; then
  echo "Missing source skill: $SRC_SKILL/SKILL.md" >&2
  exit 1
fi
if [[ ! -f "$SRC_AGENT" ]]; then
  echo "Missing source agent: $SRC_AGENT" >&2
  exit 1
fi

mkdir -p "$PROJECT_PATH/.claude/skills" "$DST_AGENT_DIR"
rm -rf "$DST_SKILL"
cp -a "$SRC_SKILL" "$DST_SKILL"
cp "$SRC_AGENT" "$DST_AGENT_DIR/chomview-second-thought.md"

echo "Installed ChomView into $PROJECT_PATH"

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$SkillDir = Join-Path $ProjectPath ".claude\skills\chomview"
$AgentDir = Join-Path $ProjectPath ".claude\agents"
$RuntimeDir = Join-Path $ProjectPath ".claude\chomview"

New-Item -ItemType Directory -Force -Path (Join-Path $SkillDir "references") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $SkillDir "schemas") | Out-Null
New-Item -ItemType Directory -Force -Path $AgentDir | Out-Null
New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null

Copy-Item (Join-Path $Root "SKILL.md") (Join-Path $SkillDir "SKILL.md") -Force
Copy-Item (Join-Path $Root "references\*.md") (Join-Path $SkillDir "references") -Force
Copy-Item (Join-Path $Root "schemas\*.json") (Join-Path $SkillDir "schemas") -Force
Copy-Item (Join-Path $Root "agents\chomview-second-thought.md") (Join-Path $AgentDir "chomview-second-thought.md") -Force
Copy-Item (Join-Path $Root "runtime\chomview_guard.py") (Join-Path $RuntimeDir "chomview_guard.py") -Force
$ContractPath = Join-Path $RuntimeDir "behavioral-contract.json"
if (-not (Test-Path $ContractPath)) {
    Copy-Item (Join-Path $Root "config\behavioral-contract.default.json") $ContractPath
}

$PythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
    & py -3 (Join-Path $Root "scripts\configure_claude_hooks.py") $ProjectPath --python py
    $env:CLAUDE_PROJECT_DIR = $ProjectPath
    & py -3 (Join-Path $RuntimeDir "chomview_guard.py") status | Out-Null
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
    & python (Join-Path $Root "scripts\configure_claude_hooks.py") $ProjectPath --python python
    $env:CLAUDE_PROJECT_DIR = $ProjectPath
    & python (Join-Path $RuntimeDir "chomview_guard.py") status | Out-Null
} else {
    throw "Python 3 is required to install the ChomView v0.4 Behavioral Continuity + Compatibility Guard."
}

Write-Host "Installed ChomView v0.4.0 into $ProjectPath"
Write-Host "Behavioral Continuity + Compatibility Guard enabled via SessionStart, UserPromptSubmit, and PreToolUse hooks."

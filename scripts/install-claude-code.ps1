param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$SkillDir = Join-Path $ProjectPath ".claude\skills\chomview"
$AgentDir = Join-Path $ProjectPath ".claude\agents"

New-Item -ItemType Directory -Force -Path (Join-Path $SkillDir "references") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $SkillDir "schemas") | Out-Null
New-Item -ItemType Directory -Force -Path $AgentDir | Out-Null

Copy-Item (Join-Path $Root "SKILL.md") (Join-Path $SkillDir "SKILL.md") -Force
Copy-Item (Join-Path $Root "references\*.md") (Join-Path $SkillDir "references") -Force
Copy-Item (Join-Path $Root "schemas\*.json") (Join-Path $SkillDir "schemas") -Force
Copy-Item (Join-Path $Root ".claude\agents\chomview-second-thought.md") (Join-Path $AgentDir "chomview-second-thought.md") -Force

Write-Host "Installed ChomView into $ProjectPath"

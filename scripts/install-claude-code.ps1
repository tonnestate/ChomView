param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$SourceSkill = Join-Path $Root ".claude\skills\chomview"
$SourceAgent = Join-Path $Root ".claude\agents\chomview-second-thought.md"
$DestinationSkillsRoot = Join-Path $ProjectPath ".claude\skills"
$DestinationSkill = Join-Path $DestinationSkillsRoot "chomview"
$DestinationAgentDir = Join-Path $ProjectPath ".claude\agents"

if (-not (Test-Path (Join-Path $SourceSkill "SKILL.md"))) {
    throw "Missing source skill: $SourceSkill\SKILL.md"
}
if (-not (Test-Path $SourceAgent)) {
    throw "Missing source agent: $SourceAgent"
}

New-Item -ItemType Directory -Force -Path $DestinationSkillsRoot | Out-Null
New-Item -ItemType Directory -Force -Path $DestinationAgentDir | Out-Null

if (Test-Path $DestinationSkill) {
    Remove-Item -Recurse -Force $DestinationSkill
}
Copy-Item -Recurse -Force $SourceSkill $DestinationSkill
Copy-Item -Force $SourceAgent (Join-Path $DestinationAgentDir "chomview-second-thought.md")

Write-Host "Installed ChomView into $ProjectPath"

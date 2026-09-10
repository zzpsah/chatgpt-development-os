param([Parameter(Mandatory=$true,Position=0)][string]$Path,[string]$Name,[string]$ProjectId)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
if(-not $Name){$Name=Split-Path $root -Leaf}
if(-not $ProjectId){$ProjectId=($Name.ToLower() -replace '[^a-z0-9]+','-' -replace '(^-|-$)','')}
$ai=Join-Path $root '.ai'
New-Item -ItemType Directory -Force -Path $ai,(Join-Path $ai 'SESSIONS') | Out-Null
function Write-IfMissing($file,$content){if(-not(Test-Path -LiteralPath $file)){Set-Content -LiteralPath $file -Value $content -Encoding UTF8}}
Write-IfMissing (Join-Path $root 'AGENTS.md') @"
# Project AI Entry Point

This project uses the Portable Project Context Specification from ChatGPT Development OS.

Before substantial work, read `.ai/manifest.yaml`, `.ai/PROJECT.md`, `.ai/CURRENT-STATE.md`, and relevant decisions/tasks/architecture. Inspect actual source code before changing it.

After meaningful work, update verified state, tasks, and important decisions. Never store secrets or credentials in project context.

The project-local `.ai/` context, source code, and version-control history are the durable project record; do not depend on AI account chat memory.
"@
Write-IfMissing (Join-Path $ai 'manifest.yaml') @"
context_version: 1
specification: portable-project-context
project_id: $ProjectId
name: "$Name"
managed_by: development-os
context_directory: .ai
read_first:
  - PROJECT.md
  - CURRENT-STATE.md
recommended:
  - ARCHITECTURE.md
  - DECISIONS.md
  - TASKS.md
secrets_policy: never-store-secrets
"@
$today=Get-Date -Format 'yyyy-MM-dd'
Write-IfMissing (Join-Path $ai 'PROJECT.md') @"
# Project

## Identity
- Project ID: $ProjectId
- Name: $Name
- Created: $today

## Purpose
Describe what this project does and why it exists.

## Scope
Describe the main capabilities and boundaries.

## Technology
- Runtime:
- Framework:
- Database:
- Hosting:

## Important constraints
- 

## Authoritative sources
- Source code
- Version-control history
- This `.ai/` directory
"@
Write-IfMissing (Join-Path $ai 'CURRENT-STATE.md') @"
# Current State

Last verified: never

## Working
- 

## In progress
- 

## Known issues
- 

## Next actions
- 

## Verification
- No verification has been recorded yet.
"@
Write-IfMissing (Join-Path $ai 'ARCHITECTURE.md') "# Architecture`n`nDescribe components, data flows, integrations, and boundaries.`n"
Write-IfMissing (Join-Path $ai 'DECISIONS.md') "# Decisions`n`nRecord material architecture, security, data, UX, deployment, and maintenance decisions.`n"
Write-IfMissing (Join-Path $ai 'TASKS.md') "# Tasks`n`n## Active`n- `n`n## Planned`n- `n`n## Blocked`n- `n"
Write-Host "Initialized portable AI context: $root" -ForegroundColor Green

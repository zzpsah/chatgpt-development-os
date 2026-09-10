param(
  [Parameter(Mandatory=$true,Position=0)][string]$Path,
  [string]$Name,
  [string]$ProjectId,
  [switch]$DryRun
)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
if(-not(Test-Path (Join-Path $root '.git') -PathType Container)){ throw "Not a Git repository: $root" }
if(-not $Name){$Name=Split-Path $root -Leaf}
if(-not $ProjectId){$ProjectId=($Name.ToLower() -replace '[^a-z0-9]+','-' -replace '(^-|-$)','')}
$init=Join-Path $PSScriptRoot 'init-project.ps1'
$caller=Join-Path $root '.github\workflows\context-sync.yml'

Write-Host "Development OS onboarding: $root"
Write-Host "Project: $Name ($ProjectId)"
if($DryRun){ Write-Host 'DRY RUN: no files will be changed.' -ForegroundColor Yellow }

function Invoke-Step($description,[scriptblock]$action){
  Write-Host "- $description"
  if(-not $DryRun){ & $action }
}

Invoke-Step 'Initialize missing portable .ai context' { & $init -Path $root -Name $Name -ProjectId $ProjectId }
Invoke-Step 'Add GitHub context-sync caller when missing' {
  $dir=Split-Path $caller -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  if(-not(Test-Path -LiteralPath $caller)){
    @'
# Project-side caller for the reusable Development OS context synchronizer.
name: Development OS Context Sync

on:
  push:
    branches:
      - main
      - master

permissions:
  contents: write

jobs:
  sync:
    uses: zzpsah/chatgpt-development-os/.github/workflows/context-sync.yml@main
    permissions:
      contents: write
'@ | Set-Content -LiteralPath $caller -Encoding UTF8
  } else { Write-Host '  Existing caller preserved.' }
}

if($DryRun){
  Write-Host 'Dry run complete.' -ForegroundColor Yellow
} else {
  Write-Host 'Onboarding complete. Existing .ai files were preserved.' -ForegroundColor Green
  Write-Host 'Next: commit/push the onboarding changes so GitHub Actions can synchronize STATE-INDEX and CHANGELOG.'
}

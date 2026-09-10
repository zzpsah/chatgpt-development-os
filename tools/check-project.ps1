param([Parameter(Mandatory=$true,Position=0)][string]$Path)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
$required=@(
  'AGENTS.md',
  '.ai\manifest.yaml',
  '.ai\STATE-INDEX.md',
  '.ai\PROJECT.md',
  '.ai\CURRENT-STATE.md',
  '.ai\ARCHITECTURE.md',
  '.ai\DECISIONS.md',
  '.ai\TASKS.md',
  '.ai\CHANGELOG.md',
  '.ai\SESSIONS\session-template.md',
  '.github\workflows\context-sync.yml'
)
$missing=@(); foreach($item in $required){if(-not(Test-Path (Join-Path $root $item))){$missing+=$item}}
$secrets=@('.env','*.pem','*.key','*secret*','*password*','*token*')
$secretHits=@(); foreach($pattern in $secrets){$secretHits += Get-ChildItem -Path $root -Recurse -Force -File -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {$_.FullName.Substring($root.Length+1)}}
Write-Host "Development OS health check: $root"
if($missing.Count -eq 0){Write-Host 'Context files: OK' -ForegroundColor Green}else{Write-Host ('Missing: '+($missing -join ', ')) -ForegroundColor Red}
if($secretHits.Count -eq 0){Write-Host 'Obvious secret-named files: none detected' -ForegroundColor Green}else{Write-Host ('Review secret-named files: '+($secretHits -join ', ')) -ForegroundColor Yellow}
if($missing.Count -gt 0){exit 1}

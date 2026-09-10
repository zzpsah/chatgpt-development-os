param([Parameter(Mandatory=$true)][string]$Root)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $Root -ErrorAction Stop).Path
$script=Join-Path $PSScriptRoot 'init-project.ps1'
$watcher=New-Object System.IO.FileSystemWatcher
$watcher.Path=$root
$watcher.IncludeSubdirectories=$true
$watcher.EnableRaisingEvents=$true
$watcher.NotifyFilter=[IO.NotifyFilters]'DirectoryName,FileName'
$action={
  $path=$Event.SourceEventArgs.FullPath
  if($path -match '\\.ai(\\|$)' -or $path -match '\\node_modules(\\|$)' -or $path -match '\\.git(\\|$)'){return}
  $dir=if(Test-Path -LiteralPath $path -PathType Container){$path}else{Split-Path $path -Parent}
  while($dir -and $dir.StartsWith($using:root,[StringComparison]::OrdinalIgnoreCase)){
    if(Test-Path (Join-Path $dir '.git') -PathType Container -or Test-Path (Join-Path $dir 'package.json') -PathType Leaf -or Test-Path (Join-Path $dir 'pyproject.toml') -PathType Leaf -or Test-Path (Join-Path $dir 'requirements.txt') -PathType Leaf){
      & $using:script -Path $dir | Out-Null; break
    }
    $parent=Split-Path $dir -Parent; if($parent -eq $dir){break}; $dir=$parent
  }
}
Register-ObjectEvent $watcher Created -Action $action | Out-Null
Write-Host "Development OS watcher active: $root" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop."
try { while($true){Start-Sleep -Seconds 2} } finally { Get-EventSubscriber | Unregister-Event; $watcher.Dispose() }

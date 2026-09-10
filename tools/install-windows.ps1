param([string[]]$Roots=@())
$ErrorActionPreference='Stop'
$devos=Join-Path $env:USERPROFILE '.devos'
New-Item -ItemType Directory -Force $devos | Out-Null
$rootsFile=Join-Path $devos 'roots.txt'
if($Roots.Count -gt 0){$Roots | ForEach-Object { (Resolve-Path -LiteralPath $_ -ErrorAction Stop).Path } | Set-Content $rootsFile -Encoding UTF8}
if(-not(Test-Path $rootsFile)){throw "No roots configured. Example: .\install-windows.ps1 -Roots 'D:\Projects','C:\Users\You\Documents\Projects'"}
$watch=(Join-Path (Split-Path $PSScriptRoot -Parent) 'tools\watch-projects.ps1')
$launcher=Join-Path $devos 'watch.ps1'
$code=@'
$roots=Get-Content "$env:USERPROFILE\.devos\roots.txt" | Where-Object {$_ -and (Test-Path $_)}
foreach($r in $roots){ Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"__WATCH__`" -Root `"$r`"" -WindowStyle Hidden }
'@.Replace('__WATCH__',$watch)
Set-Content $launcher $code -Encoding UTF8
$task='DevelopmentOS-ProjectWatcher'
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$launcher`""
$trigger=New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName $task -Action $action -Trigger $trigger -Description 'Creates portable .ai project context for projects detected under configured Development OS roots.' -Force | Out-Null
Write-Host "Installed Development OS project watcher." -ForegroundColor Green
Write-Host "Configured roots:"; Get-Content $rootsFile

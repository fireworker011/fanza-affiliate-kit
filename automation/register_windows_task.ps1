# Register a daily Windows task (edit time as needed)
# Run in PowerShell (may need admin depending on policy):
#   powershell -ExecutionPolicy Bypass -File automation\register_windows_task.ps1

$python = (Get-Command python).Source
$kit = "C:\Users\ys734\fanza_affiliate_kit"
$action = New-ScheduledTaskAction -Execute $python -Argument "automation\run_daily.py" -WorkingDirectory $kit
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "FanzaNoteDailyPackage" -Action $action -Trigger $trigger -Settings $settings -Force
Write-Output "Registered FanzaNoteDailyPackage at 9:00 daily"
Write-Output "Output goes to automation\out\ — still paste/publish to note (or use note_publish.py semi-auto)"

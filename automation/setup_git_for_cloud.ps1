# Initialize git repo for GitHub Actions cloud daily runs.
# Does NOT create the remote for you (needs your GitHub account).

$ErrorActionPreference = "Stop"
# script is automation\setup_git_for_cloud.ps1 -> kit root is parent of automation
$kit = Split-Path $PSScriptRoot -Parent
Set-Location $kit

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error "git is not installed. Install from https://git-scm.com/"
}

if (-not (Test-Path .git)) {
  git init
  Write-Output "git init OK"
} else {
  Write-Output "git already initialized"
}

git add -A
git status

$hasHead = $true
git rev-parse HEAD 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { $hasHead = $false }

if (-not $hasHead) {
  git commit -m "feat: FANZA kit with cloud daily note package automation"
  Write-Output "initial commit created"
} else {
  $pending = git status --porcelain
  if ($pending) {
    git commit -m "chore: update automation for cloud daily runs"
    Write-Output "commit created"
  } else {
    Write-Output "nothing to commit"
  }
}

Write-Output ""
Write-Output "Next steps:"
Write-Output "  1. Create empty private repo on GitHub"
Write-Output "  2. git remote add origin https://github.com/USER/REPO.git"
Write-Output "  3. git branch -M main"
Write-Output "  4. git push -u origin main"
Write-Output "  5. Actions tab, Daily note package, Run workflow"
Write-Output "See automation/CLOUD_DAILY.md"

# Initialize git repo for GitHub Actions cloud daily runs.
# Does NOT create the remote for you (needs your GitHub account).

$ErrorActionPreference = "Continue"
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

git rev-parse --verify HEAD 1>$null 2>$null
$hasHead = ($LASTEXITCODE -eq 0)

if (-not $hasHead) {
  git -c user.email=kit@local -c user.name=fanza-kit commit -m "feat: FANZA kit with cloud daily note package automation"
  Write-Output "initial commit created"
} else {
  $pending = git status --porcelain
  if ($pending) {
    git -c user.email=kit@local -c user.name=fanza-kit commit -m "chore: update automation for cloud daily runs"
    Write-Output "commit created"
  } else {
    Write-Output "nothing to commit"
  }
}
git branch -M main 2>$null

Write-Output ""
Write-Output "Next steps:"
Write-Output "  1. Create empty private repo on GitHub"
Write-Output "  2. git remote add origin https://github.com/USER/REPO.git"
Write-Output "  3. git branch -M main"
Write-Output "  4. git push -u origin main"
Write-Output "  5. Actions tab, Daily note package, Run workflow"
Write-Output "See automation/CLOUD_DAILY.md"

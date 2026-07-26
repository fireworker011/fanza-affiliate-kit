# Push kit to GitHub private/public repo named fanza-affiliate-kit
# Usage:
#   powershell -ExecutionPolicy Bypass -File automation\push_github.ps1 -GitHubUser YOUR_USERNAME
# Optional:
#   -Private:$false  for public repo (default private note only - create empty repo first on web)

param(
  [Parameter(Mandatory = $true)]
  [string]$GitHubUser,
  [string]$RepoName = "fanza-affiliate-kit"
)

$ErrorActionPreference = "Stop"
$kit = Split-Path $PSScriptRoot -Parent
Set-Location $kit

if (-not (Test-Path .git)) {
  Write-Error "No .git — run automation\setup_git_for_cloud.ps1 first"
}

$url = "https://github.com/$GitHubUser/$RepoName.git"
Write-Output "Remote: $url"

$existing = git remote 2>$null
if ($existing -match "origin") {
  git remote set-url origin $url
  Write-Output "Updated origin URL"
} else {
  git remote add origin $url
  Write-Output "Added origin"
}

git branch -M main
Write-Output "Pushing main (login / token may be required)..."
git push -u origin main
Write-Output "Done. Open: https://github.com/$GitHubUser/$RepoName/actions"
Write-Output "Then: Actions -> Daily note package -> Run workflow"

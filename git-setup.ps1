# Resume Chatbot - Git Setup Script for PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Resume Chatbot - Git Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize git repository
Write-Host "[1/6] Initializing Git repository..." -ForegroundColor Yellow
try {
    git init
    Write-Host "✓ Repository initialized" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to initialize repository" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Configure git user
Write-Host "[2/6] Configuring Git user..." -ForegroundColor Yellow
git config user.name "Shreyansh Chheda"
git config user.email "shreyansh.chheda@gmail.com"
Write-Host "✓ User configured" -ForegroundColor Green

# Add all files
Write-Host "[3/6] Adding all files to staging..." -ForegroundColor Yellow
try {
    git add .
    $fileCount = (git diff --cached --numstat | Measure-Object).Count
    Write-Host "✓ Added $fileCount files to staging" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create commit
Write-Host "[4/6] Creating initial commit..." -ForegroundColor Yellow
$commitMessage = @"
feat: Complete refactoring with 74% test coverage

- Refactored to modular app/ package structure
- Added comprehensive test suite (121 passing tests)
- Achieved 74% code coverage (87% for main.py)
- Created 5 new test files
- Set up GitHub Actions CI/CD pipeline
- Updated documentation for deployment
"@

try {
    git commit -m $commitMessage
    Write-Host "✓ Commit created" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create commit" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Rename branch to main
Write-Host "[5/6] Renaming branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Branch renamed to main" -ForegroundColor Green

# Add remote
Write-Host "[6/6] Adding GitHub remote..." -ForegroundColor Yellow
try {
    git remote add origin https://github.com/shrey-c/resume-chatbot.git 2>$null
    Write-Host "✓ Remote added" -ForegroundColor Green
} catch {
    Write-Host "⚠ Remote might already exist, continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SUCCESS! Repository initialized." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Push to GitHub" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run the following command:" -ForegroundColor White
Write-Host "  git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "You will need:" -ForegroundColor White
Write-Host "  • Username: shrey-c" -ForegroundColor White
Write-Host "  • Password: Use Personal Access Token (not GitHub password)" -ForegroundColor White
Write-Host ""
Write-Host "To create a Personal Access Token:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "  2. Click 'Generate new token (classic)'" -ForegroundColor White
Write-Host "  3. Select scopes: 'repo' and 'workflow'" -ForegroundColor White
Write-Host "  4. Copy the token and use it as your password" -ForegroundColor White
Write-Host ""
Write-Host "Repository will be available at:" -ForegroundColor Yellow
Write-Host "  https://github.com/shrey-c/resume-chatbot" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to continue"

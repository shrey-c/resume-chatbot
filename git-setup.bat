@echo off
echo ========================================
echo Resume Chatbot - Git Setup Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git is installed. Proceeding...
echo.

REM Initialize git repository
echo [1/6] Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize git repository
    pause
    exit /b 1
)

REM Configure git user (update with your details)
echo [2/6] Configuring Git user...
git config user.name "Shreyansh Chheda"
git config user.email "shreyansh.chheda@gmail.com"

REM Add all files
echo [3/6] Adding all files to staging...
git add .
if %errorlevel% neq 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

REM Commit
echo [4/6] Creating initial commit...
git commit -m "feat: Complete refactoring with 74%% test coverage - Refactored to modular app/ package structure - Added comprehensive test suite (121 passing tests) - Achieved 74%% code coverage - Set up GitHub Actions CI/CD pipeline"
if %errorlevel% neq 0 (
    echo ERROR: Failed to commit
    pause
    exit /b 1
)

REM Rename branch to main
echo [5/6] Renaming branch to main...
git branch -M main

REM Add remote
echo [6/6] Adding GitHub remote...
git remote add origin https://github.com/shrey-c/resume-chatbot.git
if %errorlevel% neq 0 (
    echo Note: Remote might already exist, continuing...
)

echo.
echo ========================================
echo SUCCESS! Repository initialized.
echo ========================================
echo.
echo Next step: Push to GitHub
echo Run: git push -u origin main
echo.
echo You will need:
echo - GitHub username: shrey-c
echo - Personal Access Token (not your password)
echo.
echo To create a token:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Generate new token (classic)
echo 3. Select 'repo' and 'workflow' scopes
echo 4. Copy the token and use it as password
echo.
pause

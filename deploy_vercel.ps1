Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Wallet Platform - Vercel Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js first." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Please install npm first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
npm install -g vercel

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Vercel CLI" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Vercel CLI installed successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "Follow the prompts to complete deployment..." -ForegroundColor Cyan

vercel --prod

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
    Write-Host "Check your Vercel dashboard for the live URL" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed. Check the error messages above." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"

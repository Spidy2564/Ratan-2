@echo off
echo ========================================
echo    Wallet Platform - Vercel Deploy
echo ========================================
echo.

echo Installing Vercel CLI...
npm install -g vercel

echo.
echo Deploying to Vercel...
vercel --prod

echo.
echo Deployment complete!
echo Check your Vercel dashboard for the live URL
pause

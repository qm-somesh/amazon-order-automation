@echo off
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                 🔐 CONFIGURE AMAZON CREDENTIALS                              ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo This script will help you configure your Amazon India credentials.
echo.
echo ⚠️  IMPORTANT: Your credentials will be stored securely in .env file
echo ⚠️  The .env file is excluded from git (won't be uploaded to GitHub)
echo.
pause
echo.
echo Opening .env file in Notepad...
echo.
echo Please replace these lines with YOUR Amazon credentials:
echo   AMAZON_EMAIL=your_email@example.com       ^<-- Replace with your email
echo   AMAZON_PASSWORD=your_secure_password      ^<-- Replace with your password
echo.
echo After editing:
echo   1. Save the file (Ctrl+S)
echo   2. Close Notepad
echo   3. Come back here
echo.
pause

notepad .env

echo.
echo ✅ Credentials configuration complete!
echo.
echo Next step: Run the setup script
echo   Command: .\scripts\setup.bat
echo.
pause

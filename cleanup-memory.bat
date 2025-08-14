@echo off
echo Cleaning up memory-consuming files and directories...

:: Clean Next.js build files
if exist .next rmdir /s /q .next
echo Removed .next directory

:: Clean coverage reports
if exist coverage rmdir /s /q coverage
echo Removed coverage directory

:: Clean build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Removed build/dist directories

:: Clean Turbo cache
if exist .turbo rmdir /s /q .turbo
echo Removed .turbo directory

:: Clean TypeScript build info
if exist tsconfig.tsbuildinfo del tsconfig.tsbuildinfo
echo Removed TypeScript build info

:: Clean standalone builds
if exist standalone rmdir /s /q standalone
echo Removed standalone directory

:: Clean test artifacts
if exist test-results rmdir /s /q test-results
if exist playwright-report rmdir /s /q playwright-report
echo Removed test artifacts

:: Clean log files
for /r %%i in (*.log) do del "%%i" >nul 2>&1
echo Removed log files

:: Clean temp directories
if exist tmp rmdir /s /q tmp
if exist temp rmdir /s /q temp
echo Removed temp directories

echo.
echo Memory cleanup complete!
echo You can now restart VSCode for better performance.
pause
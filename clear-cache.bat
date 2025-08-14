@echo off
echo Clearing project caches and temporary files...

echo Removing .next folder...
rmdir /s /q .next 2>nul

echo Removing node_modules/.cache...
rmdir /s /q node_modules\.cache 2>nul

echo Removing TypeScript build info...
del *.tsbuildinfo 2>nul

echo Removing .turbo folder...
rmdir /s /q .turbo 2>nul

echo Removing coverage folder...
rmdir /s /q coverage 2>nul

echo Removing dist folder...
rmdir /s /q dist 2>nul

echo Removing standalone folder...
rmdir /s /q standalone 2>nul

echo Cache cleared successfully!
echo.
echo To reduce memory usage further:
echo 1. Restart VS Code after clearing cache
echo 2. Open only necessary files
echo 3. Close unused terminal tabs
echo 4. Disable unnecessary extensions
echo 5. Consider increasing Node.js memory: set NODE_OPTIONS=--max-old-space-size=4096
echo.
pause
# Install Supabase CLI on Windows

Write-Host "Installing Supabase CLI..." -ForegroundColor Green

# Method 1: Try with winget (Windows Package Manager)
try {
    Write-Host "`nAttempting installation with winget..." -ForegroundColor Yellow
    winget install --id Supabase.CLI --source winget
    Write-Host "✅ Supabase CLI installed successfully with winget!" -ForegroundColor Green
    supabase --version
    exit 0
} catch {
    Write-Host "⚠️ Winget installation failed, trying alternative method..." -ForegroundColor Yellow
}

# Method 2: Try with Scoop
try {
    # Check if Scoop is installed
    $scoopInstalled = Get-Command scoop -ErrorAction SilentlyContinue
    
    if (-not $scoopInstalled) {
        Write-Host "`nScoop not found. Installing Scoop first..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    }
    
    Write-Host "`nInstalling Supabase CLI with Scoop..." -ForegroundColor Yellow
    scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
    scoop install supabase
    
    Write-Host "✅ Supabase CLI installed successfully with Scoop!" -ForegroundColor Green
    supabase --version
    exit 0
} catch {
    Write-Host "⚠️ Scoop installation failed, trying direct download..." -ForegroundColor Yellow
}

# Method 3: Direct Download
try {
    Write-Host "`nDownloading Supabase CLI directly..." -ForegroundColor Yellow
    
    # Determine architecture
    $arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "386" }
    
    # Get latest version
    $latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/supabase/cli/releases/latest"
    $version = $latestRelease.tag_name -replace 'v', ''
    
    # Download URL
    $downloadUrl = "https://github.com/supabase/cli/releases/download/v$version/supabase_${version}_windows_${arch}.zip"
    $zipPath = "$env:TEMP\supabase.zip"
    $extractPath = "$env:LOCALAPPDATA\supabase"
    
    Write-Host "Downloading from: $downloadUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    
    # Extract
    Write-Host "Extracting to: $extractPath" -ForegroundColor Cyan
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$extractPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$extractPath", "User")
        $env:Path = "$env:Path;$extractPath"
        Write-Host "Added Supabase CLI to PATH" -ForegroundColor Green
    }
    
    # Clean up
    Remove-Item $zipPath
    
    Write-Host "✅ Supabase CLI installed successfully!" -ForegroundColor Green
    Write-Host "⚠️ Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    
    # Test installation
    & "$extractPath\supabase.exe" --version
    
} catch {
    Write-Host "❌ Failed to install Supabase CLI" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    Write-Host "`n📋 Manual Installation Instructions:" -ForegroundColor Cyan
    Write-Host "1. Visit: https://github.com/supabase/cli/releases" -ForegroundColor White
    Write-Host "2. Download the Windows binary for your architecture" -ForegroundColor White
    Write-Host "3. Extract the zip file" -ForegroundColor White
    Write-Host "4. Add the extracted folder to your PATH" -ForegroundColor White
    Write-Host "5. Restart your terminal" -ForegroundColor White
}
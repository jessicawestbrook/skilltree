# Install Supabase CLI on Windows
Write-Host "Installing Supabase CLI..." -ForegroundColor Green

# Method 1: Direct Download
try {
    Write-Host "Downloading Supabase CLI directly..." -ForegroundColor Yellow
    
    # Determine architecture
    $arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "386" }
    
    # Get latest version
    $latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/supabase/cli/releases/latest"
    $version = $latestRelease.tag_name -replace 'v', ''
    
    # Download URL - it's a tar.gz file for Windows
    $downloadUrl = "https://github.com/supabase/cli/releases/download/v$version/supabase_windows_$($arch).tar.gz"
    $zipPath = "$env:TEMP\supabase.tar.gz"
    $extractPath = "$env:LOCALAPPDATA\supabase"
    
    Write-Host "Downloading from: $downloadUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    
    # Extract tar.gz file
    Write-Host "Extracting to: $extractPath" -ForegroundColor Cyan
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }
    New-Item -ItemType Directory -Path $extractPath -Force | Out-Null
    
    # Use tar to extract (available in Windows 10+)
    tar -xzf $zipPath -C $extractPath
    
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$extractPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$extractPath", "User")
        $env:Path = "$env:Path;$extractPath"
        Write-Host "Added Supabase CLI to PATH" -ForegroundColor Green
    }
    
    # Clean up
    Remove-Item $zipPath
    
    Write-Host "Supabase CLI installed successfully!" -ForegroundColor Green
    Write-Host "Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    
    # Test installation
    & "$extractPath\supabase.exe" --version
    
} catch {
    Write-Host "Failed to install Supabase CLI" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
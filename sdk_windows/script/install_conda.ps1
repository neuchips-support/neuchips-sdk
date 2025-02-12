# Define Miniconda installation path and installer name
$CONDA_PATH = "$env:UserProfile\Miniconda3\Scripts\conda.exe"
$INSTALLER = "miniconda.exe"

# Check if Miniconda is already installed
if (Test-Path $CONDA_PATH) {
    Write-Host "Miniconda is already installed at $env:UserProfile\Miniconda3."
    Write-Host "Skipping installation..."
    exit 0
}

# Check if the installer already exists
if (Test-Path $INSTALLER) {
    Write-Host "Installer $INSTALLER already exists. Skipping download..."
} else {
    # Download the Miniconda installer
    Write-Host "Downloading Miniconda installer..."
    Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile $INSTALLER

    # Verify if the download was successful
    if (-not (Test-Path $INSTALLER)) {
        Write-Host "Download failed. Please check your internet connection and try again."
        exit 1
    }
}

# Install Miniconda silently
Write-Host "Installing Miniconda..."
Start-Process -Wait -FilePath ".\$INSTALLER" -ArgumentList "/InstallationType=JustMe", "/RegisterPython=0", "/S", "/D=$env:UserProfile\Miniconda3"

# Remove the installer after installation
Remove-Item -Force $INSTALLER

# Verify if Miniconda was installed successfully
if (-not (Test-Path "$env:UserProfile\Miniconda3")) {
    Write-Host "Miniconda installation failed. Directory $env:UserProfile\Miniconda3 does not exist."
    exit 1
}

# Add Miniconda to the system PATH
Write-Host "Adding Miniconda to PATH..."
$NEW_PATH = "$env:UserProfile\Miniconda3;$env:UserProfile\Miniconda3\Scripts;$env:UserProfile\Miniconda3\Library\bin;$env:Path"
[System.Environment]::SetEnvironmentVariable("Path", $NEW_PATH, [System.EnvironmentVariableTarget]::User)

# Verify installation
Write-Host "Verifying Miniconda installation..."
if (Test-Path $CONDA_PATH) {
    Write-Host "Miniconda installed successfully."
} else {
    Write-Host "Miniconda installation verification failed."
    exit 1
}

Write-Host "Installation completed successfully."
Pause

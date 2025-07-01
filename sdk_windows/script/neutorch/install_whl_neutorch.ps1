# Define the Conda environment name
$ENV_NAME = "neutorch"

# Activate the specified Conda environment
Write-Host "Activating the $ENV_NAME environment..."
conda activate $ENV_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate $ENV_NAME environment."
    exit 1
}

# Run Python script to generate requirements and check for errors
Write-Host "Generating pip requirements..."
python gen_requires.py win
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to run gen_requires.py."
    exit 1
}

# Install packages from requirements.txt and check for errors
Write-Host "Installing packages..."
pip3 install --force-reinstall --no-index -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies from requirements.txt."
    exit 1
}

# Remove requirements.txt and check for errors
Remove-Item -Force requirements.txt -ErrorAction SilentlyContinue
if (Test-Path "requirements.txt") {
    Write-Host "ERROR: Failed to remove requirements.txt."
    exit 1
}

# Confirm success if all commands succeeded
Write-Host "Installation succeeded!"

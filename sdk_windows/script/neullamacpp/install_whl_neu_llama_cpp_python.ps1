# Define the Conda environment name
$ENV_NAME = "neullamacpp"

# Activate the specified Conda environment
Write-Host "Activating the $ENV_NAME environment..."
conda activate $ENV_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate $ENV_NAME environment." -ForegroundColor Red
    exit 1
}

# Run Python script to generate requirements
Write-Host "Generating pip requirements..."
python gen_neu_llama_cpp_python_requires.py win
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to run gen_neu_llama_cpp_python_requires.py." -ForegroundColor Red
    exit 1
}

# Install packages from requirements.txt
Write-Host "Installing packages..."
pip3 install --force-reinstall -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies from requirements.txt." -ForegroundColor Red
    exit 1
}

# Remove requirements.txt
Remove-Item -Force requirements.txt -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to remove requirements.txt." -ForegroundColor Red
    exit 1
}

# Ensure Conda activate.d directory exists
$activateDir = "$env:CONDA_PREFIX\etc\conda\activate.d"
if (!(Test-Path $activateDir)) {
    New-Item -ItemType Directory -Path $activateDir -Force
}

# Set PATH in activation script
$script_path = "$activateDir\set_env.ps1"
$pathUpdate = "`$env:PATH += ';$env:CONDA_PREFIX\Lib\site-packages\torch\lib'"
Set-Content -Path $script_path -Value $pathUpdate -Encoding utf8

Write-Host "Installation succeeded!" -ForegroundColor Green

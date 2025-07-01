# Define the Conda environment name
$ENV_NAME = "neutorch"

# Set the YAML path
$YAML_PATH = "..\..\conda\env_windows.yml"

Write-Host "Checking if $ENV_NAME environment exists..."
$envExists = conda env list | Select-String -Pattern $ENV_NAME

if ($envExists) {
    Write-Host "$ENV_NAME environment found. Updating..."
    conda activate $ENV_NAME
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to activate $ENV_NAME environment."
        exit 1
    }

    conda env update --name $ENV_NAME --file "$YAML_PATH"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Failed to update existing environment."
        exit 1
    }
} else {
    Write-Host "$ENV_NAME environment does not exist. Creating new environment..."

    # Create Conda environment
    conda env create -n $ENV_NAME -f "$YAML_PATH"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create Conda environment."
        exit 1
    }
}

# Check if everything succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Host "Environment setup succeeded!"
} else {
    Write-Host "Environment setup failed!"
    exit 1
}

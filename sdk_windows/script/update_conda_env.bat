@echo off
setlocal

REM Set variables
set "YAML_PATH=..\neu_pytorch_extension\neutorch\conda\env_windows.yml"

echo Checking if neutorch environment exists...
conda env list | findstr "neutorch" >nul
if %ERRORLEVEL% EQU 0 (
    echo neutorch environment found. Updating...
    call conda activate neutorch
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate neutorch environment.
        exit /b 1
    )
    call conda env update --name neutorch --file "%YAML_PATH%"
    if %ERRORLEVEL% NEQ 0 (
        echo Warning: Failed to update existing environment.
        exit /b 1
    )
) else (
    echo neutorch environment does not exist. Creating new environment...
    REM Create Conda environment
    call conda env create -f "%YAML_PATH%"
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create Conda environment.
        exit /b 1
    )
)

REM Check if everything succeeded
if %ERRORLEVEL% EQU 0 (
    echo Environment setup succeeded!
) else (
    echo Environment setup failed!
    exit /b 1
)

endlocal

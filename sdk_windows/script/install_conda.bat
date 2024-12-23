@echo off
set "CONDA_PATH=%UserProfile%\Miniconda3\Scripts\conda.exe"
set "INSTALLER=miniconda.exe"

REM Check if Miniconda is already installed
if exist "%CONDA_PATH%" (
    echo Miniconda is already installed at %UserProfile%\Miniconda3.
    echo Skipping installation...
    exit /b 0
)

REM Check if the installer already exists
if exist "%INSTALLER%" (
    echo Installer %INSTALLER% already exists. Skipping download...
) else (
    REM Download the Miniconda installer
    echo Downloading Miniconda installer...
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o %INSTALLER%

    REM Check if the download was successful
    if errorlevel 1 (
        echo Download failed. Please check your internet connection and try again.
        exit /b 1
    )
)

REM Install Miniconda silently
echo Installing Miniconda...
start /wait "" %INSTALLER% /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3

REM Remove installer after installation
del %INSTALLER%

REM Check if Miniconda was installed successfully
if not exist "%UserProfile%\Miniconda3" (
    echo Miniconda installation failed. Directory %UserProfile%\Miniconda3 does not exist.
    exit /b 1
)

REM Add Miniconda to PATH
echo Adding Miniconda to PATH...
setx PATH "%UserProfile%\Miniconda3;%UserProfile%\Miniconda3\Scripts;%UserProfile%\Miniconda3\Library\bin;%PATH%"

REM Verify installation
echo Verifying Miniconda installation...
if exist "%CONDA_PATH%" (
    echo Miniconda installed successfully.
) else (
    echo Miniconda installation verification failed.
    exit /b 1
)

echo Installation completed successfully.
pause
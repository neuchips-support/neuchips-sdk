@echo off

set "targetDir=C:\Program Files\Neuchips"
if not exist "%targetDir%" (
    echo Creating directory "%targetDir%"...
    mkdir "%targetDir%"
) else (
    echo Directory "%targetDir%" already exists.
)

set "sourceFile=%~dp0neuchips-smi.exe"
if exist "%sourceFile%" (
    echo Copying "neuchips-smi.exe" to "%targetDir%"...
    copy /Y "%sourceFile%" "%targetDir%"
) else (
    echo Error: "neuchips-smi.exe" not found in "%~dp0".
    pause
    exit /b 1
)

set URL=https://live.sysinternals.com/handle64.exe
set OUTPUT=handle64.exe

echo Attempting to download %OUTPUT% ...

:: Try to download the file
powershell -Command "try { Invoke-WebRequest -Uri '%URL%' -OutFile '%OUTPUT%' -ErrorAction Stop; Write-Host 'Download successful: %OUTPUT%' } catch { Write-Host '[Warning]: Download failed!,Please check your network connection' -ForegroundColor Red; exit 1 }"

if not exist "%OUTPUT%" (
    echo Download failed! Checking for "%~dp0%OUTPUT%"...
    if exist "%~dp0%OUTPUT%" (
        echo Found "%OUTPUT%" in the current folder. Copying to "%targetDir%"...
        copy /Y "%~dp0%OUTPUT%" "%targetDir%"
        if %errorlevel% equ 0 (
            echo File successfully copied to "%targetDir%".
        ) else (
            echo Failed to copy "%OUTPUT%" to "%targetDir%". Please check permissions.
            pause
            exit /b 1
        )
    ) else (
        echo [Warning]: "%OUTPUT%" not found in the current folder or could not be downloaded.
    )
) else (
    echo Copying downloaded "%OUTPUT%" to "%targetDir%"...
    copy /Y "%OUTPUT%" "%targetDir%"
    if %errorlevel% equ 0 (
        echo File successfully copied to "%targetDir%".
    ) else (
        echo Failed to copy "%OUTPUT%" to "%targetDir%". Please check permissions.
    )
)

echo Checking if "%targetDir%" is already in PATH...
echo %PATH% | find /I "%targetDir%" >nul
if errorlevel 1 (
    echo Adding "%targetDir%" to PATH...
    setx PATH "%PATH%;%targetDir%" /M
    echo Path updated successfully.
) else (
    echo "%targetDir%" is already in PATH.
)

echo Setup completed. You can now use 'neuchips-smi' as a global command.
pause
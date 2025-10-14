@echo off
set "MINICONDA_ROOT="
set "SDKPATH="

if exist "%USERPROFILE%\venv-neuchips-sdk\Scripts\activate" (
	goto :USE_PYTHON_VENV
) else (
    if exist "%USERPROFILE%\Miniconda3\envs\neutorch" (
		goto :USE_MINICONDA
    ) else (
        echo "ERROR: No Miniconda(%USERPROFILE%\Miniconda3\envs\neutorch) nor python venv(%USERPROFILE%\venv-neuchips-sdk) is pre-installed. Please refer to its installation guide."
        exit /b 1
    )
)

:USE_PYTHON_VENV
call %USERPROFILE%\venv-neuchips-sdk\Scripts\activate
goto :MAIN

:USE_MINICONDA
call %USERPROFILE%\Miniconda3\Scripts\activate.bat %USERPROFILE%\Miniconda3
call conda activate neutorch
for /d %%d in ("%USERPROFILE%\Miniconda*") do (
    set "MINICONDA_ROOT=%%d"
)
set "SDKPATH="

:MAIN

for /f "usebackq delims=" %%i in (`python -c "import sysconfig; print(sysconfig.get_path('purelib'))"`) do (
    set "PYTHON_SITEPACKAGE=%%i"
)

if not defined PYTHON_SITEPACKAGE (
    echo [Error] Could not determine Python site-packages path.
    exit /b 1
)

if not exist "%PYTHON_SITEPACKAGE%\torch\lib\" (
    echo [Warning] torch\lib not found under "%PYTHON_SITEPACKAGE%"
    exit /b 1
)

pushd "%PYTHON_SITEPACKAGE%\..\.."
set "PARENT_DIR=%cd%"
popd

set "TORCH_LIB_DIR=%PYTHON_SITEPACKAGE%\torch\lib"
set "PATH=%PATH%;%PARENT_DIR%;%TORCH_LIB_DIR%"

rem echo [Info] PATH updated:
rem echo %PATH%

cd /d "%~dp0"

set MYPROMPT="Imagine you are an engineer exploring a futuristic underwater research station built inside a massive transparent dome on the ocean floor. Describe in detail what you see as you walk through the curved glass corridors: the shimmering light filtering down from the surface, schools of curious fish drifting past, and the quiet hum of the life support systems. Include the textures, colors, and sounds that make the environment feel alive. Focus especially on the interaction between technology and nature, where marine life brushes up against human invention, creating a sense of both wonder and fragility in this unique setting."

set "CURRENT_DIR=%cd%"
set "LLAMA_BINARY=%CURRENT_DIR%\llama-cli.exe"
set "LLAMA_LIB=%CURRENT_DIR%"
set "PATH=%SDKPATH%;%LLAMA_LIB%;%PATH%;"

set MODEL_FILE=models\llama3\ggml-model-f16.gguf
echo Replace "MODEL_FILE" to the path of your .gguf model file, current default value is %MODEL_FILE%

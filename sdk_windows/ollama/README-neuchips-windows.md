# Ollama Windows for Neuchips Viper Products

Welcome to Ollama for Windows.

No more WSL required!

Ollama now runs as a native Windows application, including NVIDIA and AMD Radeon GPU support.
After installing Ollama for Windows, Ollama will run in the background and
the `ollama` command line is available in `cmd`, `powershell` or your favorite
terminal application. As usual the Ollama [api](https://github.com/ollama/ollama/blob/main/docs/api.md) will be served on
`http://localhost:11434`.

## System Requirements

* Windows 11 23H2 or newer, Home or Pro
* Neuchips N3000 Drivers if you have an N3000 series card

Ollama uses unicode characters for progress indication, which may render as unknown squares in some older terminal fonts in Windows 10. If you see this, try changing your terminal font settings.

## Filesystem Requirements

The Ollama install does not require Administrator, and installs in your home directory by default.  You'll need at least 4GB of space for the binary install.  Once you've installed Ollama, you'll need additional space for storing the Large Language models, which can be tens to hundreds of GB in size.  If your home directory doesn't have enough space, you can change where the binaries are installed, and where the models are stored.

## Neuchips SDK and Conda Requirements

Neuchips Ollama requires Neuchips' SDK and Conda environment. Install Miniconda3 and Neuchips SDK package are required.
Refer to [sdk_windows](https://github.com/neuchips-support/neuchips-sdk/tree/main/sdk_windows) for how to setup this requirement.

> [!NOTE]
> must fulfill this requirement before proceed. If you prefer to use Python venv, please refer to python venv requirements as below.

## Neuchips SDK and Python VENV Requirements

Neuchips' SDK can also run inside python venv. Please follow below steps to resolve package dependencies.

1. Use python version 3.10.x. Ollama executable and Neuchips SDK are tested under Python 3.10.x environment.
   Please check your Python verion is also 3.10.x to avoid unexpected errors.
```bat
Win+R -> cmd -> Microsof Windows Command Prompt
C:\Users\username>python -V
Python 3.10.11
```
* If Python is installed from Microsoft Store, please choose Python 3.10 to install instead of the newest Python 3.13.

2. Create **venv-neuchips-sdk** venv. Please do NOT change **venv-neuchips-sdk** to other name. 
   The venv must be created under %USERPROFILE% path in Microsoft Windows Command Prompt.
```bat
cd %USERPROFILE%
python -m venv venv-neuchips-sdk
```
3. Install required Python packages.
```bat
cd %USERPROFILE%
.\venv-neuchips-sdk\Scripts\activate
python -m pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cpu
```

> [!NOTE]
> must fulfill this requirement before proceed.

### Changing Install Location

To install the Ollama application in a location different than your home directory, start the installer with the following flag

```powershell
NeuchipsOllamaSetup.exe /DIR="d:\some\location"
```

## API Access

Here's a quick example showing API access from `powershell`

```powershell
Invoke-WebRequest -method POST -body '{"name":"llama3.1:8b", "insecure": false}' -uri http://localhost:11434/api/pull
(Invoke-WebRequest -method POST -body '{"model":"llama3.1:8b", "prompt":"Why is the sky blue?", "stream": false}' -uri http://localhost:11434/api/generate ).Content | ConvertFrom-json
```

## Troubleshooting

Neuchips Ollama on Windows stores files in a few different locations.  You can view them in
the explorer window by hitting `<Ctrl>+R` and type in:
- `explorer %LOCALAPPDATA%\Ollama` contains logs, and downloaded updates
    - *app.log* contains most resent logs from the GUI application
    - *server.log* contains the most recent server logs

- `explorer %LOCALAPPDATA%\Programs\Ollama` contains the binaries (The installer adds this to your user PATH)
- `explorer %HOMEPATH%\.ollama` contains models and configuration
> [!NOTE]
> Neuchips ollama versions update is done via latest **NeuchipsOllamaSetup.exe** installation, not updated from live update.

## Uninstall

The Ollama Windows installer registers an Uninstaller application.  Under `Add or remove programs` in Windows Settings, you can uninstall Ollama.

## Standalone CLI

The easiest way to install Ollama on Windows is to use the `NeuchipsOllamaSetup.exe`
installer. It installs in your account without requiring Administrator rights.
We update Ollama regularly to support the latest models, and this installer will
help you keep up to date.

> [!NOTE]  
> If you are upgrading from a prior version, you should remove the old directories first.

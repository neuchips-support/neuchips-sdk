# Llama.cpp Windows for Neuchips Viper Products

Neuchips has integrated Viper products to work with Llama.cpp.

Llama.cpp(llama-cli.exe or llama-server.exe) now runs as a native Windows application,
you may choose use Conda environment or Python venv to run these programs.

## System Requirements

* Windows 11 23H2 or newer, Home or Pro
* Neuchips N3000 Drivers if you have an N3000 series card

## Neuchips SDK and Conda Requirements

Neuchips's Llama.cpp integration requires Neuchips' SDK and Conda environment. Install Miniconda3 and Neuchips SDK package are required.
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

## Running llama-cli.exe

Use below steps to run llama-cli.exe with Viper products.
```bat
cd neuchips-sdk\sdk_windows\llama.cpp

.\prepare_env.bat

set MYPROMPT="Imagine you are an engineer exploring a futuristic underwater research station built inside a massive transparent dome on the ocean floor. Describe in detail what you see as you walk through the curved glass corridors: the shimmering light filtering down from the surface, schools of curious fish drifting past, and the quiet hum of the life support systems. Include the textures, colors, and sounds that make the environment feel alive. Focus especially on the interaction between technology and nature, where marine life brushes up against human invention, creating a sense of both wonder and fragility in this unique setting."

set MODEL_FILE=models\llama3\ggml-model-f16.gguf
.\llama-cli.exe --no-warmup -c 0 -m %MODEL_FILE% -p ""%MYPROMPT%"" -ub 256 -t 6 -n 64 --jinja -no-cnv
```

## Running llama-server.exe
In a new Windows prompt command console,
```bat
.\prepare_env.bat
set MODEL_FILE=models\llama3\ggml-model-f16.gguf
.\llama-server.exe -m %MODEL_FILE% --api-key test_key --slots --metrics
```

In another Windows prompt command console,
```bat
curl --request POST --url http://localhost:8080/completion ^
--header "Authorization: Bearer test_key" ^
--header "Content-Type: application/json" ^
--data "{\"prompt\": \"Hello, how are you?\", \"n_predict\": 16, \"stream\": false}"
```
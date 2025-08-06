<div align="center">
</div>

# Ollama for Viper

Get up and running with large language models with Viper card.

## Limitations

Currently, Viper cards only support bf16 or fp16 formant of .gguf model files.

### Linux environment setting

```shell
conda activate neutorch
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH
```

## CLI Reference


### Start Ollama

`ollama serve` is used when you want to start ollama without running the desktop application.

### Running local builds

Next, start the server:

```shell
./ollama serve
```

### Pull a model

```shell
./ollama pull llama3.1:8b-instruct-fp16
```

> **Output**: pulling 09cd6813dc2e: 100% ▕██████████████████████████████████████████████████████████████████████▏  16 GB

Finally, in a separate shell, run a model:

```shell
./ollama run llama3.1:8b-instruct-fp16 "hi"
```
> **Output**: How are you doing today? Is there something I can help with or would you like to chat?

### Remove a model

```shell
./ollama rm llama3.1:8b-instruct-fp16
```

### Pass the prompt as an argument

```shell
./ollama run llama3.1:8b-instruct-fp16 "Summarize this file: $(cat README.md)"
```

### Show model information

```shell
./ollama show llama3.1:8b-instruct-fp16
```

### List models on your computer

```shell
./ollama list
```

### List which models are currently loaded

```shell
./ollama ps
```

### Stop a model which is currently running

```shell
./ollama stop llama3.1:8b-instruct-fp16
```

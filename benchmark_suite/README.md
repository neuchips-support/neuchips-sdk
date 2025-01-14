# Benchmark Suite

Benchmark suite for Neutorch SDK with Neuchips Viper

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Configuration](#configuration)
4. [Benchmark](#benchmark)


## Introduction
This Benchmark Suite is designed to evaluate the performance of Neuchips Viper GenAI processing card. It supports multiple testing environments and offers a comprehensive set of metrics to measure key performance indicators such as First token lateny, Output TPS, Prompt TPS, Generation TPS etc.

## Requirements
You need to first follow the SDK instructions to set up the Neutorch environment properly, and most importantly, make sure to insert the Neuchips Viper card 🎇.
Afterward, install the required Python modules for benchmarking by running the following command:
```
pip install -r requirements.txt
```


## Configuration

### Download LLM model from Huggingface

To download the original LLM model weights from Hugging Face, follow these steps:

Visit the Hugging Face Website:

Go to https://huggingface.co/ in your web browser.
Search for the Model:

Use the search bar to find the specific LLM model you want to download. For example, you might search for "Llama," "mistral," or "Gemma," depending on the model you're interested in.
Select the Model Repository:

Once you find the desired model, click on its repository to enter its page.
Download the Model Weights:

On the model page, look for the "Files and versions" tab. You should find the model weights.
Click on the file you need to download, or you can use Git LFS (Large File Storage) if the files are large.

Alternatively, if you're using a terminal, you can clone the repository or download the weights via the Hugging Face Python library.

## Benchmark

### Single Model Benchmark
```
python benchmark.py \
                --target_model ./model_zoo/Llama-3.1-8B-Instruct \
                --prompt_gen \
                --prompt_list "128-256-512-1024-2048" \
                --gen_list "1-128-256-512-1024-2048" \
                --benchmark
```

### Model Zoo Benchmark
```
 python benchmark.py \
                --model_zoo_path ./model_zoo/ \
                --prompt_gen \
                --prompt_list "128-256-512-1024-2048" \
                --gen_list "128-256-512-1024-2048" \
                --benchmark

```
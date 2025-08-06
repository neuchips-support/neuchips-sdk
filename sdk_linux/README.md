# NEUCHIPS Extension for PyTorch
Neuchips Extension for PyTorch extends PyTorch with up-to-date features optimizations for an extra performance boost on Neuchips hardware.

The extension can be loaded as a Python module for Python programs. In Python scripts users can enable it dynamically by `import neutorch`.


# Getting Started
## Conda setup
1. Install conda, Anaconda[https://www.anaconda.com/download] is our recommended package manager.
2. Create a new conda environment in two ways,

* (Suggested) From a proven conda environment yml file

```bash
conda env create -f conda/env_linux.yml
```

* (Create your) With commands
```
# python version >= 3.10
conda create --name <env name> python=<your decision>

conda activate <env name>

# Install the latest official released pytorch with pip or with conda
# Ex.
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install other packages, such as transformers ..., etc.
# Ex.
# pip3 install transformers accelerate sentencepiece importlib-resources protobuf parameterized pybind11 ninja

```

## Install Neuchips PyTorch extension
Once you have obtained the Neuchips PyTorch extension, you can easily install it via `pip`, the installation command is as follows:

```
cd script/neutorch
conda activate neutorch
python3 gen_requires.py linux
pip3 install --force-reinstall --no-index -r requirements.txt
```

This command will install the extension into your Python environment. Once it is installed, you can import it into your Python code as follows:

```Python
import neutorch
```
This will import the Neuchips PyTorch extension into your Python environment. You can then use it to access Neuchips hardware accelerators.


## Running example
Before running the sample, you should prepare the model data and modify the path settings in the sample code.

```
self.default_test_model = get_model_path("meta-llama/Llama-2-7b-chat-hf")
```
When everything is ready, execute the sample and explore with the program.

```bash
# Must have model files
cd neu_pytorch_extension/neutorch/test/ && python3 test_neutorch_for_release.py
```


# Supported Models
We currently only support Hugging Face Transformers-formatted models (LlamaForCausalLM and MistralForCausalLM). We will update this list once we have verified more models.

| Name | Url |
|------|-----|
| LLaMA 2 7B | https://huggingface.co/meta-llama/Llama-2-7b-hf |
| LLaMA 2 7B Chat | https://huggingface.co/meta-llama/Llama-2-7b-chat-hf |
| LLaMA 2 13B | https://huggingface.co/meta-llama/Llama-2-13b-hf |
| LLaMA 2 13B Chat | https://huggingface.co/meta-llama/Llama-2-13b-chat-hf |
| LLaMA 3 8B | https://huggingface.co/meta-llama/Meta-Llama-3-8B |
| | https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct |
| LLaMA 3.1 8B | https://huggingface.co/meta-llama/Llama-3.1-8B |
| | https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct |
| LLaMA 3.2 3B | https://huggingface.co/meta-llama/Llama-3.2-3B |
| | https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct |
| Code Llama 7B | https://huggingface.co/codellama/CodeLlama-7b-hf |
| Code Llama 7B Python | https://huggingface.co/codellama/CodeLlama-7b-Python-hf |
| Code Llama 13B | https://huggingface.co/codellama/CodeLlama-13b-hf |
| Code Llama 13B Python | https://huggingface.co/codellama/CodeLlama-13b-Python-hf |
| ELYZA-japanese-Llama-2-7b | https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b |
| | https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct |
| Mistral 7B | https://huggingface.co/mistralai/Mistral-7B-v0.3 |
| | https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 |
| Mistral Nemo | https://huggingface.co/mistralai/Mistral-Nemo-Base-2407 |
| | https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407 |
| Ministral 8B | https://huggingface.co/mistralai/Ministral-8B-Instruct-2410 |
| Breeze 7B | https://huggingface.co/MediaTek-Research/Breeze-7B-Base-v1_0 |
| | https://huggingface.co/MediaTek-Research/Breeze-7B-Instruct-v1_0 |
| Phi-2 | https://huggingface.co/microsoft/phi-2 |
| Phi-3-mini-4k-instruct | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct |
| Phi-3.5-mini-instruct | https://huggingface.co/microsoft/Phi-3.5-mini-instruct |
| Phi-4-mini-instruct  | https://huggingface.co/microsoft/Phi-4-mini-instruct |
| Phi-4-mini-reasoning | https://huggingface.co/microsoft/Phi-4-mini-reasoning |
| Gemma 2 9B | https://huggingface.co/google/gemma-2-9b |
| | https://huggingface.co/google/gemma-2-9b-it |
| TAIDE-LX-7B | https://huggingface.co/taide/TAIDE-LX-7B |
| | https://huggingface.co/taide/TAIDE-LX-7B-Chat |
| TAIDEL-LX-8B | https://huggingface.co/taide/Llama-3.1-TAIDE-LX-8B-Chat |
| Qwen 2.5 7B | https://huggingface.co/Qwen/Qwen2.5-7B |
| | https://huggingface.co/Qwen/Qwen2.5-7B-Instruct |
| Qwen 2.5 14B | https://huggingface.co/Qwen/Qwen2.5-14B |
| | https://huggingface.co/Qwen/Qwen2.5-14B-Instruct |
| Qwen 3 8B | https://huggingface.co/Qwen/Qwen3-8B |
| Qwen 3 14B | https://huggingface.co/Qwen/Qwen3-14B |
| DeepSeek R1 Distill Llama 8B | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B |
| DeepSeek R1 Distill Qwen 7B | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B |
| DeepSeek R1 Distill Qwen 14B | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B |
| DeepSeek R1 0528 Qwen 3B | https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B |
| Yi 1.5 9B | https://huggingface.co/01-ai/Yi-1.5-9B |
| | https://huggingface.co/01-ai/Yi-1.5-9B-Chat |
| Yi Coder 9B | https://huggingface.co/01-ai/Yi-Coder-9B |
| | https://huggingface.co/01-ai/Yi-Coder-9B-Chat |


# Performance
The following is the performance data of each model when the input and output lengths are 128 tokens, the unit is tps (tokens per second)

| Model | Prompt | Generation | Performance |
|-------|--------|------------|-------------|
| LLaMA 2 7B | 7.3 | 6.3 | 3.4 |
| LLaMA 3 8B | 6.8 | 5.7 | 3.1 |
| Mistral 7B | 7.0 | 6.2 | 3.3 |
| Breeze 7B | 6.9 | 6.1 | 3.3 |
| Phi-2 | 12.4 | 9.9 | 5.5 |

When `use_matrix=True` is applied in `neutorch._C.set_device()`, the tps for prompt will be increased.

| Model | Prompt | Generation | Performance |
|-------|--------|------------|-------------|
| LLaMA 2 7B | 98.7 | 6.1 | 5.7 |
| LLaMA 3 8B | 73.2 | 5.4 | 5.0 |
| Mistral 7B | 103.1 | 6.1 | 5.8 |
| Breeze 7B | 85.4 | 5.7 | 5.3 |
| Phi-2 | 179.8 | 7.0 | 6.7 |

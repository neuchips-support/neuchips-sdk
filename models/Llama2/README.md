# NEUCHIPS Extension for PyTorch
Neuchips Extension for PyTorch extends PyTorch with up-to-date features optimizations for an extra performance boost on Neuchips hardware.

The extension can be loaded as a Python module for Python programs or linked as a C++ library for C++ programs. In Python scripts users can enable it dynamically by `import neutorch`.


# Getting Started
## Conda setup
1. Install conda, Anaconda[https://www.anaconda.com/download] is our recommended package manager.
2. Create a new conda environment in two ways,
* (Suggested) From a proven conda environment yml file
```bash
conda env create -f conda/env.yml
```
Then activate the environment and start developing.
```bash
conda activate neutorch
```

* (Create your) With commands
```
# python version == 3.10
conda create --name <env name> python=3.10

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
Once you have obtained the Neuchips PyTorch extension, you can easily install it via `pip`. Assuming the filename is `neutorch-0.1.0+a86d524-py2.py3-none-any.whl`, then the installation command is as follows:

```
pip install neutorch-0.1.0+a86d524-py2.py3-none-any.whl
```
This command will install the extension into your Python environment. Once it is installed, you can import it into your Python code as follows:

```Python
import neutorch
```
This will import the Neuchips PyTorch extension into your Python environment. You can then use it to access Neuchips hardware accelerators.


## Running example
Before running the sample, you should prepare the model data and modify the path settings in the sample code.

```
self.default_test_model = "/data/models/meta-llama/Llama-2-7b-chat-hf"
```
When everything is ready, execute the sample and explore with the program.

```bash
# Must have model files
cd examples && python3 test_llama_for_release.py
```


# Supported Models
We currently only support Hugging Face Transformers-formatted models (LlamaForCausalLM and MistralForCausalLM). We will update this list once we have verified more models.

| Name | Url |
|------|-----|
| LLaMA 2 7B | https://huggingface.co/meta-llama/Llama-2-7b-hf |
| LLaMA 2 7B Chat | https://huggingface.co/meta-llama/Llama-2-7b-chat-hf |
| LLaMA 2 13B | https://huggingface.co/meta-llama/Llama-2-13b-hf |
| LLaMA 2 13B Chat | https://huggingface.co/meta-llama/Llama-2-13b-chat-hf |
| Code Llama 7B | https://huggingface.co/codellama/CodeLlama-7b-hf |
| Code Llama 7B Python | https://huggingface.co/codellama/CodeLlama-7b-Python-hf |
| Code Llama 13B | https://huggingface.co/codellama/CodeLlama-13b-hf |
| Code Llama 13B Python | https://huggingface.co/codellama/CodeLlama-13b-Python-hf |
| ELYZA-japanese-Llama-2-7b | https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b |
| | https://huggingface.co/elyza/ELYZA-japanese-Llama-2-7b-instruct |
| Mistral 7B | https://huggingface.co/mistralai/Mistral-7B-v0.1 |
| | https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2 |
| Breeze 7B | https://huggingface.co/MediaTek-Research/Breeze-7B-Base-v1_0 |
| | https://huggingface.co/MediaTek-Research/Breeze-7B-Instruct-v1_0 |


# Performance
The following is the performance data of each model when the input and output lengths are 128 tokens, the unit is tps (tokens per second)

| Model | Prompt | Generation | Performance |
|-------|--------|------------|-------------|
| LLaMA 2 7B | 7.0 | 6.1 | 3.3 |
| LLaMA 2 13B | 3.5 | 3.2 | 1.7 |
| Mistral 7B | 6.7 | 6.0 | 3.2 |
| Breeze 7B | 6.7 | 5.9 | 3.2 |


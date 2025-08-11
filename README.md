# NEUCHIPS Support Site

This Github page provides information on software development kit (SDK) for neuchips products, including sample code, documentation, and known issues. Neutorch is an SDK developed based on the PyTorch extension, and currently supports the Neuchips accelerator Raptor and Parrot chip, PCIe card including Viper, Phoeinx, and DM2 product.

# How to Use This SW Package
The prerequisites such as fw update and pcie driver setup are not mentioned here.
Please contact Neuchips for the documents by sending emails to contact@neuchips.ai.

```bash
# Step 1:
# Install docker engine
# https://docs.docker.com/engine/install/

# Step 2:
# Clone the sw package and its folder is denoted as PATH-TO-NEUCHIPS-SDK.
git clone https://github.com/neuchips-support/neuchips-sdk.git
cd PATH-TO-NEUCHIPS-SDK
git checkout nchc

# Step 3:
# Download the model supported by Neuchips.
# For example, download the model google/gemma-3-4b-it from https://huggingface.co/google/gemma-3-4b-it.
# Since the default file format from huggingface is safetensors and neuchips sdk is integrated with llama.cpp which uses another file format gguf, you need to convert the download model to gguf format.
# Don't worry. The project llama.cpp has the script for achieving this.
# Clone llama.cpp and the folder is denoted as PATH-TO-LLAMA-CPP.
git clone https://github.com/ggml-org/llama.cpp.git
cd PATH-TO-LLAMA-CPP
# This command will convert the model to gguf file and save it in the current working directory.
python3 convert_hf_to_gguf.py --outtype f16 /path/to/huggingface-model-folder/
# Please see the help messages if you need more controls in the convert process.
python3 convert_hf_to_gguf.py --help

# Step 4:
# Setup environment variables for docker.
# The environment variables are defined in the files docker/env_* as examples.
# Take the file env_gemma3_4b as an example,
# docker will go to $HOST_MODEL_FOLDER to find the gguf file $MODEL.
# docker will also go to $HOST_CACHE_FOLDER to find any neuchips sdk data generated in the previous session. If yes, then sdk can reuse them this time. If no, then sdk will generate these data and save them in $HOST_CACHE_FOLDER.
# So, it's suggested to create the below folders:
#   - /neuchips/models_zoo (refered by HOST_MODEL_FOLDER)
#   - /neuchips/models_cache (refered by HOST_CACHE_FOLDER)
# And put the gguf files to /neuchips/models_zoo.
# Or if you'd like to customize these folders and file names, then please
# define these variables HOST_MODEL_FOLDER, HOST_CACHE_FOLDER, and MODEL properly in docker/env_*.

# Step 5:
# Build docker image. If you get any prompt, then follow the default value is fine.
cd PATH-TO-NEUCHIPS-SDK/docker
./docker.sh --help
sudo ./docker.sh build

# Step 6:
# Run docker image to activate the llama server
sudo ./docker.sh run ENV_FILE
# ex: sudo ./docker.sh run ./env_gemma3_4b

# Step 7:
# Test llama server by sending curl request from client
./docker.sh test -p PROMPT(or -f PROMPT_TXT_FILE) [MAX_TOKENS        (default: $MAX_TOKENS)]"
# ex: ./docker.sh test -p "Wikipedia is" 128
```

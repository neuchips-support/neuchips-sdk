# NEUCHIPS Support Site

This Github page provides information on software development kit (SDK) for neuchips products, including sample code, documentation, and known issues. Neutorch is an SDK developed based on the PyTorch extension, and currently supports the Neuchips accelerator Raptor and Parrot chip, PCIe card including Viper, Phoeinx, and DM2 product.

# How to Use This SW Package
The prerequisites such as fw update and pcie driver setup are not mentioned here.
Please ask Neuchips for the documents.

```bash
# Step 1:
# Install docker engine
# https://docs.docker.com/engine/install/

# Step 2:
# Clone the sw package
git clone https://github.com/neuchips-support/neuchips-sdk.git
cd neuchips-sdk
git checkout nchc

# Step 3:
# Download the model supported by Neuchips.
# For example, Meta-Llama-3-8B-Instruct-F16.gguf, which can be downloaded from HuggingFace.

# Step 4:
# Setup environment variables.
# The environment variables are defined in the file docker/env_llama3.
# By default, you should create the below folders.
#   - /neuchips/models_zoo (refered by HOST_MODEL_FOLDER)
#   - /neuchips/models_cache (refered by HOST_CACHE_FOLDER)
# And put the downloaded models to /neuchips/models_zoo.
# Or you should customize HOST_MODEL_FOLDER or HOST_CACHE_FOLDER in docker/env_llama3.

# Step 5:
# Build docker image
cd docker
sudo ./docker.sh build

# Step 6:
# Run docker image to activate the llama server
sudo ./docker.sh run

# Step 7:
# Test llama server by sending curl request from client
./docker.sh test

```

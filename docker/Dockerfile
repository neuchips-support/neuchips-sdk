# Using Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
RUN apt-get install -y --no-install-recommends \
        wget \
        pciutils
RUN apt-get clean

RUN mkdir /neuchips

# Download Neuchips SDK
RUN wget https://github.com/neuchips-support/neuchips-sdk/archive/refs/tags/LLM_SDK_1.4.1.tar.gz -O - | tar -zxvf - -C /neuchips/ \
    && cp -r /neuchips/neuchips-sdk-LLM_SDK_1.4.1/sdk_linux/llama.cpp /neuchips \
    && cp /neuchips/neuchips-sdk-LLM_SDK_1.4.1/sdk_linux/conda/env_linux.yml /env.yml \
    && rm -f /sdk.tgz

# === Conda ===
# Download the Miniconda installation script and install Miniconda
#RUN wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh -O /conda.sh \
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /conda.sh \
    && bash /conda.sh -b -p /neuchips/conda \
    && rm /conda.sh

# Add Miniconda's bin directory to PATH, so conda command can be used directly
ENV PATH=/neuchips/conda/bin:$PATH

# Use conda to create the environment, regardless of how ENV_FILE is specified,
# use /env.yml as the environment file
RUN conda env create -f /env.yml \
    && conda clean -afy \
    && echo "source activate neutorch" >> ~/.bashrc \
    && echo "conda activate neutorch" >> ~/.bashrc \
    && rm -f /env.yml

# Download dockerfile
RUN wget https://github.com/neuchips-support/neuchips-sdk/releases/download/LLM_SDK_1.4.1/start-neuchips-service.sh -O /neuchips/start-neuchips-service.sh

CMD ["/bin/bash", "/neuchips/start-neuchips-service.sh" ]

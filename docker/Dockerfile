# Using Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
RUN apt-get install -y --no-install-recommends \
        wget \
        pciutils \
        moreutils
RUN apt-get clean

RUN mkdir -p /neuchips/llama.cpp

COPY sdk_linux/llama.cpp /neuchips/llama.cpp
COPY sdk_linux/conda/env_linux.yml /env.yml
COPY docker/start-neuchips-service.sh /neuchips

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

CMD ["/bin/bash", "/neuchips/start-neuchips-service.sh" ]

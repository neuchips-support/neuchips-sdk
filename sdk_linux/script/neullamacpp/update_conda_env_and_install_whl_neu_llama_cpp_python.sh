#!/bin/bash

# please make sure you already installed conda environment to ~/anaconda3 path first
source ~/anaconda3/etc/profile.d/conda.sh

ENV_NAME="neullamacpp"
ENV_FILE_PATH="../../conda/env_linux.yml"
if conda env list | grep -q "$ENV_NAME"; then
    echo "update env $ENV_NAME..."
    conda env update --name "$ENV_NAME" --file "$ENV_FILE_PATH"
else
    echo "create env $ENV_NAME..."
    conda env create --name "$ENV_NAME" --file "$ENV_FILE_PATH"
fi

conda activate $ENV_NAME
# Wait for the environment activation to stabilize
sleep 1

conda env config vars set LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH


conda activate $ENV_NAME
# Reload the env
sleep 1

python3 gen_neu_llama_cpp_python_requires.py linux
pip3 install --force-reinstall -r requirements.txt

RET_CODE=$?
if [ $RET_CODE -ne 0 ]; then
    echo "============== Update Neuchips Llama Cpp Python Failed =============="
    exit -1
else
    echo "============== Update Neuchips Llama Cpp Python Succeed =============="
fi

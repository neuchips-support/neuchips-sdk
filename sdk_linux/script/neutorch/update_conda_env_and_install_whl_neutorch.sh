#!/bin/bash

# please make sure you already installed conda environment to ~/anaconda3 path first
source ~/anaconda3/etc/profile.d/conda.sh

ENV_NAME="neutorch"
ENV_FILE_PATH="../../conda/env_linux.yml"
if conda env list | grep -q "$ENV_NAME"; then
    echo "update env $ENV_NAME..."
    conda env update --name "$ENV_NAME" --file "$ENV_FILE_PATH"
else
    echo "create env $ENV_NAME..."
    conda env create --name "$ENV_NAME" --file "$ENV_FILE_PATH"
fi

conda activate $ENV_NAME
python3 gen_requires.py linux
pip3 install --force-reinstall --no-index -r requirements.txt

RET_CODE=$?
if [ $RET_CODE -ne 0 ]; then
    echo "============== Update Neuchips Pytorch Extension Failed =============="
    exit -1
else
    echo "============== Update Neuchips Pytorch Extension Succeed =============="
fi

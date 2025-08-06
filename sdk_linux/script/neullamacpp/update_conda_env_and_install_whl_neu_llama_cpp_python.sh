#!/usr/bin/env bash

if ! command -v conda &>/dev/null; then
  if [[ -f "$HOME/anaconda3/bin/conda" ]]; then
    export PATH="$HOME/anaconda3/bin:$PATH"
  elif [[ -f "$HOME/miniconda3/bin/conda" ]]; then
    export PATH="$HOME/miniconda3/bin:$PATH"
  else
    echo "Error: conda command not found. Please install Anaconda or Miniconda first." >&2
    exit 1
  fi
fi

CONDA_BASE=$(conda info --base) || {
  echo "Error: could not determine Conda base path." >&2
  exit 1
}

CONDA_SH="$CONDA_BASE/etc/profile.d/conda.sh"
if [[ -f "$CONDA_SH" ]]; then
  source "$CONDA_SH"
else
  echo "Error: cannot find $CONDA_SH." >&2
  exit 1
fi

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

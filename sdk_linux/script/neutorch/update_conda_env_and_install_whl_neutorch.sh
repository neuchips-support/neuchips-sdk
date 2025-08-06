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

#!/bin/bash

PYTORCH_VERSION=`python -c "import torch; print(torch.__version__)"`
if [[ ! "$PYTORCH_VERSION" =~ ^2\.[4|5] ]]; then
  echo
  echo "The current PyTorch version is $PYTORCH_VERSION , but this program only supports version 2.4 above."
  echo 
  exit 1
fi

PYTHON_SITEPACKAGE=`python -c "import sysconfig; print(sysconfig.get_path('purelib'))"`
if [ ! -z $PYTHON_SITEPACKAGE ]; then
  if [ -d $PYTHON_SITEPACKAGE/torch/lib ]; then
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PYTHON_SITEPACKAGE/../..:$PYTHON_SITEPACKAGE/torch/lib
  fi
fi

BASEDIR=$(dirname "$0")

LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$BASEDIR $BASEDIR/llama-server "$@"

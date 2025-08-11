#!/bin/bash

SDK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LLAMA_ROOT=${SDK_ROOT}/llama.cpp
MODEL_PATH="${DOCKER_MODEL_FOLDER}/${MODEL}"
CACHE_PATH="${DOCKER_CACHE_FOLDER}"

export LD_LIBRARY_PATH=/neuchips/conda/envs/neutorch/lib:/neuchips/conda/envs/neutorch/lib/python3.10/site-packages/torch/lib

mkdir -p "${CACHE_PATH}"

"${LLAMA_ROOT}"/llama-server -m "${MODEL_PATH}" \
    -v \
    -np 1 \
    -ub 256 \
    -c 81920 \
    -t 8 \
    --threads-http 1 \
    --queued-http-reqs 3 \
    --host 0.0.0.0 \
    --port "${PORT}" \
    --api-key "${API_KEY}" \
    --nr-devices "${NUM_N3K}" \
    --slots \
    --metrics \
    --neutorch-cache-path "${CACHE_PATH}" \
    2>&1 | ts | tee /neuchips/llama.log

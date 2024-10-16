#!/bin/bash
# model_list=("meta-llama/Llama-3.2-3B-Instruct" \
# "meta-llama/Llama-3.1-8B-Instruct" \
# "meta-llama/Llama-2-7b-chat-hf" \
# "meta-llama/Llama-2-13b-chat-hf" \
# 		"mistralai/Mistral-7B-v0.3" \
# 		"mistralai/Mistral-Nemo-Instruct-2407" \
# 		"google/gemma-2-2b-it" \
# 		"google/gemma-2-9b-it" \
# 		"microsoft/Phi-3-mini-4k-instruct" \
# 		"microsoft/Phi-3.5-mini-instruct" \
# 		"microsoft/phi-2")

model_list=("meta-llama/Llama-3.1-8B-Instruct")

for i in ${model_list[@]}
do
	echo $i
	python HF_weight_downloader.py --model_name $i --org_weight_only
done




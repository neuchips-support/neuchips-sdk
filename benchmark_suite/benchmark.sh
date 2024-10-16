HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \

# single model benchmark
python benchmark.py \
		--target_model ./model_zoo/Llama-3.1-8B-Instruct \
		--prompt_gen \
		--prompt_list "128-256-512-1024-2048" \
		--gen_list "1-128-256-512-1024-2048" \
	    --benchmark

# model zoo benchmark
# python benchmark.py --model_zoo_path ./model_zoo/ \
#                 --prompt_gen \
#                 --prompt_list "128-2048" \
#                 --gen_list "1-128-2048" \
#                 --benchmark



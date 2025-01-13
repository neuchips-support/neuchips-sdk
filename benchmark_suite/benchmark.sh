HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \


export OMP_SCHEDULE=STATIC
export OMP_NUM_THREADS=8 #Core(s) per socket
export OMP_DYNAMIC=FALSE


# single model benchmark
python benchmark.py \
		--target_model /home/user/kevin/benchmark_suite/model_zoo/Mistral-Nemo-Instruct-2407 \
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



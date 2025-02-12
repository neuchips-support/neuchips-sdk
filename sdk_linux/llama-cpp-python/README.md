# Llama-cpp-python for Viper

This is the initial llama-cpp-python support for Viper, install conda and execute ../script/neullamacpp/update_conda_env_and_install_whl_neu_llama_cpp_python.sh to setup the environment.

# Sample codes for testing

While most test scripts in [this repo](https://github.com/abetlen/llama-cpp-python/tree/main/examples) should
run, we'll use `high_level_api_inference.py` as our example.

# Converting models from HuggingFace

You can find a list of supported models in the [README.md](https://github.com/neuchips-support/neuchips-sdk/tree/main/sdk_linux#readme) file.
The `convert_hf_to_gguf.py` script (cloned from https://github.com/ggerganov/llama.cpp/tree/0827b2c1da299805288abbd556d869318f2b121e) allows you to convert these models to the gguf format.

Ex: 
```
$ conda activate neullamacpp # (optional, or make sure you have those packages installed: 'sentencepiece, tokenizers, numpy, pyyaml')
$ python convert_hf_to_gguf.py  --outtype f16 /data/models/meta-llama//Meta-Llama-3.1-8B-Instruct --outfile models/Meta-Llama-3.1-8B-Instruct-F16.gguf
```

# Running sample code

```
$ conda activate neullamacpp # (optional)
$ python high_level_api_inference.py ../models/Meta-Llama-3.1-8B-Instruct-F16.gguf
```

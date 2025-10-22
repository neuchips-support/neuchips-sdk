# Llama.cpp tool for Viper

This is the initial llama.cpp support for Viper, for using this tool you have to install pytorch 2.4.0 or above.
```
$ cd sdk_linux/script/neutorch/
$ ./update_conda_env_and_install_whl_neutorch.sh
```

# Converting models from HuggingFace

You can find a list of supported models in the [README.md](https://github.com/neuchips-support/neuchips-sdk/tree/main/sdk_linux#readme) file.
The `convert_hf_to_gguf.py` script (cloned from https://github.com/ggerganov/llama.cpp/tree/0827b2c1da299805288abbd556d869318f2b121e) allows you to convert these models to the gguf format.

Ex: 
```
$ conda activate neutorch # (optional, or make sure you have those packages installed: 'sentencepiece, tokenizers, numpy, pyyaml')
$ cd sdk_linux/llama.cpp/
$ python convert_hf_to_gguf.py  --outtype f16 /data/models/meta-llama//Meta-Llama-3.1-8B-Instruct --outfile models/Meta-Llama-3.1-8B-Instruct-F16.gguf
```

# Running llama.cpp

```
$ cd sdk_linux/llama.cpp/
$ chmod +x llama.sh
$ conda activate neutorch
$ ./llama.sh -m ../models/Meta-Llama-3.1-8B-Instruct-F16.gguf --neutorch-cache-path ./cache/Meta-Llama-3.1-8B-Instruct -no-cnv -t 6 -c 0 -n 256 -ub 256 --jinja -p "There's a llama in my garden, What should I do? "
```

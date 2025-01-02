# Llama.cpp tool for Viper

This is the initial llama.cpp support for Viper, for using this tool you have to install pytorch 2.4.0 or above.

# Converting models from HuggingFace

You can find a list of supported models in the [README.md](https://github.com/neuchips-support/neuchips-sdk/tree/main/sdk_linux#readme) file.
The `convert_hf_to_gguf.py` script (cloned from https://github.com/ggerganov/llama.cpp/tree/0827b2c1da299805288abbd556d869318f2b121e) allows you to convert these models to the gguf format.

Ex: 
```
$ conda activate neutorch # (optional, or make sure you have those packages installed: 'sentencepiece, tokenizers, numpy, pyyaml')
$ python convert_hf_to_gguf.py  --outtype f16 /data/models/meta-llama//Meta-Llama-3.1-8B-Instruct --outfile models/Meta-Llama-3.1-8B-Instruct-F16.gguf
```

# Running llama.cpp

```
$ chmod +x llama.sh
$ conda activate neutorch # (optional)
$ ./llama.sh -m ../models/Meta-Llama-3.1-8B-Instruct-F16.gguf --neutorch-cache-path ./cache/Meta-Llama-3.1-8B-Instruct -c 4096 -n 256 -ub 256 -p "There's a llama in my garden, What should I do? "
```

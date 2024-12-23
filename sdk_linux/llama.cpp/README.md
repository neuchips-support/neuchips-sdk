# Llama.cpp tool for Viper

This is the initial llama.cpp support for Viper, for using this tool you have to install pytorch 2.4.0 or above.

# Converting models from HuggingFace

The supporting models are listed in
[README.md](https://github.com/neuchips-support/neuchips-sdk/tree/main/neutorch#readme),
by using
[convert_hf_to_gguf.py](https://github.com/ggerganov/llama.cpp/blob/master/convert_hf_to_gguf.py)
you can convert those models to gguf format.

Ex: 
```
python convert_hf_to_gguf.py  --outtype f16 /data/models/meta-llama//Meta-Llama-3.1-8B-Instruct --outfile models/Meta-Llama-3.1-8B-Instruct-F16.gguf
```

# Running llama.cpp

```
$ chmod +x llama.sh
$ conda activate neutorch # (optional)
$ ./llama.sh -m ../models/Meta-Llama-3.1-8B-Instruct-F16.gguf --neutorch-cache-path ./cache/Meta-Llama-3.1-8B-Instruct -c 4096 -n 256 -ub 256 -p "There's a llama in my garden, What should I do? "
```

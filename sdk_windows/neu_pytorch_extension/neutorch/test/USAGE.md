How to use the sample code
==========================

This script demonstrates how to perform LLM inference on a workstation using Neutorch. Users are required to download the original model from HuggingFace as noted in [README.md](https://github.com/neuchips-support/neuchips-sdk/blob/main/neutorch/README.md). Additionally, you can download pre-compiled model data from [Neuchips' page on HuggingFace](https://huggingface.co/neuchips) to accelerate script execution.

Once you have confirmed that you have the language model and precompiled data, please follow the steps below to conduct the testing.

1. Activate conda environment, you will see “(neutorch)” string before command line “$” string.
```
$ source ~/anaconda3/etc/profile.d/conda.sh
$ conda activate neutorch
(neutorch) $
```

2. Run sample script
```
(neutorch) $ python3 test_neutorch_for_release.py --test_model=models/meta-llama/Llama-2-7b-hf --compiled_model_path=precompiled_model/Llama-2-7b-hf
```

Note:
a. When the command is executed, a folder named `Llama-2-7b-hf` will be created under the precompiled_model directory, containing the precompiled data for Llama-2-7b-hf, which can speed up the inference process.
b. The test_model must match the model in the compiled_model_path.
c. The models and precompiled data in the command can be adjusted based on their actual storage locations.

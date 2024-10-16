from huggingface_hub import snapshot_download
from pathlib import Path

import argparse
import os

# def model_path2name(name):
#     temp = name.replace("/", "-")
#     return temp

def model_path2name(path):
    target_idx = 0
    for i in range(len(path)):
        if path[i] == "/":
            target_idx = i
    
    return path[target_idx+1:]

def model_download(access_token, model_name, model_zoo_path, compiled_data_path, org_weight_only):

     # check model zoo dir existence
    if not os.path.exists(model_zoo_path):
        os.makedirs(model_zoo_path)


    model_path = model_zoo_path +  model_path2name(model_name)
    compiled_path = compiled_data_path +  model_path2name(model_name)
    print("model_path: ", model_path)

    # download Original HF model 

    if access_token!=None:
        snapshot_download(repo_id=model_name,
                            local_dir=model_path, 
                            token=access_token)
    else:
        snapshot_download(repo_id=model_name,
                            local_dir=model_path)


    # check specific model compiled data dir existence
    if not os.path.exists(compiled_data_path+model_path2name(model_name)) and not org_weight_only:

        # check compiled data root dir existence
        if not os.path.exists(compiled_data_path):
            os.makedirs(compiled_data_path)

        
        # download Neutorch precomiled data from HF
        print("neuchips/"+model_path2name(model_name))
        snapshot_download(repo_id="neuchips/"+model_path2name(model_name),
                            local_dir=compiled_data_path+model_path2name(model_name), 
                            token=access_token)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--hf_access_token", default=None)
    parser.add_argument("--model_name", default="microsoft/Phi-3-mini-4k-instruct")
    parser.add_argument("--org_weight_only", action="store_true")
    parser.add_argument("--model_zoo_path", default="./model_zoo/")
    parser.add_argument("--compiled_data_path", default="./compiled_data/")


    args = parser.parse_args()


    model_download(args.hf_access_token, args.model_name, args.model_zoo_path, args.compiled_data_path, args.org_weight_only)

from pathlib import Path
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, TextStreamer
from tqdm import tqdm
from threading import Thread

import os
import csv
import torch
import neutorch
import argparse
import time 
from cpuinfo import get_cpu_info

root_path = "./prompts/"


# '''
def model_path2name(path):
    target_idx = 0
    for i in range(len(path)):
        if path[i] == "/":
            target_idx = i
    
    return path[target_idx+1:]


def Convert(string):
    li = [int(i) for i in string.split("-")]#list(string.split("-"))

    return li

def prompt_gen(test_model , prompt_len_list, target_file):
    
    tokenizer = AutoTokenizer.from_pretrained(test_model)
    print("Prompt Length List: ", prompt_len_list)
    prompt_dir = "./gen_prompts/"

    # loading tokenizer
    tokenizer = AutoTokenizer.from_pretrained(test_model)

    # check prompts dir existence
    if not os.path.exists(prompt_dir):
        os.makedirs(prompt_dir)


    # Prompt files generation 
    for length in tqdm(prompt_len_list):

        system_prompt = "please extend the following story as much as possible: \n"
        txt = system_prompt + target_file #Path(target_file).read_text()
        inputs = tokenizer.encode(txt, max_length=length, truncation=True)
        raw_text = tokenizer.decode(inputs)
        print(len(tokenizer.encode(raw_text, max_length=length, truncation=True)))
        
        print()
        model_name = model_path2name(test_model)
        print('processed model name', model_name)
        with open(prompt_dir+model_name+"_"+str(length)+".txt", "w+") as file:
            file.write(raw_text)


def model_preparation(test_model, compiled_data, neutorch_max_batch):
    '''
    llama-3-8B: "/home/user/llm_weight/8b_instruct_hf"
    phi2: "microsoft/phi-2"
    mistral-7b-v02: /home/user/llm_weight/mistral/7B/
    mistral-nemo-12B: mistralai/Mistral-Nemo-Instruct-2407
    '''
    access_token = ""
    # test_model = "/home/user/llm_weight/mistral/7B/"
    
    config = AutoConfig.from_pretrained(test_model,
                                                 token=access_token)
    tokenizer = AutoTokenizer.from_pretrained(test_model,
                                                 token=access_token)
    # streamer = TextIteratorStreamer(tokenizer)
    print("loading tokenizer successfully~")

    # cpu arch detection
    cpu_data = get_cpu_info()
    attn_option = "sdpa"
    model_dtype = torch.bfloat16

    # print(cpu_data['brand_raw'])
    # print(cpu_data['flags'])

    if "AMD" in cpu_data['brand_raw']:
        attn_option = "eager"
    else:
        attn_option = "sdpa"
    
    if "avx512_bf16" in cpu_data['flags']:
        model_dtype = torch.bfloat16
    else:
        model_dtype = torch.float32


    print("attn_implementation: ", attn_option)

    model = AutoModelForCausalLM.from_pretrained(test_model, 
                                                 torch_dtype=model_dtype, 
                                                 low_cpu_mem_usage=True,
                                                 attn_implementation=attn_option,
                                                 token=access_token
                                                 )
    print("loading LLM successfully~")

    print(config)
    ''' neutorch import '''
    # Specified your devices
    device_ids = neutorch._C.get_available_devices()
    #print(device_ids[0])
    print("device_ids")
    print(device_ids)
    neutorch._C.set_device(
        [device_ids[0]], use_matrix=True
    )  # single card

    # check neutorch_compiled_data existence
    neutorch_data_path = "./compiled_data/"
    if  not os.path.exists(neutorch_data_path):
        os.mkdir(neutorch_data_path)

    
    compiled_data = neutorch_data_path + model_path2name(test_model)

    print("precomiled data : ", compiled_data)
    
    neutorch_compilation_start = time.time()
    neutorch_model = model
    neutorch_model= neutorch.optimize(
       model,
      inplace=True,
       config_dir=compiled_data,
    )
    print("neutorch model: ", neutorch_model)
    print("neutorch compilation time: %4.2f" %(time.time() - neutorch_compilation_start))


    # print("hidden size: ", config.hidden_size)
    # print("context length: ", config.max_position_embeddings)

    hidden_size = config.hidden_size
    context_length = config.max_position_embeddings

    return tokenizer, neutorch_model, config.hidden_size, config.max_position_embeddings


    


def model_inference(tokenizer, 
                    neutorch_model, 
                    hidden_size, 
                    context_length, 
                    neutorch_max_batch, 
                    test_model_path, 
                    prompt_len_list, 
                    gen_len_list):

    benchmark_dir = "./benchmark_result/"
    # check benchmark result dir existence
    if not os.path.exists(benchmark_dir):
        os.makedirs(benchmark_dir)


    benchmark_record_file = benchmark_dir+model_path2name(test_model_path)+ "_benchmark_result.csv"
    decode_kwargs = dict(do_sample=False,
                            top_k=10,
                            num_return_sequences=1,
                            eos_token_id=tokenizer.eos_token_id)
    streamer = TextStreamer(tokenizer, decode_kwargs=decode_kwargs)
    
    with open(benchmark_record_file, 'a', newline='') as csvfile:
      # 建立 CSV 檔寫入器
      writer = csv.writer(csvfile)
      writer.writerow(['Model Name', "Prompt Length", "Gen Length", "Total Time", "Output TPS", "Prompt TPS", "Gen. TPS"])
    
    
    for i in tqdm(prompt_len_list):

        ttft = 0
        for g in tqdm(gen_len_list):

            print("input length: " + str(i)+", output length: "+ str(g))
            if i+g > context_length:
                print("exceed the context length("+str(context_length)+")"+": ", i+g)
                continue
            else:
                #    with open(prompt_dir+model_name+"_"+str(length)+".txt", "w+") as file:
             
                text = Path('./gen_prompts/'+model_path2name(test_model_path)+"_"+str(i)+'.txt').read_text()
                # final_prompt = content
                # text= final_prompt

                if text =="":
                    break
                else:
                    inputs = tokenizer([text], return_tensors="pt", max_length=i)
                    print("inputs size: ", inputs["input_ids"].size())

                    
                    start_time = time.time()
                    generation_output = neutorch_model.generate(**inputs,
                                                    min_new_tokens=g,
                                                    max_new_tokens=g,
                                                    max_length=i+g,
                                                    streamer=streamer)
                    
                    total_time = time.time()-start_time

                    if g == 1:
                        ttft = total_time
                        # print(ttft)

                        with open(benchmark_record_file, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            # writer.writerow(['Model Name', "Prompt Length", "Gen Length", "Output TPS"])
                            writer.writerow([test_model_path, inputs['input_ids'].size()[1], g, total_time, g/total_time, inputs['input_ids'].size()[1]/ttft, (g-1)/(ttft)])
                            print(" %s |input length: %d | gen length: %d | Total Time: %4.2f | Output TPS %4.2f | Prompt TPS %4.2f | Gen. TPS %4.2f" %(test_model_path, inputs['input_ids'].size()[1], g, total_time, g/total_time, inputs['input_ids'].size()[1]/ttft, 0))

                    else:
                        print(ttft)
                        with open(benchmark_record_file, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            # writer.writerow(['Model Name', "Prompt Length", "Gen Length", "Output TPS"])
                            writer.writerow([test_model_path, inputs['input_ids'].size()[1], g, total_time, g/total_time, inputs['input_ids'].size()[1]/ttft, g/(total_time - ttft)])
                            print(" %s | input length: %d | gen length: %d | Total Time: %4.2f | Output TPS %4.2f | Prompt TPS %4.2f | Gen. TPS %4.2f" %(test_model_path, inputs['input_ids'].size()[1], g, total_time, g/total_time, inputs['input_ids'].size()[1]/ttft, (g-1)/(total_time - ttft)))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--model_zoo_path", default="./model_zoo/")
    parser.add_argument("--target_model", default=None)
    parser.add_argument("--compiled_data", default="./data")
    parser.add_argument("--prompt_gen", action='store_true')
    parser.add_argument("--benchmark", action='store_true')
    parser.add_argument("--streaming", action='store_true')
    parser.add_argument("--burn_in", action="store_true")
    parser.add_argument("--prompt_file", default="./OZ_story_example.txt")
    parser.add_argument("--device_id", default=0, type=int)
    parser.add_argument("--prompt_list", default="128-256-512-1024-2048")
    parser.add_argument("--gen_list", default="1-128-256-512-1024-2048")
    parser.add_argument("--neutorch_max_batch", default=128, type=int)

    
    args = parser.parse_args()



    prompt_list = Convert(args.prompt_list)
    print("prompt config: ", prompt_list)
    gen_list = Convert(args.gen_list)
    print("gen config: ", gen_list)
    root_path = args.model_zoo_path

    if args.prompt_gen:
        print('prompt gen')
        target_file = Path(args.prompt_file).read_text()

        if args.target_model!=None:
            print("target model")
            prompt_gen(args.target_model, prompt_list, target_file)
        
        else:
            # print()
            # for i in tqdm(os.walk(root_path)):
            model_list = next(os.walk(root_path))
                # print("sdjfldsfj")
            for i in tqdm(model_list[1]):
                print(i)
                prompt_gen(args.model_zoo_path+i, prompt_list, target_file)

    if args.benchmark:

        if args.target_model!=None:
            tokenizer, neutorch_model, hidden_size, context_length = model_preparation(args.target_model, 
                                                                                       args.compiled_data, 
                                                                                       args.neutorch_max_batch)
            model_inference(tokenizer, 
                            neutorch_model, 
                            hidden_size, 
                            context_length, 
                            args.neutorch_max_batch, 
                            args.target_model,
                            prompt_list,
                            gen_list)

            neutorch._C.release_device()
            
        else:
            model_list = next(os.walk(root_path))
                # print("sdjfldsfj")
            for i in tqdm(model_list[1]):
                print(i)

                tokenizer, neutorch_model, hidden_size, context_length = model_preparation(args.model_zoo_path+i, 
                                                                                           args.compiled_data, 
                                                                                           args.neutorch_max_batch)
                model_inference(tokenizer, 
                                neutorch_model, 
                                hidden_size, 
                                context_length, 
                                args.neutorch_max_batch, 
                                args.model_zoo_path+i,
                                prompt_list,
                                gen_list)
                
                neutorch._C.release_device()


    






    

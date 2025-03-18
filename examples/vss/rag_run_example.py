import argparse
import neutorch
import neuvss as vss
import numpy as np
import os
import torch

from sentence_transformers import SentenceTransformer
from transformers import (
    AutoTokenizer,
    LlamaForCausalLM,
    LlamaTokenizer,
    logging,
    TextStreamer)

RAW_TEXT_CACHE_FILE = "raw_text.pt"
CORPUS_EMB_CACHE_FILE = "corpus_emb.pt"
TOP_K = 4
INPUT_SCALE = 0.0374
WEIGHT_SCALE = 0.0374
OUTPUT_SCALE = 2.6562
# use model Meta-Llama-3.1-8B-Instruct and corresponding template
LLM_PROMPT_TEMPLATE = (
    "<|begin_of_text|>\n"
    "<|start_header_id|>system<|end_header_id|>\n"
    "[system_setting]<|eot_id|>\n\n"
    "<|start_header_id|>user<|end_header_id|>\n"
    "[user_prompt_setting]<|eot_id|>\n\n"
    "<|start_header_id|>assistant<|end_header_id|>\n"
    "<|end_of_text|>\n")
LLM_EOS_TOKEN = "<|eot_id|>"

vss_calc = None
llm_tokenizer = None
llm_model = None

class NoEosTextStreamer(TextStreamer):
    def on_finalized_text(self, text: str, stream_end: bool = False):
        if not text.strip().endswith(self.tokenizer.eos_token):
            super().on_finalized_text(text, stream_end=stream_end)
        else:
            super().on_finalized_text(text[:-len(self.tokenizer.eos_token)], stream_end=stream_end)

def load_db_from_cache(db_cache_dir):
    raw_text_path = os.path.join(db_cache_dir, RAW_TEXT_CACHE_FILE)
    if not os.path.exists(raw_text_path):
        raise RuntimeError(f"Can not find cache file {raw_text_path}.")
    corpus_emb_path = os.path.join(db_cache_dir, CORPUS_EMB_CACHE_FILE)
    if not os.path.exists(corpus_emb_path):
        raise RuntimeError(f"Can not find cache file {corpus_emb_path}.")

    raw_text = torch.load(raw_text_path, map_location=torch.device("cpu"), weights_only=True)
    corpus_emb = torch.load(corpus_emb_path, map_location=torch.device("cpu"), weights_only=True)

    return raw_text, corpus_emb

def get_q_scale():
    in_scale = torch.tensor(INPUT_SCALE, dtype=torch.bfloat16)
    w_scale = torch.tensor(WEIGHT_SCALE, dtype=torch.bfloat16)
    out_scale = torch.tensor(OUTPUT_SCALE, dtype=torch.bfloat16)

    return (in_scale * w_scale / out_scale).item()

def to_vss_input(prompt):
    emb_model = SentenceTransformer("WhereIsAI/UAE-Large-V1")
    encoded_prompt = emb_model.encode(prompt, convert_to_tensor=True)
    quanted_prompt = torch.clamp(torch.round(encoded_prompt / INPUT_SCALE), -127, 127).to(torch.int8)

    return quanted_prompt.view(-1, 16).flip(1).flatten().numpy()

def init_vss(device_id, input_dim, weight_dir):
    global vss_calc
    if vss_calc is not None:
        raise RuntimeError("Failed to initialize VSS calculator. It is already initizlied.")

    device_list = vss.PyNeuVssCalculator.get_available_device()
    if device_id not in device_list:
        raise RuntimeError(f"The test device {device_id} is not available.")

    vss_calc = vss.PyNeuVssCalculator()
    if not vss_calc.bind_device(device_id):
        vss_calc = None
        raise RuntimeError(f"Failed to bind device {device_id}.")
    if not vss_calc.initialize(input_dim, weight_dir, get_q_scale()):
        vss_calc = None
        raise RuntimeError(f"Failed to initialize VSS.")

    print("Create VSS calculator OK.")

def run_vss(raw_text, prompt, output_dim):
    output_buffer_size = (output_dim + 3) // 4 * 4 # align to 4 bytes
    input_data = to_vss_input(prompt)
    output_buffer = np.zeros((output_buffer_size,), dtype=np.int8)

    if not vss_calc.run(input_data, output_buffer):
        raise RuntimeError(f"Failed to run VSS.")

    output_buffer = output_buffer[:output_dim]
    db_values, db_indices = torch.topk(torch.from_numpy(output_buffer), TOP_K, dim=0)
    content = ""
    for i in range(len(db_indices)):
        content += raw_text[db_indices[i]] + "\n"

    return content

def convert_single_quote(text):
    return text.replace("'", "'\\''")

def generate_sys_prompt():
    system_prompt = (
        "You are a helpful AI assistant, aiming to keep your answers in brief."
        "Use the following context to answer the user's question. If you don't know the answer, "
        "just say that you don't know, don't try to make up an answer.")

    return convert_single_quote(system_prompt)

def format_prompt(prompt, vss_content):
    user_prompt = (
        "Context: " + vss_content + "\n"
        "Question: " + prompt + " Only return the helpful answer below and nothing else.\n"
        "Answer: ")

    return convert_single_quote(user_prompt)

def apply_template(system_prompt, user_prompt):
    data = {
        "[system_setting]": system_prompt,
        "[user_prompt_setting]": user_prompt}
    applied_prompt = LLM_PROMPT_TEMPLATE
    for placeholder, value in data.items():
        if placeholder in applied_prompt:
            applied_prompt = applied_prompt.replace(placeholder, value)

    return applied_prompt

def decorate_prompt(prompt, vss_content):
    system_prompt = generate_sys_prompt()
    formated_prompt = format_prompt(prompt, vss_content)
    templated_prompt = apply_template(system_prompt, formated_prompt)

    return templated_prompt

def init_llm(device_id, model_dir, model_cache_dir):
    global llm_tokenizer
    global llm_model
    if llm_model is not None:
        raise RuntimeError("Failed to initialize LLM. It is already initialized.")

    device_list = neutorch._C.get_available_devices()
    if device_id not in device_list:
        raise RuntimeError(f"The test device {device_id} is not available.")
    neutorch._C.set_device([ device_id ], use_emb=True, use_matrix=True)

    llm_tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = LlamaForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
    llm_model = neutorch.optimize(model, usage_pattern="long", inplace=True, config_dir=model_cache_dir)

    print("Create LLM model and tokenizer OK.")

def run_llm(decode_kwargs, prompt):
    streamer = NoEosTextStreamer(tokenizer=llm_tokenizer, skip_prompt=True, decode_kwargs=decode_kwargs)
    dv_prompt = llm_tokenizer(prompt, return_tensors="pt")
    generation_kwargs = dict(
        **dv_prompt,
        do_sample=False,
        top_p=1.0,
        temperature=1.0,
        max_new_tokens=512,
        num_return_sequences=1,
        streamer=streamer)

    try:
        output = llm_model.generate(**generation_kwargs)
        return llm_tokenizer.decode(output[0, dv_prompt["input_ids"].shape[1]:], skip_special_tokens=True)
    except Exception as e:
        print(f"LLM generation error: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(description="An example for running RAG with model Meta-Llama-3.1-8B-Instruct.")
    parser.add_argument("--device", type=str, required=True, help="The target device to run. ex. neuchips_ai_epr-0")
    parser.add_argument("--vss_db_cache_dir", type=str, required=True,
        help="The directory of VSS DB cache. It is the output of VSS conver db.")
    parser.add_argument("--vss_weight_dir", type=str, required=True,
        help="The directory of VSS weights. It is the output of VSS conver db.")
    parser.add_argument("--llm_model_dir", type=str, required=True,
        help="The directory of LLM model. It is downloaded from Hugging Face.")
    parser.add_argument("--llm_model_cache_dir", type=str, required=True,
        help=("The directory of LLM model cache. If the cache exists, the program will use the cache directly. "
              "If the cache does not exist, the program will generate the cache from LLM model that is "
              "in llm_model_dir, and then use the cache."))
    parser.add_argument("--prompt", type=str, default="",
        help=("Optional. The input prompt. If the prompt is provided, the program will feed the prompt and show "
              "the response automatically. If it is not provided, the program will wait and notify user to enter "
              "the prompt, and then show the response recursively."))
    args = parser.parse_args()

    logging.set_verbosity_error()# prevent too many hugging face verbose logs

    # initialize
    raw_text, corpus_emb = load_db_from_cache(args.vss_db_cache_dir)
    vss_input_dim = corpus_emb.shape[1]
    vss_output_dim = corpus_emb.shape[0]
    init_vss(args.device, vss_input_dim, args.vss_weight_dir)

    init_llm(args.device, args.llm_model_dir, args.llm_model_cache_dir)

    # run
    decode_kwargs = dict(
        eos_token_id=[ llm_tokenizer.eos_token_id, llm_tokenizer.convert_tokens_to_ids(LLM_EOS_TOKEN) ],
        skip_special_tokens=False,
        return_full_text=False)
    if args.prompt != "":
        print(f"Prompt: {args.prompt}")
        vss_content = run_vss(raw_text, args.prompt, vss_output_dim)
        llm_prompt = decorate_prompt(args.prompt, vss_content)
        run_llm(decode_kwargs, llm_prompt)
    else:
        while True:
            user_prompt = input("Enter the prompt to run or empty to quit: ")
            if user_prompt == "":
                break
            vss_content = run_vss(raw_text, user_prompt, vss_output_dim)
            llm_prompt = decorate_prompt(user_prompt, vss_content)
            run_llm(decode_kwargs, llm_prompt)

if __name__ == '__main__':
    main()

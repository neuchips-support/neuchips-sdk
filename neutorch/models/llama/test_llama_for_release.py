#!/usr/bin/env python3
#
# NEUCHIPS CONFIDENTIAL
#
# Copyright (C) 2018-2022 NEUCHIPS Corp.
# All Rights Reserved.
# Author: Alan Kao <alan.kao@neuchips.ai>
#
# The information and source code contained herein is the exclusive property
# of NEUCHIPS CORPORATION and may not be disclosed, examined or reproduced
# in whole or in part without explicit written authorization from the company.
#

import argparse
import datetime
import torch
import os
import time
import neutorch

from transformers import LlamaForCausalLM, LlamaModel, LlamaConfig, LlamaTokenizer, pipeline
from neutorch.conversion.linear import neu_linear

class LlamaTestbed:

    def __init__(self):
        pass

    def run(self, test_model, prompt, max_tokens, verify_mode, verify_answer):
        print("[Run Testbed] run - ", datetime.datetime.now())
        answer = self.__test_model_logits(test_model, prompt, max_tokens, verify_mode)
        if verify_mode:
            assert(answer == verify_answer)
        print("[Run Testbed] end - ", datetime.datetime.now())

    def __inference(self, p, tokenizer, prompt, max_tokens):
        start_time = time.time()
        sequences = p(prompt,
                      do_sample=False,
                      top_k=10,
                      num_return_sequences=1,
                      eos_token_id=tokenizer.eos_token_id,
                      max_length=max_tokens)
        end_time = time.time()
        cpu_time = round(end_time - start_time, 2)

        answer = sequences[0]['generated_text']
        tokens = len(tokenizer.tokenize(answer))
        #print("len of tokenizer tokenize:", tokens, "\n") # here is the tokenized length
        print("\n[", cpu_time, "s]", "[", round(tokens/cpu_time, 2), "tokens/s]")
        print(answer)
        return answer

    def __test_model_logits(self, test_model, prompt, max_tokens, verify_mode):
        m = LlamaForCausalLM.from_pretrained(test_model, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)

        number_of_words = len(prompt.split())
        tokenizer = LlamaTokenizer.from_pretrained(test_model)
        #print("len of tokenizer tokenize:", len(tokenizer.tokenize(prompt))) # here is the tokenized length

        # Specified your devices
        device_ids = neutorch._C.get_available_devices()
        print(device_ids)
        neutorch._C.set_device(device_ids[:1]) # single card

        compiled_model_path = os.path.join(os.getcwd(), 'data') if os.path.exists(os.path.join(os.getcwd(), 'data')) else ''
        print("Specified load model from", compiled_model_path)
        m = neutorch.optimize(m, inplace=True, config_dir=compiled_model_path)
        p = pipeline("text-generation", model=m, torch_dtype=torch.bfloat16, device_map="auto", tokenizer=tokenizer)

        print("\n\nInference ************************************************")
        answer = self.__inference(p, tokenizer, prompt, max_tokens)
        if verify_mode:
            return answer

        while True:
            prompt = input("Enter your prompt string (or 'exit' to stop): ")
            if not prompt:
                print("You didn't enter anything. Please try again.")
                continue  # Continue the loop to prompt for input again
            elif prompt.lower() == 'exit':
                break  # Exit the loop if the user enters 'exit'

            max_tokens_str = input("Enter your max tokens number (or 'exit' to stop): ")
            if not max_tokens_str:
                print("You didn't enter anything. Use privious max tokens number ", max_tokens)
            elif max_tokens_str.lower() == 'exit':
                break  # Exit the loop if the user enters 'exit'
            else:
                try:
                    max_tokens = int(max_tokens_str)
                except ValueError:
                    print("You didn't enter anything. Use privious max tokens number ", max_tokens)

            answer = self.__inference(p, tokenizer, prompt, max_tokens)

        return answer

class ArgParser():

    def __init__(self):
        self.default_test_model = "/data/models/meta-llama/Llama-2-7b-chat-hf"
        self.default_prompt = "Once upon a time, there existed a little girl who liked to have adventures. She wanted to go to places and meet new people, and have fun"
        self.default_max_tokens = 50
        self.default_verify_mode = False
        self.default_verify_answer = "Once upon a time, there existed a little girl who liked to have adventures. She wanted to go to places and meet new people, and have fun. But her parents were always telling her to stay at home and be careful. They were wor"

    def get_user_parameters(self):
        arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        arg_parser.add_argument('--test_model', type=str, help=f'Test model (default is \'{self.default_test_model}\')', default=self.default_test_model)
        arg_parser.add_argument('--prompt', type=str, help=f'Prompt string (default is \'{self.default_prompt}\')', default=self.default_prompt)
        arg_parser.add_argument('--max_tokens', type=int,  help=f'Max tokens number (default is {self.default_max_tokens})', default=self.default_max_tokens)
        arg_parser.add_argument('--verify_mode', type=bool,  help=f'Verify mode only for debug (default is {self.default_verify_mode})', default=self.default_verify_mode)
        arg_parser.add_argument('--verify_answer', type=str,  help=f'Verify answer when verify mode is true (default is {self.default_verify_answer})', default=self.default_verify_answer)

        args = arg_parser.parse_args()
        test_model = args.test_model
        prompt = args.prompt
        max_tokens = args.max_tokens
        verify_mode = args.verify_mode
        verify_answer = args.verify_answer

        print("test_model :", test_model)
        print("prompt :", prompt)
        print("max_tokens :", max_tokens)
        if verify_mode:
            print("verify_mode :", verify_mode)
            print("verify_answer :", verify_answer)
        print("")

        return [test_model, prompt, max_tokens, verify_mode, verify_answer]

def main():
    arg_parser = ArgParser()
    [test_model, prompt,  max_tokens, verify_mode, verify_answer] = arg_parser.get_user_parameters()

    testbed = LlamaTestbed()
    testbed.run(test_model, prompt, max_tokens, verify_mode, verify_answer)

if __name__ == '__main__':
    main()




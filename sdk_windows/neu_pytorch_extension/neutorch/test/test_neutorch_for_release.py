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
import zipfile
import neutorch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaForCausalLM,
    LlamaTokenizer,
    MistralForCausalLM,
    pipeline,
)

from neutorch.conversion.linear import neu_linear
from path_utils import get_model_path


class LLMTestbed:

    def __init__(self):
        pass

    def load_model_and_tokenizer(self, model_path: str):
        model_path_lower = model_path.lower()
        model_class, tokenizer_class = AutoModelForCausalLM, AutoTokenizer

        # For microsoft model, use trust_remote_code and torch_dtype="auto"
        if any(
            keyword in model_path_lower
            for keyword in ["phi2", "phi-3-mini-4k-instruct"]
        ):
            model = model_class.from_pretrained(
                model_path,
                torch_dtype="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True,
                attn_implementation="eager",
            ).to(torch.bfloat16)
            tokenizer = tokenizer_class.from_pretrained(
                model_path, trust_remote_code=True
            )
        else:
            model = model_class.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                attn_implementation="eager",
            )
            tokenizer = tokenizer_class.from_pretrained(model_path)

        return model, tokenizer

    def handle_model_path(self, compiled_model_path: str):
        if not compiled_model_path:
            return None

        absolute_path = os.path.abspath(compiled_model_path)

        if os.path.exists(absolute_path):
            # If the compiled model path is a zip file, unzip the file.
            if absolute_path.endswith(".zip"):
                extract_dir = os.path.join(
                    os.path.dirname(absolute_path),
                    os.path.splitext(os.path.basename(absolute_path))[0],
                )

                if not os.path.exists(extract_dir):
                    with zipfile.ZipFile(absolute_path, "r") as zip_ref:
                        zip_ref.extractall(extract_dir)
                        print(f"Unzip compiled model to: {extract_dir}")
                else:
                    print(
                        f"The {extract_dir} exists. If the compiled model cannot be loaded, please remove the folder and run or unzip it again."
                    )

                return extract_dir
            else:
                return absolute_path
        else:
            return None

    def run(
        self,
        test_model,
        compiled_model_path,
        use_matrix,
        usage_pattern,
        prompt,
        max_tokens,
        verify_mode,
        verify_answer,
    ):
        print("[Run Testbed] run - ", datetime.datetime.now())
        answer = self.__test_model_logits(
            test_model,
            compiled_model_path,
            use_matrix,
            usage_pattern,
            prompt,
            max_tokens,
            verify_mode,
        )
        if verify_mode:
            assert answer == verify_answer
        print("[Run Testbed] end - ", datetime.datetime.now())

    def __inference(self, p, tokenizer, prompt, max_tokens):
        start_time = time.time()
        sequences = p(
            prompt,
            do_sample=False,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            max_length=max_tokens,
        )
        end_time = time.time()
        cpu_time = round(end_time - start_time, 2)

        answer = sequences[0]["generated_text"]
        tokens = len(tokenizer.tokenize(answer))
        # print("len of tokenizer tokenize:", tokens, "\n") # here is the tokenized length
        print("\n[", cpu_time, "s]", "[", round(tokens / cpu_time, 2), "tokens/s]")
        print(answer)
        return answer

    def __test_model_logits(
        self,
        test_model,
        compiled_model_path,
        use_matrix,
        usage_pattern,
        prompt,
        max_tokens,
        verify_mode,
    ):
        m, tokenizer = self.load_model_and_tokenizer(test_model)

        number_of_words = len(prompt.split())
        # print("len of tokenizer tokenize:", len(tokenizer.tokenize(prompt))) # here is the tokenized length

        # Specified your devices
        device_ids = neutorch._C.get_available_devices()
        print(device_ids)
        neutorch._C.set_device(device_ids[:1], use_matrix=use_matrix)  # single card

        compiled_model_path_ = self.handle_model_path(compiled_model_path)
        print("Specified load model from", compiled_model_path_)
        m = neutorch.optimize(
            m,
            usage_pattern=usage_pattern,
            inplace=True,
            config_dir=compiled_model_path_,
        )
        p = pipeline(
            "text-generation",
            model=m,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            tokenizer=tokenizer,
        )

        print("\n\nInference ************************************************")
        answer = self.__inference(p, tokenizer, prompt, max_tokens)
        if verify_mode:
            return answer

        while True:
            prompt = input("Enter your prompt string (or 'exit' to stop): ")
            if not prompt:
                print("You didn't enter anything. Please try again.")
                continue  # Continue the loop to prompt for input again
            elif prompt.lower() == "exit":
                break  # Exit the loop if the user enters 'exit'

            max_tokens_str = input("Enter your max tokens number (or 'exit' to stop): ")
            if not max_tokens_str:
                print(
                    "You didn't enter anything. Use previous max tokens number ",
                    max_tokens,
                )
            elif max_tokens_str.lower() == "exit":
                break  # Exit the loop if the user enters 'exit'
            else:
                try:
                    max_tokens = int(max_tokens_str)
                except ValueError:
                    print(
                        "You didn't enter anything. Use previous max tokens number ",
                        max_tokens,
                    )

            answer = self.__inference(p, tokenizer, prompt, max_tokens)

        return answer


class ArgParser:

    def __init__(self):
        self.default_test_model = get_model_path("meta-llama/Llama-2-7b-hf")
        # self.default_test_model = get_model_path("meta-llama/Llama-2-13b-chat-hf")
        self.default_compiled_model_path = None
        self.default_use_matrix = True
        self.default_usage_pattern = "general"
        self.default_prompt = "Once upon a time, there existed a little girl who liked to have adventures. She wanted to go to places and meet new people, and have fun"
        self.default_max_tokens = 50
        self.default_verify_mode = False
        self.default_verify_answer = "Once upon a time, there existed a little girl who liked to have adventures. She wanted to go to places and meet new people, and have fun. She wanted to be a part of something bigger than herself. She wanted to be a"

    def get_user_parameters(self):
        arg_parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter
        )
        arg_parser.add_argument(
            "--test_model",
            type=str,
            help=f"Test model (default is `{self.default_test_model}`), supports the following models: Llama-2-7b-hf, Llama-3-8B, Mistral-7B, Breeze-7B, Gemma-2-9B, Phi2, and Phi-3-Mini-4K.",
            default=self.default_test_model,
        )
        arg_parser.add_argument(
            "--compiled_model_path",
            type=str,
            help=f"Path to load the precompiled model (default is empty).",
            default=self.default_compiled_model_path,
        )
        arg_parser.add_argument(
            "--use_matrix",
            type=bool,
            help=f"Model inference by Matrix engines (default is '{self.default_use_matrix}')",
            default=self.default_use_matrix,
        )
        arg_parser.add_argument(
            "--usage_pattern",
            type=str,
            help=f"Specifies the user scenario. The value can be either `general` for normal purposes (e.g., chat, QA) or `long` for scenarios like Retrieval-Augmented Generation (RAG), where the average input prompt is longer. (default is '{self.default_usage_pattern}')",
            default=self.default_usage_pattern,
        )
        arg_parser.add_argument(
            "--prompt",
            type=str,
            help=f"Prompt string (default is '{self.default_prompt}')",
            default=self.default_prompt,
        )
        arg_parser.add_argument(
            "--max_tokens",
            type=int,
            help=f"Max tokens number (default is '{self.default_max_tokens}')",
            default=self.default_max_tokens,
        )
        arg_parser.add_argument(
            "--verify_mode",
            type=bool,
            help=f"Verify mode only for debug (default is '{self.default_verify_mode}')",
            default=self.default_verify_mode,
        )
        arg_parser.add_argument(
            "--verify_answer",
            type=str,
            help=f"Verify answer when verify mode is true (default is '{self.default_verify_answer}')",
            default=self.default_verify_answer,
        )

        args = arg_parser.parse_args()
        test_model = args.test_model
        compiled_model_path = args.compiled_model_path
        use_matrix = args.use_matrix
        usage_pattern = args.usage_pattern
        prompt = args.prompt
        max_tokens = args.max_tokens
        verify_mode = args.verify_mode
        verify_answer = args.verify_answer

        print("test_model :", test_model)
        print("compiled_model_path :", compiled_model_path)
        print("use_matrix :", use_matrix)
        print("usage_pattern: ", usage_pattern)
        print("prompt :", prompt)
        print("max_tokens :", max_tokens)
        if verify_mode:
            print("verify_mode :", verify_mode)
            print("verify_answer :", verify_answer)
        print("")

        return [
            test_model,
            compiled_model_path,
            use_matrix,
            usage_pattern,
            prompt,
            max_tokens,
            verify_mode,
            verify_answer,
        ]


def main():
    arg_parser = ArgParser()
    [
        test_model,
        compiled_model_path,
        use_matrix,
        usage_pattern,
        prompt,
        max_tokens,
        verify_mode,
        verify_answer,
    ] = arg_parser.get_user_parameters()

    testbed = LLMTestbed()

    testbed.run(
        test_model,
        compiled_model_path,
        use_matrix,
        usage_pattern,
        prompt,
        max_tokens,
        verify_mode,
        verify_answer,
    )


if __name__ == "__main__":
    main()

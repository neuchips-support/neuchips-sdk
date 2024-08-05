#!/usr/bin/env python3
#
# NEUCHIPS CONFIDENTIAL
#
# Copyright (C) 2018-2022 NEUCHIPS Corp.
# All Rights Reserved.
# Author: Ethan Chen <ethan_chen@neuchips.ai>
#
# The information and source code contained herein is the exclusive property
# of NEUCHIPS CORPORATION and may not be disclosed, examined or reproduced
# in whole or in part without explicit written authorization from the company.
#

import torch
import neutorch
import os
import time
from transformers import pipeline, TextStreamer, AutoTokenizer, AutoModelForCausalLM

test_model = '/data/models/phi2'
model = AutoModelForCausalLM.from_pretrained(test_model, torch_dtype="auto", trust_remote_code=True, low_cpu_mem_usage=True).to(torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(test_model,trust_remote_code=True)
prompt = '''Alice, Bob and Charles are playing games. Alice first pick a random number from 333 to 678, Bob then pick a number starting from Alice’s number to 888, Charles then pick a number starting from 123 to Bob’s number. Alice gets one point if Alice’s number minus Charles’s number is divisible by the floor of the square root of Bob’s number, otherwise Bob gets one point. Simulate Alice’s and Bob’s points in 30 iterations. '''

# Set max_batch_size
max_batch_size = 256

# Specified your devices
device_ids = neutorch._C.get_available_devices()
print(device_ids)
neutorch._C.set_device(device_ids[:1], use_emb=True, use_matrix=True)

compiled_model_path = os.path.join(os.getcwd(), 'data') if os.path.exists(os.path.join(os.getcwd(), 'data')) else ''
print("Specified load model from", compiled_model_path)
model = neutorch.optimize(model, max_batch_size=max_batch_size, inplace=True, config_dir=compiled_model_path)

p = pipeline("text-generation", model=model, torch_dtype=torch.bfloat16, device_map="auto", tokenizer=tokenizer)
_streamer = TextStreamer(tokenizer)
sequences = p(prompt,
    do_sample=True,
    temperature=0.01,
    top_p=0.01,
    num_return_sequences=1,
    max_new_tokens=512,
    streamer=_streamer
)

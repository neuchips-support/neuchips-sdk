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
from transformers import pipeline, TextStreamer, AutoTokenizer, MistralForCausalLM

test_model = '/data/models/Mistral-7B-v0.1'
model = MistralForCausalLM.from_pretrained(test_model, low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(test_model)
prompt = "As a data scientist, can you explain the concept of regularization in machine learning?"

# Specified your devices
device_ids = neutorch._C.get_available_devices()
print(device_ids)
neutorch._C.set_device(device_ids[:1])

compiled_model_path = os.path.join(os.getcwd(), 'data') if os.path.exists(os.path.join(os.getcwd(), 'data')) else ''
print("Specified load model from", compiled_model_path)
model = neutorch.optimize(model, inplace=True, config_dir=compiled_model_path)

p = pipeline("text-generation", model=model, torch_dtype=torch.bfloat16, device_map="auto", tokenizer=tokenizer)
_streamer = TextStreamer(tokenizer)
sequences = p(prompt,
    do_sample=False,
    temperature=1.0,
    top_p=1.0,
    num_return_sequences=1,
    max_length=128,
    streamer=_streamer
)

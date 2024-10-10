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

test_model = '/data/models/Breeze-7B-Instruct-v0_1'
model = MistralForCausalLM.from_pretrained(test_model, low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(test_model)
prompt = '''You are a helpful AI assistant built by MediaTek Research. The user you are helping speaks Traditional Chinese and comes from Taiwan. [INST] 請擬定一封專業的郵件，尋求主管對你準備的「季度財務報告」提供意見。特別詢問有關資料分析、呈現風格，以及所提取結論的清晰度。郵件請簡潔扼要。[/INST]'''

# Specified your devices
device_ids = neutorch._C.get_available_devices()
print(device_ids)
neutorch._C.set_device(device_ids[:1])

compiled_model_path = os.path.join(os.getcwd(), 'data') if os.path.exists(os.path.join(os.getcwd(), 'data')) else ''
print("Specified load model from", compiled_model_path)
model = neutorch.optimize(model, usage_pattern="general", inplace=True, config_dir=compiled_model_path)

p = pipeline("text-generation", model=model, torch_dtype=torch.bfloat16, device_map="auto", tokenizer=tokenizer)
_streamer = TextStreamer(tokenizer)
sequences = p(prompt,
    do_sample=False,
    temperature=0.01,
    top_p=0.01,
    num_return_sequences=1,
    max_length=512,
    streamer=_streamer
)

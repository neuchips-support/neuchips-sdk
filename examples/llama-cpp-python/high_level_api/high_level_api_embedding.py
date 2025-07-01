import argparse

from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../models/7B/ggml-model.bin")
parser.add_argument("-ncp", "--neutorch_cache_path", type=str, default="./data")
args = parser.parse_args()

llm = Llama(model_path=args.model, embedding=True, neutorch_cache_path=args.neutorch_cache_path)

print(llm.create_embedding("Hello world!"))

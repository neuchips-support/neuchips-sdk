import json
import argparse

from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../models/7B/ggml-models.bin")
parser.add_argument("--n3k_id", "--n3k_id", type=int, default=0)
parser.add_argument("-ncp", "--neutorch_cache_path", type=str, default="./data")
args = parser.parse_args()

llm = Llama(model_path=args.model, n3k_id=args.n3k_id, neutorch_cache_path=args.neutorch_cache_path)

output = llm(
    "Question: What are the names of the planets in the solar system? Answer: ",
    max_tokens=48,
    stop=["Q:", "\n"],
    echo=True,
)

print(json.dumps(output, indent=2))

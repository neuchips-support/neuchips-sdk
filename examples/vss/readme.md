# RAG Example Usage

Here provides two examples demonstrating how to use the SDK library for RAG. Please setup the environment the same as for RAG App.

## Example: vss_convert_db_example.py

This example demonstrates how to convert a pdf file to db cache and VSS weights. **convert_db.sh** executes the py file with corresponding parameters.

### Parameters
| Name     | Description                                   |
|----------|-----------------------------------------------|
| `--pdf_file` | A pdf file that is the db source. |
| `--cache_dir` | The directory of db cache files. |
| `--weight_dir` | The directory of VSS weight files. |

## Example: rag_run_example.py

This example demonstrates how to run the RAG flow with model Meta-Llama-3.1-8B-Instruct. **run_rag.sh** executes the py file with corresponding parameters.

### Parameters
| Name     | Description                                   |
|----------|-----------------------------------------------|
| `--device` | The target device to run. ex. neuchips_ai_epr-0 |
| `--vss_db_cache_dir` | The directory of VSS DB cache. It is the output of VSS conver db. |
| `--vss_weight_dir` | The directory of VSS weights. It is the output of VSS conver db. |
| `--llm_model_dir` | The directory of LLM model. It is downloaded from Hugging Face. |
| `--llm_model_cache_dir` | The directory of LLM model cache. If the cache exists, the program will use the cache directly. If the cache does not exist, the program will generate the cache from LLM model that is in llm_model_dir, and then use the cache. |
| `--prompt` | Optional. The input prompt. If the prompt is provided, the program will feed the prompt and show the response automatically. If it is not provided, the program will wait and notify user to enter the prompt, and then show the response recursively. |

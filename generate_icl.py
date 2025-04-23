import json
import openai
from concurrent.futures import ProcessPoolExecutor, as_completed

openai.api_key = ""

# Contains correct version in the benchmark
with open("correct_codes.json", "r") as f:
    dataset = json.load(f)

# Contains incorrect code, each contains explanation on intended logic of the program
with open("0_examples_benchmark.json", "r") as f:
    dataset1 = json.load(f)
    
# Prompt that is used for prompting OpenAI to generate few-prompt (buggy/fixed pairs)
def process_batch(i):
    prompt = f"""
    You are an expert in software bug fixing and educational code generation.

    Given a buggy Java function and its fixed version, your task is to generate **three (3)** high-quality in-context learning (ICL) examples that could help a language model fix the buggy function.

    Each ICL example should contain:

    1. A code snippet (buggy) that contains a **different bug** (not the same as the main input) but is **similar in functionality or domain**. The examples should not contain the same fix presented in the fixed version. The buggy code should have a comment pointing out where the bug is.
    2. The fixed version of the buggy snippet.

    Each example should be formatted like this:

    [ICL Example 1]
    # Provide a fix for the buggy function
    # Buggy Function:
    [Java buggy function here]

    # Fixed Function:
    [Fixed Java function here]

    The targeted fixed version:
    {dataset['data'][i]['input']}

    Now generate 3 ICL examples for the following buggy Java function, the examples **must not** contain the same fix presented in the targeted fixed version:
    {dataset1['data'][i]['input']}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an expert coder."}, 
                  {"role": "user", "content": prompt}],
        temperature=1.0
    )
    generated_description = response["choices"][0]["message"]["content"]
    
    return i, {"input": i, "output": generated_description}  


data = []

# Utilizing Parallel for faster generation
with ProcessPoolExecutor(max_workers=10) as executor:  
    futures = {executor.submit(process_batch, i): i for i in dataset['data']}

    for future in as_completed(futures):
        i, result = future.result()
        data.append((i, result))

data.sort(key=lambda x: x[0])  
final_data = [item[1] for item in data]  

with open("ICL_examples_5.json", "w") as f:
    json.dump(final_data, f, indent=2)

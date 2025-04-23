import json
import openai
from concurrent.futures import ProcessPoolExecutor, as_completed

openai.api_key = "" 

# Correct code dataset
with open("correct_codes.json", "r") as f:
    dataset = json.load(f)

# Dataset contains buggy code with no additional context
with open("No_context_benchmark.json", "r") as f:
    dataset1 = json.load(f)
    
# Prompt that is used for prompting OpenAI to generate intended logic of the buggy function
def process_batch(i):
    prompt = f"""
    You are given two Java functions: one is buggy, and the other is the correct version.

    Your task is to generate a concise, high-level explanation of what the **correct function** is intended to do, based purely on its logic and structure. 
    Do not include the logic of each line in the description.

    **Important constraints**:
    - Do NOT compare the correct function with the buggy one.
    - Do NOT mention or hint at any bugs, fixes, or incorrect behavior.
    - ONLY describe the purpose, flow, and general logic of the correct code.

    Here are the two code snippets:

    [Buggy Function]
    ```java
    {dataset1["data"][i]["input"]}

    [Correct Function]
    ```java
    {dataset["data"][i]["input"]}

    Now, provide the explanation of what the correct function does. 
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert coder."}, 
                  {"role": "user", "content": prompt}],
        temperature=1.0
    )
    generated_description = response["choices"][0]["message"]["content"]
    
    return i, {"input": i, "output": generated_description} 


# Utilizing Parallel for faster generation
data = []
with ProcessPoolExecutor(max_workers=10) as executor:  
    futures = {executor.submit(process_batch, i): i for i in dataset['data']}

    for future in as_completed(futures):
        i, result = future.result()
        data.append((i, result))

data.sort(key=lambda x: x[0])  
final_data = [item[1] for item in data] 

# Save Results
with open("explanation_examples.json", "w") as f:
    json.dump(final_data, f, indent=2)

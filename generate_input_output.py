import json
import openai
from concurrent.futures import ProcessPoolExecutor, as_completed

openai.api_key = "" 

# Correct code dataset
with open("correct_codes.json", "r") as f:
    dataset1 = json.load(f)

# Prompt that is used for prompting OpenAI to generate intended logic of the buggy function
def process_batch(i):
    prompt = f"""
    You are an expert Java developer. Given the following correct Java function, generate the following:  

    **Examples**: Provide **10** distinct examples of valid inputs and their corresponding outputs. Ensure that:
    - Each example is numbered from **1 to 10**.
    - The inputs showcase different edge cases, such as normal cases, empty strings, large inputs, and special characters.
    - The outputs should be correct and reflect the expected behavior of the function.

    Here is the Java function:  
    ```java
    {dataset1["data"][i]["input"]}
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
    futures = {executor.submit(process_batch, i): i for i in dataset1['data']}

    for future in as_completed(futures):
        i, result = future.result()
        data.append((i, result))

data.sort(key=lambda x: x[0])  
final_data = [item[1] for item in data] 

# Save Results
with open("inputoutput_examples.json", "w") as f:
    json.dump(final_data, f, indent=2)

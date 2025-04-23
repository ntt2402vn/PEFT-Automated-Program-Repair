import json
import openai
from concurrent.futures import ProcessPoolExecutor, as_completed

openai.api_key = ""  

with open("dataset_30k_nontext2.json", "r") as f:
    selected_dataset = json.load(f)

# Prompt that is used for prompting OpenAI to generate additional descriptions
def process_batch(i):
    prompt = f"""Please gain inspiration from the following 3 sections of buggy and their fix code snippets to create a high-quality programming problem. 

    For each section, provide exactly two labeled parts:  
    1. **[Bug Description]** – This section must contain:
    - **Bug Context**: Provide all the necessary contextual information needed to understand the buggy code snippet.  
    - **Bug Reason**: Explain the reason for the bug in the buggy code snippet.  
    - Do **not** include the full buggy code snippet—just describe its relevant aspects.  

    2. **[Solution]** – This section must:  
    - Offer a **comprehensive and correct** explanation of how to fix the bug.  
    - Indicate which lines or logic need modification but **do not** provide the entire fixed function.  

    Follow this exact structure for all three sections.

    ---

    **[Section 1]**  
    [Bug Description]  
    - **Bug Context**: (Describe the context of `{selected_dataset[i]['buggy_function']}`)  
    - **Bug Reason**: (Explain the specific reason why `{selected_dataset[i]['buggy_function']}` contains a bug)  

    [Solution]  
    (Provide a clear explanation on how `{selected_dataset[i]['fixed_function']}` fixes the issue without including the full fixed function.)  

    ---

    **[Section 2]**  
    [Bug Description]  
    - **Bug Context**: (Describe the context of `{selected_dataset[i+1]['buggy_function']}`)  
    - **Bug Reason**: (Explain the specific reason why `{selected_dataset[i+1]['buggy_function']}` contains a bug)  

    [Solution]  
    (Provide a clear explanation on how `{selected_dataset[i+1]['fixed_function']}` fixes the issue without including the full fixed function.)  

    ---

    **[Section 3]**  
    [Bug Description]  
    - **Bug Context**: (Describe the context of `{selected_dataset[i+2]['buggy_function']}`)  
    - **Bug Reason**: (Explain the specific reason why `{selected_dataset[i+2]['buggy_function']}` contains a bug)  

    [Solution]  
    (Provide a clear explanation on how `{selected_dataset[i+2]['fixed_function']}` fixes the issue without including the full fixed function.)  
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert coder."}, 
                  {"role": "user", "content": prompt}],
        temperature=1.0
    )
    generated_description = response["choices"][0]["message"]["content"]
    
    return i, generated_description  

# Utilizing Parallel for faster generation
data = []
with ProcessPoolExecutor(max_workers=6) as executor:  
    futures = {executor.submit(process_batch, i): i for i in range(3, 29997, 3)}

    for future in as_completed(futures):
        i, result = future.result()
        data.append((i, result))

data.sort(key=lambda x: x[0])  
final_data = [item[1] for item in data]  

with open("generated_descriptions_2.json", "w") as f:
    json.dump(final_data, f, indent=2)

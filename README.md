# Parameter-Efficient Fine-Tuning for Automated Program Repair

This repository contains all necessary files and resources related to my research on parameter-efficient fine-tuning for automated program repair. Each component is documented and reproducible.

## 📚 Instruction Datasets

Instruction datasets used for training and evaluation in the study:

- **[No Context]** dataset: https://huggingface.co/datasets/zxliu/ReAPR-Automatic-Program-Repair-via-Retrieval-Augmented-Large-Language-Models
- **[Some Context]** dataset: https://huggingface.co/datasets/ntt2402vn/30k_withcomments
- **[Full Context]** dataset: https://huggingface.co/datasets/ntt2402vn/30k_withcomments_solution

## 📁 Benchmarks

This folder includes the seven benchmarks used in the study:

- **No_context_benchmark** – Used for **RQ1** and **RQ3**. Contains only buggy and fixed code without additional context.
- **Only_Explanation_benchmark** – Used for **RQ2** and **RQ3**. Includes only the intended correct logic of the buggy function, provided during inference.
- **{i}_examples_benchmark** – Used for **RQ2** and **RQ3**. Each benchmark includes valid input/output examples and explanations of the intended logic.
- **Few_Prompt_benchmark** – Used for **RQ2** and **RQ3**. Includes three buggy/fixed code pairs as few-shot prompts for inference.

## 📁 RQ_Results

Contains results corresponding to the three research questions. Each result set is organized into the following file types:

- `*_RAW.json`: Raw model outputs directly after inference. These may include noise or duplicated responses.
- `*_CLEAN.json`: Cleaned outputs after applying regex and manual inspection to remove noise.
- `*_RESULT.json`: Evaluation results based on JUnit test cases from the HumanEval-Java benchmark.

## 📄 Scripts.ipynb

A Jupyter notebook containing scripts used to:

- Clean model outputs (requires manual inspection after regex processing)
- Run JUnit test evaluations
- Compute pass@k metrics
- Perform training and inference

## 🛠️ Utility Scripts

- `generate_description_examples.py`: Generates `[Bug Description]` and `[Solution]` instructions for each buggy example in the dataset.
- `generate_icl.py`: Generates in-context learning examples with buggy/fixed code pairs (e.g., `// buggy code at line 5 → // fixed code`).
- `generate_input_output.py`: Creates valid input/output examples (e.g., `input = [2, 3, 4] → output = 4`) for model inference.

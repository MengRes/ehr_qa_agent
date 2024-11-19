## README

This repository contains the project code for the MIMIC-IV Question Answering (QA) generation task.

`discharge_summary_explore.ipynb` processes the discharge summaries and extracts those patients who havs been existed both in icu and in the hospital. The output file `icu_discharge_merged.csv` contains the icu patient information and discharge summary.

`qwen_explore.ipynb` processes the question and answer pairs and extracts the relevant information for the QA generation task with LLM models downloaded from the Hugging Face model hub.

`discharge_qa.py` processes the discharge summaries and question and answer pairs to generate the QA pairs. The output file is stored in the `outputs/discharge_summary_qa` directory.

### Generate the QA pairs from EHR tables

To generate the QA pairs from EHR tables, we need to select the relevant tables and columns.
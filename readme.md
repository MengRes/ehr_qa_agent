## README

This repository contains the project code for the MIMIC-IV Question Answering (QA) generation task.

`discharge_summary_explore.ipynb` processes the discharge summaries and extracts those patients who havs been existed both in icu and in the hospital. The output file `icu_discharge_merged.csv` contains the icu patient information and discharge summary.

`qwen_explore.ipynb` processes the question and answer pairs and extracts the relevant information for the QA generation task with LLM models downloaded from the Hugging Face model hub.

`discharge_qa.py` processes the discharge summaries and question and answer pairs to generate the QA pairs. The output file is stored in the `outputs/discharge_summary_qa` directory.

### Generate the QA pairs from EHR tables

To generate the QA pairs from EHR tables, we need to select the relevant tables and columns. 

1. `admissions.csv`: this table includes the admission information of patients. We selected `subject_id`, `hadm_id`, `admittime`, `dischtime`, `admission_type`, `admission_location`, `discharge_location`, `insurance`, `marital_status`, and `race` columns.
2. `patients.csv`: this table includes the demographic information of patients. We selected `subject_id`, `hadm_id`, `gender`, `age`, `year`, `dod`, and `dob` columns.
3. `diagnoses_icd.csv`: this table includes the diagnoses of patients. We selected `subject_id`, `hadm_id`, `icd_code`, `icd_version`, and `long_title` columns. `long_title` is the detailed description of the diagnoses.
4. `labevents.csv`: this table includes the lab results of patients. We selected `subject_id`, `hadm_id`, `itemid`,  `charttime`, `valuenum`, `valueuom` `ref_range_lower`, `ref_range_upper`, `label`, `fluid` and `category` columns. `label` is the lab test name, `valuenum` is the lab result, `valueuom` is the unit of the lab result, `ref_range_lower`, and `ref_range_upper` are the reference range of the lab result.
5. `microbiologyevents.csv`: this table includes the microbiology results of patients. We selected `subject_id`, `hadm_id`, `charttime`, `spec_type_desc`, `test_name`, and `org_name` columns. `test_name` is the name of the test, `spec_type_desc` is the type of the test, and `org_name` is the name of the organism.
6. `prescriptions.csv`: this table includes the medications prescribed to patients. We selected `subject_id`, `hadm_id`, `starttime`, `stoptime`, `drug`, `dose_val_rx`, `dose_unit_rx`, and `route` columns. `drug` is the name of the medication, `dose_val_rx` is the dose of the medication, `dose_unit_rx` is the unit of the dose, and `route` is the administration route of the medication.
7. `procedures.csv`: this table includes the procedures of patients. We selected `subject_id`, `hadm_id`, `icd_code`, `icd_version`, and `long_title` columns. `long_title` is the detailed description of the procedures.
8. `cxr_report.csv`: this table includes the chest x-ray reports of patients. We selected `subject_id`, `hadm_id`, `cxr_report_text` columns. `cxr_report_text` is the text of the chest x-ray report.
9. `icu_stays.csv`: this table includes the information of patients who stayed in the ICU. We selected `subject_id`, `hadm_id`, `stay_id`, `first_careunit`, `last_careunit`, `intime`, and `outtime` columns. `intime` and `outtime` are the start and end time of the ICU stay, `first_careunit` and `last_careunit` are the first and last care unit of the patient.
10. `chartevents.csv`: this table includes the chart events of patients. We selected `subject_id`, `hadm_id`, `charttime`, `stay_id`, `charttime`, `itemid`, `label`, `value`, and `valueuom`. `label` is the name of the chart event, `value` is the value of the chart event, and `valueuom` is the unit of the chart event.
11. `inputevents.csv`: this table includes the input events of patients. We selected `subject_id`, `hadm_id`, `starttime`, `endtime`, `itemid`, `label`, `amount`, and `amountuom`. `label` is the name of the input event, `amount` is the value of the input event, and `amountuom` is the unit of the input event.
12. `outputevents.csv`: this table includes the output events of patients. We selected `subject_id`, `hadm_id`, `stay_id`, `charttime`, `itemid`, `label`, `value`, and `valueuom`. `label` is the name of the output event, `value` is the value of the output event, and `valueuom` is the unit of the output event.
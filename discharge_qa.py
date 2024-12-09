import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import random
import json
from tqdm import tqdm
import cv2
import torch
import transformers
from transformers import BertTokenizer, BertModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from accelerate import Accelerator
import gc
os.environ["CUDA_VISIBLE_DEVICES"] = "2, 3"


ehr_data_dir = "/home/mengliang/DatasetFolder/mimiciv/2.2"
note_data_dir = "/home/mengliang/DatasetFolder/mimic-iv-note/2.2"
# load icustays.csv.gz
icu_icustays_path = os.path.join(ehr_data_dir, "icu/icustays.csv.gz")
df_icu_icustays = pd.read_csv(icu_icustays_path, index_col=False, 
                              compression="gzip")
# load discharge.csv.gz
note_discharge_path = os.path.join(note_data_dir, "note/discharge.csv.gz")
df_note_discharge = pd.read_csv(note_discharge_path, index_col=False, 
                                compression='gzip')

icu_discharge_merged = pd.merge(df_icu_icustays, df_note_discharge, on=['subject_id', 'hadm_id'])
icu_discharge_merged.head()

# control the number of samples
discharge_test = icu_discharge_merged.iloc[:100,:]

# load discharge summary question dictionary
def parse_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    mother_questions = []
    child_questions = []
    current_mother_question = None
    current_child_list = []
    is_in_blank_section = False  # mark if in blank section

    for line in lines:
        if line == "":  # blank line
            is_in_blank_section = True  # mark blank section end
        else:
            if is_in_blank_section:  # turn to child questions
                if current_mother_question is not None:
                    child_questions.append(current_child_list)
                    current_child_list = []
                current_mother_question = None  # next mother question
                is_in_blank_section = False  # reset blank section flag

            if current_mother_question is None:
                # a new mother question starts
                current_mother_question = line
                mother_questions.append(current_mother_question)
            else:
                # mother question continues
                current_child_list.append(line)

    # last mother question and child questions
    if current_mother_question is not None:
        child_questions.append(current_child_list)

    return mother_questions, child_questions

# 示例使用：
file_path = 'files/discharge_summary_questions.txt'  # 替换为你的 txt 文件路径
mother_questions, child_questions = parse_questions(file_path)

# 打印结果
print("question template list:", mother_questions)
print("question dict list", child_questions)


# load Qwen-14B-Chat model
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-14B-Chat", trust_remote_code=True)

# use bf16
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True, bf16=True).eval()
# use fp16
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True, fp16=True).eval()
# use cpu only
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="cpu", trust_remote_code=True).eval()
# use auto mode, automatically select precision based on the device.
accelerator = Accelerator()
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen-14B-Chat",
    device_map="auto",
    trust_remote_code=True,
    bf16=True
).eval()
model = accelerator.prepare(model)

# 使用DataParallel
#if torch.cuda.device_count() > 1:
#    model = torch.nn.DataParallel(model)

# extract answer from discharge summary
for index, row in tqdm(discharge_test.iterrows(), total=discharge_test.shape[0]):
    subject_id = row['subject_id']
    hadm_id = row['hadm_id']
    discharge_summary = row['text']
    # generate question and answer
    
    question_answer_pairs = []
    for i in range(len(mother_questions)):
        template = mother_questions[i]
        child_list = child_questions[i]
        k = len(child_list)
        random_number = random.randrange(0, k)
        question = child_list[random_number]
        
        input_text = discharge_summary + " " + question

        response, history = model.chat(tokenizer, query=input_text, history=None)
        torch.cuda.empty_cache()
        gc.collect()
        
        question_answer_pairs.append({"question_template": template,
                                      "question": question,
                                      "answer": response,})
        
    data = {"hadm_id": hadm_id,
            "subject_id": subject_id,
            "question_answer_pairs": question_answer_pairs}

    # 根据 subject_id 和 hadm_id 生成文件名
    file_name = f"{subject_id}_{hadm_id}.json"
    file_path = os.path.join("outputs/discharge_summary_qa", file_name)
    # 将数据保存为 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


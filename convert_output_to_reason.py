import pandas as pd
import json
import re
import os

folder_path = 'output'

for file in os.listdir(folder_path):
    df = pd.read_json(os.path.join(folder_path, file), lines=True, encoding='utf-8')

    questions = list(pd.read_csv("final_project_query.csv")["Question"])
    rows = []

    for i, row in df.iterrows():
        ID = row['ID']
        response_raw = row['Response']

        json_str = re.sub(r'^```json\n|```$', '', response_raw.strip(), flags=re.DOTALL)
        json_str = json_str.replace('\n', '')
        
        try:
            inner_json = json.loads(json_str)
            judge = inner_json.get("judge")
            reason = inner_json.get("reason")
            rows.append({"ID": ID, "Question": questions[i], "Judge": judge, "Reason": reason})
        except json.JSONDecodeError as e:
            print(json_str)
            print(f"⚠️ 無法解析 ID={ID} 的 JSON：{e}")

    clean_df = pd.DataFrame(rows)
    clean_df.to_csv('reason/' + file.replace(".jsonl", "") + '.csv', index=False, encoding='utf-8')
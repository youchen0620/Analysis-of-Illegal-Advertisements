import json
import pandas as pd
import re
import os

folder_path = 'output'

for file in os.listdir(folder_path):
    with open(folder_path + '/' + file, 'r', encoding='utf-8') as f:
        data = {
            "ID": [],
            "Answer": []
        }

        for line in f:
            json_raw = json.loads(line)
            data["ID"].append(json_raw["ID"])
            match = re.search(r"\"illegal\"", json_raw["Response"])
            data["Answer"].append("0" if match else "1")

        df = pd.DataFrame(data)
        df.to_csv('submission/' + file.replace(".jsonl", "") + '.csv', index=False, encoding='utf-8')
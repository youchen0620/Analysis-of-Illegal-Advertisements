import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import json
import getpass
import os
from tqdm import tqdm

os.makedirs('output', exist_ok=True)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", """請分析廣告文字內容，根據與參考資料的相似度判斷廣告用詞是否涉及誇大療效及違法

### 廣告文字內容：
{question}

### 合規性判斷
- **無罪判定原則**：不捏造或過度解讀廣告文字，**從寬認定合法性**。

### 參考資料：
- 「完整補充營養」「調整體質」「促進新陳代謝」「幫助入睡」「保護消化道全機能」「改變細菌叢生態」「排便有感」「在嚴謹的營養均衡與熱量控制，以及適當的運動條件下，適量
攝取本產品有助於不易形成體脂肪」這些文字出現時不視為有違法風險。
- 「能完整補充人體營養」、「調整體質」、「提升生理機能」、「調節生理機能」、「促進新陳代謝」、「幫助入睡」、「調整體質」、「青春美麗」、「排便超有感」、「給你排便順暢新體
驗」、「維持正常的排便習慣」、「排便順暢」、「促進新陳代謝」、「調整體質」、「改變細菌叢生態」、調節生理機能」、「保護消化道全機能」、「提升吸收滋養消化機能」"這些文字出
現時不視為有違法風險。

### 輸出格式：
{{"judge": "legal or illegal", "reason": "the reason why legal or illegal"\}}
"""),
    ]
)

gemini_models = ["gemini-2.5-flash-preview-05-20"]
selected_model = 0

llm = ChatGoogleGenerativeAI(
    model=gemini_models[selected_model],
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=0,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

llm_chain = prompt | llm

questions = list(pd.read_csv("final_project_query.csv")["Question"])
for i, question in tqdm(enumerate(questions)):
    result = llm_chain.invoke({"question": question[:512]})
            
    print(result.content)
    with open('output/2.5-flash-direct-prompt.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"ID": i, "Response": result.content}, ensure_ascii=False) + "\n")
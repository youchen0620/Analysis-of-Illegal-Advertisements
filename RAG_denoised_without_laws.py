import langchain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import pandas as pd
import json
import getpass
import os
import time
from tqdm import tqdm

os.makedirs('output', exist_ok=True)

model_name = "dunzhang/stella_en_400M_v5"
model_kwargs = {'device': 'cuda', 'trust_remote_code': True}
embedding = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

vectordb = Chroma(persist_directory="db/denoised_history", embedding_function=embedding)

retriever = vectordb.as_retriever(search_kwargs={'k': 3})

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

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

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""請分析廣告文字內容，根據與參考資料的相似度判斷廣告用詞是否涉及誇大療效及違法

### 廣告文字內容：
{question}

### 合規性判斷
- **無罪判定原則**：不捏造或過度解讀廣告文字，**從寬認定合法性**。

### 參考資料：
{context}

### 輸出格式：
{{"judge": "legal or illegal", "reason": "the reason why legal or illegal"\}}
""",
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

questions = list(pd.read_csv("final_project_query.csv")["Question"])
for i, question in tqdm(enumerate(questions)):
    result = rag_chain.invoke(question[:512])
    print(result)
    with open('output/2.5-flash-rag-denoised-history-top3-similarity-without-laws.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"ID": i, "Response": result}, ensure_ascii=False) + "\n")
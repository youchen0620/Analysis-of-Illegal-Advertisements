from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import shutil
import os

os.makedirs('db', exist_ok=True)

folder_path = 'history'

original_db_directory = 'db/original_history'
denoised_db_directory = 'db/denoised_history'

original_splits, denoised_splits = [], []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)

# original history
for file in os.listdir(folder_path):
    with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
        content = f.read().replace(' ', '')
        doc = Document(
            page_content=content,
        )
        splits = text_splitter.split_documents([doc])
        original_splits.extend(splits)

print(len(original_splits))

# denoised history
with open('filtered_history/case.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        doc = Document(
            page_content=line,
        )
        denoised_splits.append(doc)

print(len(denoised_splits))

model_name = "dunzhang/stella_en_400M_v5"
model_kwargs = {'device': 'cuda', 'trust_remote_code': True}
embedding = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

if os.path.exists(original_db_directory):
    shutil.rmtree(original_db_directory)
vectordb = Chroma.from_documents(documents=original_splits, embedding=embedding, persist_directory=original_db_directory)

if os.path.exists(denoised_db_directory):
    shutil.rmtree(denoised_db_directory)
vectordb = Chroma.from_documents(documents=denoised_splits, embedding=embedding, persist_directory=denoised_db_directory)
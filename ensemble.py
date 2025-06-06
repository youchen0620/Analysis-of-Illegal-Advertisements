import pandas as pd

ids = list(pd.read_csv('submission/2.5-flash-direct-prompt.csv')["ID"])
answer1 = list(pd.read_csv('submission/2.5-flash-direct-prompt.csv')["Answer"])
answer2 = list(pd.read_csv('submission/2.5-flash-rag-original-history-top3-similarity-without-laws.csv')["Answer"])
answer3 = list(pd.read_csv('submission/2.5-flash-rag-denoised-history-top3-similarity-without-laws.csv')["Answer"])

data = {
    "ID": ids,
    "Answer": []
}

for i in range(len(ids)):
    vote = answer1[i] + answer2[i] + answer3[i]
    if vote < 2:
        data["Answer"].append("0")
    else:
        data["Answer"].append("1")

df = pd.DataFrame(data)
df.to_csv('submission_ensemble.csv', index=False, encoding='utf-8')
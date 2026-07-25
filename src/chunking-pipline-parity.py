import json
import os
import re
import sys
from utils import init
import numpy
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = model.tokenizer
tokenCap = model.max_seq_length


wikiClient, rawdataPath, processedPath, wikisources = init()

hadrolledRessults = []
with open(os.path.join(processedPath, 'chunks.jsonl'), "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    for chunk in data :
        tokensize = len(tokenizer.encode(chunk['text']))
        hadrolledRessults.append({
            "chunk_id": chunk['chunk_id'],
            "source_title" : chunk['source_title'],
            "size" : tokensize,
        })

langchnainResults = []
with open(os.path.join(processedPath, 'chunks-langchain.jsonl'), "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    for chunk in data :
        tokensize = len(tokenizer.encode(chunk['text']))
        langchnainResults.append({
            "chunk_id": chunk['chunk_id'],
            "source_title" : chunk['source_title'],
            "size" : tokensize,
        })

handRolledMax = max(x['size'] for x in hadrolledRessults)
langchnainMax = max(x['size'] for x in langchnainResults)

print(handRolledMax)
print(langchnainMax)
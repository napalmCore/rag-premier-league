import json
import os
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import init
import numpy
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = model.tokenizer
tokenCap = model.max_seq_length


wikiClient, rawdataPath, processedPath, wikisources = init()

def buildChunks (blocks, sourceTitle, pageTitle, index, category, joinBy = '\n'):
    accumulatedText = joinBy.join(blocks)
    chunkId = pageTitle + "-" + str(index)
    return {
        "chunk_id": chunkId,
        "source_title" : sourceTitle,
        "category" : category,
        "text" : accumulatedText
    }

chunks = []
for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    cleanPageTitle = re.sub('[^a-zA-Z0-9]', '-', fixedSlug)
    category =  wikiPageSlug["category"]
    processedFilePath = f"{os.path.join(processedPath, cleanPageTitle)}.txt"
    i = 0
    with open(processedFilePath, "r", encoding='utf-8') as f:
        text = f.read()
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=tokenizer,
            chunk_size=254,
            chunk_overlap=150
        )
        texts = text_splitter.create_documents([text])
        for doc in texts :
            chunks.append(buildChunks([doc.page_content], fixedSlug, cleanPageTitle, i, category))
            i += 1

embedChunks = []
with open(os.path.join(processedPath, 'chunks-langchain.jsonl'), "w", encoding="utf-8") as f:
    for chunk in chunks:
        print("************Token length****************")
        print(len(tokenizer.encode(chunk['text'])))
        print(chunk['chunk_id'])
        embedChunks.append(chunk['text'])
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        print(f"chunk: {chunks}")

"""
embed = model.encode(embedChunks)
numpy.save(os.path.join(processedPath, 'embed.npy'), embed)
"""

import os
from networkx import config
import yaml
import wikipediaapi
import re
from utils import init

wikiClient, rawdataPath, processedPath, wikisources = init()

for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    
    ## create a processed file path if it doesn't exist
    processedFilePath = f"{os.path.join(processedPath, re.sub('[^a-zA-Z0-9]', '-', fixedSlug))}.txt"
    with open(processedFilePath, "r", encoding='utf-8') as f:
        text = f.read()
        blocks = re.split(r'\n\n', text)
        print(f"Number of blocks in {wikiPageSlug['title']}: {len(blocks)}")
        for i, block in enumerate(blocks):
            print(repr(block[:15]), "...", repr(block[-15:]))
            #print(f"Block {i}: {repr(block[:100])}...")  # print the first 100 characters of each block

"""
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
#print(type(model.tokenizer))   # what kind of tokenizer is it?
#help(model.tokenizer)          # what can it do?
embeding = model.encode("This is a test sentence.")  # how does it encode a sentence?
print(model.tokenizer.tokenize("This is a test sentence."))           # word-pieces only
print(model.tokenizer.encode("This is a test sentence."))             # what the model really sees
ids = model.tokenizer.encode("This is a test sentence.")
print(ids)
print(model.tokenizer.convert_ids_to_tokens(ids))
"""
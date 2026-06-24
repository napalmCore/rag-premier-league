import os
from networkx import config
import re
from utils import init

wikiClient, rawdataPath, processedPath, wikisources = init()

def stripBlocks(text, separator="\n\n"):
    blocks = text.split(separator)
    outblocks = []
    for block in blocks:
        block = block.strip()
        if block:
            outblocks.append(block)
            pass
    return outblocks


for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    processedFilePath = f"{os.path.join(processedPath, re.sub('[^a-zA-Z0-9]', '-', fixedSlug))}.txt"
    with open(processedFilePath, "r", encoding='utf-8') as f:
        text = f.read()
        output = stripBlocks(text)
        print(f"Processed {len(output)} blocks for page: {fixedSlug}")

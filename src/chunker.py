import json
import os
import sys
from networkx import config
import re
from utils import init
import tokenizers
import tokenizers.models
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

def packer(blocks, chunks, index, fixedSlug, cleanPageTitle, category, splitBy = '\n') :
    accumulatedBlocks = []
    for text in blocks:
        print("text is smaller than token cap continue to packer fit")
        if (len(tokenizer.encode(text)) > tokenCap):
            if (len(accumulatedBlocks) > 0):
                chunks.append(buildChunks(accumulatedBlocks, fixedSlug, cleanPageTitle, index, category, splitBy))
                index = index + 1

            accumulatedBlocks = []
            sentencSplitter = '.'
            sentences = text.split(sentencSplitter)
            #check if the text is not further breakable into sentences
            if (len(sentences) == 1):
                wordSplitter = ' '
                words = sentences[-1].split(wordSplitter)
                if (len(words) == 1) :
                    chunks.append(buildChunks(words, fixedSlug, cleanPageTitle, index, category, wordSplitter))
                    index = index + 1
                    continue

                chunks, index = packer(words, chunks, index, fixedSlug, cleanPageTitle, category, wordSplitter)
                overlap = str(chunks[-1]['text']).split(wordSplitter)[-1]
                accumulatedBlocks = [overlap]
                continue

            chunks, index = packer(sentences, chunks, index, fixedSlug, cleanPageTitle, category, sentencSplitter)
            overlap = str(chunks[-1]['text']).split(sentencSplitter)[-1]
            accumulatedBlocks = [overlap]
            continue

        accumulatedTexts = splitBy.join(accumulatedBlocks) + splitBy + text
        #check if the blocks fits in the accumuulator
        tokens = tokenizer.encode(accumulatedTexts)
        if (len(tokens) > tokenCap) :
            #emit chunk
            print("current block does not fit in the accumulator so we emit and reset the accumulator " + str(index))
            chunks.append(buildChunks(accumulatedBlocks, fixedSlug, cleanPageTitle, index, category, splitBy))
            index = index + 1
            #get last paragraph as overlap
            overlap = str(accumulatedBlocks[-1]).split(splitBy)[-1]
            #calculate if overlap + overflow text > token cap
            accumulatedBlocks = []
            carryForwardBlock = overlap + splitBy + text
            tokens = tokenizer.encode(carryForwardBlock)
            if (len(tokens) <= tokenCap) :
                print("ovrlap and overflow block fits in the token cap")
                accumulatedBlocks.extend([overlap, text])
            else:
                print("ovrlap and overflow block does not fits, dropping overlap")
                accumulatedBlocks.append(text)
        else :
            print("block fits in the accumulator, so we append the block into the accumulator")
            accumulatedBlocks.append(text)

    if (len(accumulatedBlocks) > 0):
        print("emitting the leftover blocks")
        chunks.append(buildChunks(accumulatedBlocks, fixedSlug, cleanPageTitle, index, category, splitBy))
        index = index + 1

    return chunks, index

def stripBlocks(text, separator="\n\n"):
    blocks = text.split(separator)
    outblocks = []
    for block in blocks:
        block = block.strip()
        if block:
            outblocks.append(block)
            pass
    return outblocks

chunks = []
for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    cleanPageTitle = re.sub('[^a-zA-Z0-9]', '-', fixedSlug)
    category =  wikiPageSlug["category"]
    processedFilePath = f"{os.path.join(processedPath, cleanPageTitle)}.txt"
    i = 0
    with open(processedFilePath, "r", encoding='utf-8') as f:
        text = f.read()
        output = stripBlocks(text)
        chunks, i = packer(output, chunks, i, fixedSlug, cleanPageTitle, category)

#write chunks into the jsonl
with open(os.path.join(processedPath, 'chunks.jsonl'), "w", encoding="utf-8") as f:
    for chunk in chunks:
        print("************Token length****************")
        print(len(tokenizer.encode(chunk['text'])))
        print(chunk['chunk_id'])
        f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        #print(f"chunk: {chunks}")

print(max(len(tokenizer.encode(c["text"])) for c in chunks))
#for chunk in chunks:




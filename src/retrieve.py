import json
import os
import sys
from utils import init
import numpy
from sentence_transformers import SentenceTransformer
import anthropic

api_key=os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def buildContext(chunks):
    context = []
    for chunk in chunks:
         context.append("Source:" + chunk['source_title'] + '\n' + chunk['text'])

    return '\n\n'.join(context)

model = SentenceTransformer("all-MiniLM-L6-v2")
query = "how old was david beckham when he first won a title with manchester united"
embedQuery = model.encode([query])
wikiClient, rawdataPath, processedPath, wikisources = init()
embeded = numpy.load(os.path.join(processedPath, 'embed.npy'))
similarityResult = model.similarity(embedQuery, embeded)
topShape = similarityResult.topk(5)
topIndexes = topShape.indices[0]
topChunks = []
with open(os.path.join(processedPath, 'chunks.jsonl'), "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    if (len(data) != len(embeded)):
        sys.exit("Error: index out of sync.")
    else:
        for i in topIndexes :
            topChunks.append(data[i])

if (len(topChunks) > 0) :
    context = buildContext(topChunks)
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "answre this question:" + query + ' From this content below:\n' + context
            }
        ]
    )
    print(message.content)
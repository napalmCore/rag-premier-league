import json
import os

from utils import init
import anthropic
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def buildContext(documents):
    context = []
    for document in documents:
        print(document.metadata['source_title'], document.metadata.get('chunk_id'))
        context.append("Source:" + document.metadata['source_title'] + '\n' + document.page_content)

    return '\n\n'.join(context)

wikiClient, rawdataPath, processedPath, wikisources = init()
api_key=os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

query = "how old was david beckham when he first won a title with manchester united"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore(embeddings)
documents = []
with open(os.path.join(processedPath, 'chunks.jsonl'), "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    for chunk in data :
        doc = Document(
            page_content=chunk['text'],
            metadata={"source_title": chunk['source_title'], "category": chunk['category'], "chunk_id" : chunk['chunk_id']}
        )
        documents.append(doc)

vector_store.add_documents(documents)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
llm = ChatAnthropic(model="claude-sonnet-5")
prompt = ChatPromptTemplate.from_template("""
Answer the question based strictly on the following context, don't fabricate if the context doesn't cover it:
{context}

Question: {question}
Answer:""")

rag_chain = (
    {"context": retriever | buildContext, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 9. Invoke the pipeline with your target question
response = rag_chain.invoke(query)

print(response)

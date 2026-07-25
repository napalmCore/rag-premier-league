### Simple RAG system for a premier league wikipages

## Set up instruction
 1. Clone the repo 
 2. in config.yml replace the wikiusergaent with yours : user_agent: "rag-premier-league/1.0 (wikitest@mailinator.com)"
 3. run pip install -r requirements.txt
 4. generate the raw data source from wiki: py .\src\fetch.py
 5. clean up the raw data run : py .\src\preprocess.py
 6. Chunks the preprocessed files and embedd tje chunks in numpy format: py .\src\chunker.py
 7. set up your claude api key in nv var : $env:ANTHROPIC_API_KEY = "{YOUR_KEY}"
 8. run the retrieval program : py .\src\retrieve.py "when man united was founded"


import os
import re
from utils import init

wikiClient, rawdataPath, processedPath, wikisources = init()

results = []
for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    
    print(f"Fetching page: {fixedSlug}")
    
    try:
        page_py = wikiClient.page(fixedSlug)
        if page_py.exists():
            #create a file with the name of the page and write the summary to it
            with open(f"{os.path.join(rawdataPath, re.sub('[^a-zA-Z0-9]', '-', fixedSlug))}.txt", "w", encoding='utf-8') as f:
                #encode the summary to utf-8 and ignore errors
                pageContent = page_py.text
                #print(pageContent)
                f.write(pageContent)
                results.append({"title": fixedSlug})
        else:
            print(f"Page {wikiPageSlug} does not exist.")
            results.append({"title": fixedSlug, "error": "Page does not exist"})    
        pass
    except Exception as e:
        print(f"Error fetching page {fixedSlug}: {e}")
        results.append({"title": fixedSlug, "error": str(e)})
        continue
    
for error in results:
    if "error" in error:
        print(f"Error fetching page {error['title']}: {error['error']}")

for result in results:
    if "title" in result and "error" not in result:
        print(f"Successfully fetched page: {result['title']}")





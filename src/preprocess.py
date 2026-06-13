import os
import yaml
import wikipediaapi
import re
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)   # assuming fetch.py lives in src/


  
with open(os.path.join(PROJECT_ROOT, "config.yaml"), "r", encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)


wikiClient = wikipediaapi.Wikipedia(
    user_agent=config["wikiApi"]["user_agent"], language=config["wikiApi"]["language"])

rawdataPath = os.path.abspath(os.path.join(PROJECT_ROOT, "data/raw/"))
processedPath = os.path.abspath(os.path.join(PROJECT_ROOT, "data/processed/"))
wikisources = config["pages"]

def clean(text):
    stripFromHere = ["See also", "References", "Notes", "Sources", "Further reading", "External links", "League table", "Results", 
                    "Season statistics", "Honours", "Discipline", "Awards", "Career statistics", "Top scorers", 
                    "Hat-tricks", "Clean sheets", "Personnel and kits", 
                    "Stadiums and locations", "Top assists", "Monthly awards", "Attendances",
                    "Ownership", "Management", "Managerial history", "First-team coaching staff", 
                    "Player of the Year awards", "Under-21s and Academy", 
                    "Out on loan", "First-team squad", "Players", "Arsenal board", "Kit suppliers and shirt sponsors", "Kit deals"]
    for strip in stripFromHere:
        text = re.sub(f"({strip}|{strip})(\\n.*)+", "", text)
        text = text.strip()
    return text

os.makedirs(processedPath, exist_ok=True)

## Clean the text by removing sections that are not relevant to the summary
## read the file and clean it, then write it back to the file
for wikiPageSlug in wikisources:
    fixedSlug = wikiPageSlug["title"]
    filePath = f"{os.path.join(rawdataPath, re.sub('[^a-zA-Z0-9]', '-', fixedSlug))}.txt"
    
    ## create a processed file path if it doesn't exist
    processedFilePath = f"{os.path.join(PROJECT_ROOT, 'data/processed/', re.sub('[^a-zA-Z0-9]', '-', fixedSlug))}.txt"

    with open(filePath, "r", encoding='utf-8') as f:
        text = f.read()
        cleanedText = clean(text)
    with open(processedFilePath, "w", encoding='utf-8') as f:
        f.write(cleanedText)
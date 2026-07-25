import os
import yaml
import wikipediaapi

def init():
    global wikiClient, rawdataPath, processedPath, wikisources

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

    with open(os.path.join(PROJECT_ROOT, "config.yaml"), "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.loader.SafeLoader)
    
    wikiClient = wikipediaapi.Wikipedia(
        user_agent=config["wikiApi"]["user_agent"], language=config["wikiApi"]["language"])
    
    rawdataPath = os.path.abspath(os.path.join(PROJECT_ROOT, "data/raw/"))
    processedPath = os.path.abspath(os.path.join(PROJECT_ROOT, "data/processed/"))
    wikisources = config["pages"]
    return wikiClient, rawdataPath, processedPath, wikisources

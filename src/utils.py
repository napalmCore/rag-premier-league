import os
from pathlib import Path
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
    Path(rawdataPath).mkdir(parents=True, exist_ok=True)
    processedPath = os.path.abspath(os.path.join(PROJECT_ROOT, "data/processed/"))
    Path(processedPath).mkdir(parents=True, exist_ok=True)
    wikisources = config["pages"]
    return wikiClient, rawdataPath, processedPath, wikisources

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
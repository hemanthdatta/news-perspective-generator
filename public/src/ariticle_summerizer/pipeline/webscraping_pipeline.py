import sys
import os
from pathlib import Path

ROOT_dir = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))

from src.ariticle_summerizer.conponents.stage_01_url_webscraping_version_1 import get_article_content
from src.ariticle_summerizer.logging import logging

def webscraping_pipeline_main(url):
    text_content = get_article_content(url)
    with open("article.txt", "w") as file:
        file.write(text_content)

    logging.info("Successfully extracted article content")
    return text_content

if __name__ == '__main__':
    url = "https://www.bbc.com/news/articles/cd11lz4vpr7o"
    text = webscraping_pipeline_main(url)
    print(text)

import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys
from pathlib import Path


ROOT_dir = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))
from src.ariticle_summerizer.logging import logging
from src.ariticle_summerizer.pipeline.webscraping_pipeline import webscraping_pipeline_main
from src.ariticle_summerizer.utils.common import read_yaml_file
from src.ariticle_summerizer.constants import config_yaml_file_path

load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
logging.info(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

stage_02_config = read_yaml_file(config_yaml_file_path)
print(stage_02_config)
promts_yaml_as_dict = read_yaml_file(stage_02_config['promts_yaml_file_path'])

def generate_perspective(text, perspective):
    try:
        #print(promts)
        if perspective == "business":
            prompt =  str(promts_yaml_as_dict['prompts']['business_promt'])+text

        elif perspective == "political":
            prompt = str(promts_yaml_as_dict['prompts']['political_promt'])+text

        else:  # UPSC
            prompt = str(promts_yaml_as_dict['prompts']['UPSC_promt'])+text


        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.info(f"Error generating {perspective} perspective: {str(e)}")
        return f"Error generating {perspective} perspective: {str(e)}"

if __name__ == '__main__':
    url = "https://www.bbc.com/news/articles/cd11lz4vpr7o"
    article_text = webscraping_pipeline_main(url)
    print(generate_perspective(article_text, "business"))
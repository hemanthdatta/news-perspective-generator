import os
import sys
from pathlib import Path
ROOT_dir = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))
from src.ariticle_summerizer.logging import logging
from src.ariticle_summerizer.conponents.stage_02_get_context_of_website import generate_perspective
from src.ariticle_summerizer.pipeline.webscraping_pipeline import webscraping_pipeline_main

def context_generating_pipeline_main(text, perspective):
    return generate_perspective(text, perspective)



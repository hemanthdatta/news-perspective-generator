from flask import Flask, render_template, request, jsonify, url_for, session
import requests
from bs4 import BeautifulSoup
import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
from pathlib import Path
ROOT_dir = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))
from src.ariticle_summerizer.logging import logging


def get_article_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        if not text or len(text.split()) < 10:
            raise ValueError("Could not extract meaningful content from the article")
            
        return text
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {str(e)}")
        raise ValueError(f"Could not access the article. The website might be blocking access. Please try a different news source.")
    except Exception as e:
        logging.error(f"Error processing URL {url}: {str(e)}")
        raise ValueError(f"Error processing the article: {str(e)}")

if __name__ == '__main__':
    url = "https://www.bbc.com/news/articles/cd11lz4vpr7o"
    text = get_article_content(url)
    print(text)
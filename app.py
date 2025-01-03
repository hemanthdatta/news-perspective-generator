from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging
import sys
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

def extract_article_content(url):
    try:
        logger.debug(f"Attempting to fetch content from URL: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        logger.debug(f"Successfully extracted {len(text)} characters from the URL")
        return text[:15000]  # Limit text length for processing
    except Exception as e:
        logger.error(f"Error extracting content: {str(e)}")
        return str(e)

def generate_perspective(text, perspective):
    try:
        if perspective == "business":
            prompt = f"""Analyze this news article from a business perspective. Focus on:
            1. Economic impacts and market implications
            2. Business opportunities or challenges
            3. Industry trends and market dynamics
            4. Financial implications
            
            Article: {text}
            
            Provide a concise analysis focusing only on business aspects."""
        elif perspective == "political":
            prompt = f"""Analyze this news article from a political perspective. Focus on:
            1. Government policies and decisions
            2. Political implications and consequences
            3. Impact on governance and administration
            4. Stakeholder interests and conflicts
            
            Article: {text}
            
            Provide a concise analysis focusing only on political aspects."""
        else:  # UPSC
            prompt = f"""Analyze this news article from a UPSC (Civil Services) exam perspective. Focus on:
            1. Administrative and governance aspects
            2. Constitutional and legal implications
            3. Socio-economic impacts
            4. Policy frameworks and implementation
            
            Article: {text}
            
            Provide a concise analysis that would be relevant for UPSC exam preparation."""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating {perspective} perspective: {str(e)}")
        return f"Error generating {perspective} perspective: {str(e)}"

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return str(e)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        logger.debug(f"Received request to analyze URL: {url}")
        content = extract_article_content(url)
        
        if isinstance(content, str) and "Error" in content:
            return jsonify({"error": content}), 400

        # Generate all three perspectives
        business_perspective = generate_perspective(content, "business")
        political_perspective = generate_perspective(content, "political")
        upsc_perspective = generate_perspective(content, "upsc")
        
        return jsonify({
            "business": business_perspective,
            "political": political_perspective,
            "upsc": upsc_perspective
        })
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not GOOGLE_API_KEY:
        print("Please set your GOOGLE_API_KEY in the .env file")
        sys.exit(1)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

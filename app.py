from flask import Flask, render_template, request, jsonify, url_for, session
import requests
from bs4 import BeautifulSoup
import sys
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from pathlib import Path

ROOT_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))

from src.ariticle_summerizer.logging import logging
from src.ariticle_summerizer.pipeline.webscraping_pipeline import webscraping_pipeline_main
from src.ariticle_summerizer.pipeline.context_generating_pipe_line import context_generating_pipeline_main

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
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["chrome-extension://*", "http://localhost:*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
app.secret_key = 'your_secret_key_here'
############################################
def get_article_content(url):
    pass
############################################

############################################
def generate_perspective(text, perspective):
    pass
############################################



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
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400

        url = data['url']
        
        try:
            article_text = webscraping_pipeline_main(url)
            if not article_text:
                return jsonify({'error': 'Could not extract article content. This might be due to website restrictions.'}), 400
            
            session['article_text'] = article_text
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return jsonify({'error': 'Failed to access the article. The website might be blocking automated access.'}), 400

        try:
            perspectives = {}
            perspectives_list = ['business', 'political', 'upsc']
            for p in perspectives_list:
                try:
                    perspectives[p] = context_generating_pipeline_main(article_text, p)
                except Exception as e:
                    logging.error(f"Error generating {p} perspective: {str(e)}")
                    perspectives[p] = f"Error generating {p} perspective. Please try again."
            
            session['analysis_results'] = perspectives
            
            return jsonify(perspectives)
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return jsonify({'error': 'An error occurred while analyzing the article.'}), 500

    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('question')
        article_text = session.get('article_text')
        analysis_results = session.get('analysis_results', {})
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        if not article_text:
            return jsonify({'error': 'No article context found. Please analyze an article first.'}), 400
            
        # Create a comprehensive prompt using both article and analysis
        prompt = f"""Based on this article content and its analysis:

Article:
{article_text[:1500]}...

Analysis Summary:
"""
        # Add available analyses
        for perspective, analysis in analysis_results.items():
            prompt += f"\n{perspective.upper()} PERSPECTIVE:\n{analysis[:300]}...\n"
        
        prompt += f"""
Question: {question}

Provide a clear and informative answer based on both the article content and its analysis. 
If the question cannot be answered using the available information, say so.
Format your response using markdown for better readability."""
        
        try:
            response = model.generate_content(prompt)
            return jsonify({'response': response.text})
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            return jsonify({'error': 'Failed to generate response from AI model'}), 500
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your question'}), 500

@app.route('/suggested_questions', methods=['GET'])
def suggested_questions():
    try:
        article_text = session.get('article_text')
        analysis_results = session.get('analysis_results', {})
        
        if not article_text:
            return jsonify({'error': 'No article context found. Please analyze an article first.'}), 400
            
        prompt = """Generate exactly 3 relevant questions about this article. Format your response as a comma-separated list of questions.

Article:
{text}

Example format:
What are the key economic implications discussed in the article?, How does this news affect international relations?, What are the potential long-term consequences?

Generate 3 questions:""".format(text=article_text[:1500])
        
        try:
            response = model.generate_content(prompt)
            questions = [q.strip() for q in response.text.split('?') if q.strip()]
            questions = [f"{q}?" for q in questions[:3]]  # Ensure we have exactly 3 questions
            
            if not questions:
                # Fallback questions if generation fails
                questions = [
                    "What are the main points discussed in this article?",
                    "What are the potential implications of this news?",
                    "How might this affect future developments?"
                ]
            
            return jsonify({'questions': questions})
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            return jsonify({'error': 'Failed to generate questions'}), 500
        
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
        return jsonify({'error': 'An error occurred while generating questions'}), 500

if __name__ == '__main__':
    if not GOOGLE_API_KEY:
        print("Please set your GOOGLE_API_KEY in the .env file")
        sys.exit(1)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
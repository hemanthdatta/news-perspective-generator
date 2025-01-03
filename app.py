from flask import Flask, render_template, request, jsonify, url_for
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
            prompt = f"""Analyze this news article from a business perspective. Structure your response in the following format:

📈 **ECONOMIC IMPACT**
• **Market Dynamics**: [Key point about market changes]
• **Financial Impact**: [Key point about financial implications]
• **Economic Indicators**: [Key point about economic metrics]

💼 **MARKET IMPLICATIONS**
• **Industry Trends**: [Key point about industry changes]
• **Competition**: [Key point about competitive landscape]
• **Market Opportunities**: [Key point about potential opportunities]

🔄 **BUSINESS OPPORTUNITIES**
• **Growth Areas**: [Key point about expansion possibilities]
• **Strategic Moves**: [Key point about strategic implications]
• **Investment Potential**: [Key point about investment aspects]

💡 **KEY INSIGHTS**
• **Primary Impact**: [Most important business impact]
• **Future Outlook**: [Prediction or future implications]

Article: {text}

Format your response using markdown: Use **bold** for key terms and section headers, and bullet points for lists."""

        elif perspective == "political":
            prompt = f"""Analyze this news article from a political perspective. Structure your response in the following format:

🏛️ **POLICY IMPLICATIONS**
• **Policy Changes**: [Key point about policy modifications]
• **Legislative Impact**: [Key point about legal changes]
• **Regulatory Framework**: [Key point about regulations]

⚖️ **GOVERNANCE IMPACT**
• **Administrative Changes**: [Key point about governance]
• **Implementation**: [Key point about execution]
• **Institutional Effects**: [Key point about institutional impact]

👥 **STAKEHOLDER ANALYSIS**
• **Key Players**: [Important stakeholders involved]
• **Interest Groups**: [Affected groups]
• **Public Impact**: [Effect on general public]

🎯 **KEY TAKEAWAYS**
• **Critical Impact**: [Most significant political impact]
• **Future Developments**: [Expected political developments]

Article: {text}

Format your response using markdown: Use **bold** for key terms and section headers, and bullet points for lists."""

        else:  # UPSC
            prompt = f"""Analyze this news article from a UPSC (Civil Services) exam perspective. Structure your response in the following format:

📚 **ADMINISTRATIVE ASPECTS**
• **Governance**: [Key point about administration]
• **Policy Framework**: [Key point about policy]
• **Implementation**: [Key point about execution]

⚡ **CONSTITUTIONAL IMPLICATIONS**
• **Legal Framework**: [Key point about legal aspects]
• **Constitutional Provisions**: [Relevant provisions]
• **Precedents**: [Related cases or examples]

🌐 **SOCIO-ECONOMIC IMPACT**
• **Social Changes**: [Key point about social impact]
• **Economic Effects**: [Key point about economic impact]
• **Development Goals**: [Related development aspects]

📝 **EXAM FOCUS POINTS**
• **Key Topics**: [Important topics for study]
• **Previous Questions**: [Related UPSC questions]

Article: {text}

Format your response using markdown: Use **bold** for key terms and section headers, and bullet points for lists."""

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
        url = data.get('url')
        perspective = data.get('perspective', 'all')  # Default to all perspectives

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Fetch and extract text from the URL
        text = extract_article_content(url)
        if isinstance(text, str) and "Error" in text:
            return jsonify({'error': text}), 400

        # Generate perspective based on request
        result = {}
        if perspective == 'all' or perspective == 'business':
            result['business'] = generate_perspective(text, 'business')
        if perspective == 'all' or perspective == 'political':
            result['political'] = generate_perspective(text, 'political')
        if perspective == 'all' or perspective == 'upsc':
            result['upsc'] = generate_perspective(text, 'upsc')

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not GOOGLE_API_KEY:
        print("Please set your GOOGLE_API_KEY in the .env file")
        sys.exit(1)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

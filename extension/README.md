# News Perspective Generator Chrome Extension

This Chrome extension allows you to analyze news articles from multiple perspectives using AI. It provides business, political, and UPSC (Civil Services) perspectives on any news article you're reading.

## Features

- Analyze any news article with a single click
- Get multiple perspectives:
  - Business perspective
  - Political perspective
  - UPSC perspective
- Interactive chat to ask questions about the article
- Suggested questions based on article content
- Beautiful and responsive UI

## Installation

1. Clone this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top right
4. Click "Load unpacked" and select the `extension` folder

## Usage

1. Start the backend server:
   ```bash
   cd ../
   python app.py
   ```

2. Click the extension icon while on any news article
3. Click "Analyze Current Page"
4. View the different perspectives
5. Ask questions about the article in the chat section

## Requirements

- The backend server must be running on `localhost:8000`
- Google Chrome browser
- Internet connection

## Note

Make sure the backend server is running before using the extension. The extension needs to communicate with the server to analyze articles and answer questions.

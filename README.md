# News-Perspective-Generator

> **An AI-driven web app that ingests news articles and generates concise summaries along with multiple viewpoints—political, economic, social, and technical—using Google Gemini.**

[![License](https://img.shields.io/github/license/hemanthdatta/news-perspective-generator?style=flat-square\&logo=opensourceinitiative)](https://choosealicense.com/licenses/mit/)
[![Last Commit](https://img.shields.io/github/last-commit/hemanthdatta/news-perspective-generator?style=flat-square\&logo=git\&logoColor=white)](https://github.com/hemanthdatta/news-perspective-generator/commits/main)
\[![Top Language](https://img.shields.io/github/languages/top/hemanthdatta/news-perspective-generator?style=flat-square\&color=00ff36)]
\[![Dependencies](https://img.shields.io/librariesio/release/pypi/news-perspective-generator?style=flat-square\&logo=pypi\&color=blue)]
\[![Build Status](https://img.shields.io/github/actions/workflow/status/hemanthdatta/news-perspective-generator/ci.yml?style=flat-square\&logo=github)]

---

## 📍 Table of Contents

* [📖 Overview](#-overview)
* [🚀 Features](#-features)
* [🛠️ Tech Stack](#️-tech-stack)
* [📁 Project Structure](#-project-structure)
* [🎨 Screenshots](#️-screenshots)
* [⚙️ Installation & Setup](#️-installation--setup)
* [🤖 Usage Examples](#️-usage-examples)
* [✔️ Testing](#️-testing)
* [📌 Roadmap](#️-roadmap)
* [🤝 Contributing](#️-contributing)
* [📄 License](#-license)
* [🙏 Acknowledgments](#-acknowledgments)

---

## 📖 Overview

**News-Perspective-Generator** is an interactive Flask-based web application designed to help users quickly digest lengthy news articles. By leveraging Google Gemini, the app not only summarizes articles but also generates diverse perspectives—political, economic, social, and technical—so you can grasp complex issues from multiple angles.

Key benefits:

* **Time-saving**: Get concise summaries in seconds.
* **Holistic understanding**: Explore differing viewpoints to reduce bias.
* **Customizable prompts**: Tailor the output to your needs via configuration files.

---

## 🚀 Features

* **Article Ingestion**: Paste a URL or raw text to fetch and parse content.
* **Advanced Summarization**: Condenses articles into concise summaries.
* **Perspective Generation**: Automatically produces four distinct viewpoints:

  * Political
  * Economic
  * Social
    
* **Configurable Prompts**: Edit `prompts.yaml` to adjust Gemini prompt templates.
* **User-friendly UI**: Responsive design built with HTML5, CSS, and lightweight JS.
* **Flexible Settings**: Tune model parameters in `config/config.yaml` and `params.yaml`.
* **Heroku-ready**: Includes a `Procfile` for seamless deployment.

---

## 🛠️ Tech Stack

| Component     | Technology                       |
| ------------- | -------------------------------- |
| Backend       | Python, Flask, Gunicorn          |
| AI Engine     | Google Gemini API                |
| Frontend      | HTML5, CSS3, JavaScript          |
| Configuration | YAML (`config/`, `prompts.yaml`) |
| Deployment    | Heroku, Docker (optional)        |
| Testing       | Pytest                           |

---

## 📁 Project Structure

```bash
news-perspective-generator/
├── .github/workflows/        # CI/CD pipeline (GitHub Actions)
├── config/                   # Application & pipeline configs
│   ├── config.yaml           # Flask settings, API keys
│   └── params.yaml           # Summarization & Gemini parameters
├── prompts.yaml              # Gemini prompt templates
├── src/                      # Core modules
│   └── article_summarizer/   # Scraping, summarization, and context logic
│       ├── components/       # Pipeline stages
│       └── utils/            # Helper functions
├── templates/                # Jinja2 HTML templates
│   └── index.html            # Main web UI
├── static/                   # CSS, JS, images
│   └── css/                  # Stylesheets
├── app.py                    # Flask application entrypoint
├── main.py                   # Orchestrates end-to-end workflow
├── dummy_app.py              # Minimal example for quick testing
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installer
├── Procfile                  # Heroku deployment command
└── tests/                    # Unit & integration tests
    └── test_*.py             # Test files
```

---

## 🎨 Screenshots

> *Placeholder: replace with actual screenshots of the UI*

![Home Page](docs/screenshots/home.png)
![Results](docs/screenshots/results.png)

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.8+
* Pip
* (Optional) Docker & Docker Compose

### Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/hemanthdatta/news-perspective-generator.git
   cd news-perspective-generator
   ```

2. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment**

   * Copy `.env.example` to `.env` and fill in your Google Gemini API key and other settings.

4. **Run locally**

   ```bash
   python app.py
   ```

5. **Access the app**
   Open your browser at `http://127.0.0.1:5000`

### Docker Setup (Optional)

1. **Build the Docker image**

   ```bash
   docker build -t news-perspective-generator .
   ```

2. **Run container**

   ```bash
   docker run -p 5000:5000 --env-file .env news-perspective-generator
   ```

---

## 🤖 Usage Examples

### Generating Perspectives via Web UI

1. Enter a news article URL or paste raw text.
2. Click **Generate Perspectives**.
3. View summary and four distinct viewpoints.

### CLI Example

```bash
python main.py --input-file article.txt --output perspectives.json
```

**Sample Output**:

```json
{
  "summary": "...",
  "political": "...",
  "economic": "...",
  "social": "...",
  "technical": "..."
}
```

---

## ✔️ Testing

Run all tests with:

```bash
pytest --cov=src
```

View coverage report in `htmlcov/` after tests.

---

## 📌 Roadmap

* **Stage 1 (Complete)**: Article ingestion & summarization
* **Stage 2 (In Progress)**: Perspective generation (Gemini prompts)
* **Stage 3**: UI enhancements & accessibility improvements
* **Stage 4**: Deployment automation (Docker Compose, Terraform)
* **Stage 5**: Multi-language support & browser extensions

Contributions and suggestions are welcome!

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

Please read [CONTRIBUTING.md](https://github.com/hemanthdatta/news-perspective-generator/blob/main/CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](https://choosealicense.com/licenses/mit/) for details.

---

## 🙏 Acknowledgments

* Inspired by research in AI summarization and multi-perspective analysis.
* Powered by [Google Gemini](https://developers.google.com/gemini).
* Icons by [VSCode Material Icon Theme](https://github.com/PKief/vscode-material-icon-theme).
* Badges by [Shields.io](https://shields.io/).

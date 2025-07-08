# Daily News AI-Powered Platform

**DAILY NEWS** is an AI-driven news platform that showcases an end-to-end intelligent news publishing pipeline. It automates content generation using LLMs, applies fact-checking with external APIs, classifies and scores content for publishing, and renders it in various formats (text, image-enhanced, or video-based). It also supports user interaction (likes, shares, comments, bookmarks) through anonymous session tracking.

The system integrates AI services like OpenAI, Claude, Google Fact Check, NewsAPI, DALL·E, and Synthesia to create a dynamic, data-verified content pipeline suitable for news delivery at scale.

## 🚀 Features

### AI Content Generation
Generate news content using large language models like GPT-3.5 (OpenAI) and Claude (Anthropic), with custom prompt templates and token controls.

### Automated Fact-Checking
Analyze and verify claims using external APIs for transparency, source credibility, accuracy, and clarity.

### Content Processing Pipeline
- NLP-based content classification and keyword tagging
- Composite score calculation
- Publish/unpublish decisions

### Multimodal Content Delivery
Publish articles as:
- Pure text
- Text with AI-generated images (via DALL·E)
- Videos with LLM-generated summaries (via Synthesia)

### User Interaction
- Anonymous user sessions tracked by UUID tokens
- Users can like, comment, share, and bookmark content

### Admin Functionality
- Admins can override publishing status
- Moderate evidence for fact-checking
- Manage all content types via Django admin

### Frontend Integration
Designed to work with a frontend built using React and TailwindCSS, consuming the backend APIs for content display and interaction.

### Deployed on Render
Backend hosted on Render (Starter Tier), with CORS setup for frontend interaction. PostgreSQL used as the primary DB.

## 🧠 Core Tech Stack

- **Backend**: Django, Django REST Framework
- **LLMs & AI**: OpenAI GPT-3.5, Anthropic Claude, DALL·E, Synthesia
- **Fact Checking APIs**: Google Fact Check Tools API, NewsAPI
- **Database**: PostgreSQL
- **Deployment**: Render
- **Frontend Integration**: React + TailwindCSS (via CORS)

## 📁 Project Structure

```
DailyNews/
├── dailynews_backend/      # Project settings & root URL configuration
├── content_generation/     # Handles prompt setup and LLM-based content generation
├── fact_checking/          # Interfaces with APIs to verify factual accuracy
├── content_processing/     # Categorizes content, computes scores, and manages publishing
├── content_modality/       # Stores multimodal versions: text, image, and video
├── user_management/        # Handles anonymous session creation and interaction tracking
├── utils/                  # Shared helper functions and prompt utilities
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 📦 Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/DailyNews.git
cd DailyNews
```

### 2. Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment setup

Create a `.env` file and add your API keys and DB config:

```ini
SECRET_KEY=...
OPENAI_API_KEY=...
GOOGLE_FACT_CHECK_API_KEY=...
DATABASE_URL=...
DEBUG=True
```

### 5. Run migrations & start development server

```bash
python manage.py migrate
python manage.py runserver
```

## 🔗 API Endpoints Overview

### User
- `POST /api/user/login/` — Create user session
- `GET /api/user/session/` — Validate session

### Content Generation
- `POST /api/content/generate/` — Create new article from prompt

### Fact-Checking
- `POST /api/fact-check/` — Submit text to be verified

### Content Processing
- `POST /api/process/<id>/` — Categorize and score generated content
- `GET|PUT /api/published/<id>/evidence/` — View or edit fact-check evidence

### Written Content
- `POST /news/written/`
- `GET /news/written/get/`
- `POST /news/written/<id>/comment/`, `/like/`, `/share/`, `/bookmark/`

### Written + Image Content
Same structure under `/news/written-image/`

### Video Content
Same structure under `/news/video/`

## 🔐 Deployment Instructions (Render)

1. **Connect repo to Render**

2. **Configure build and start commands:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   gunicorn dailynews_backend.wsgi
   ```

3. **Add environment variables** under the Render dashboard

4. **Set CORS_ALLOWED_ORIGINS** to your frontend URL

## 📘 License

This project is licensed under the MIT License. See LICENSE for details.

# 📧 NLP-Based Email Generation and Tone Adaptation System

**Python | FastAPI | Streamlit | Groq**

An advanced Natural Language Processing (NLP) system that generates professional business emails from brief prompts and seamlessly adapts their tone (Formal, Friendly, Urgent, etc.) using AI.

---

## ✨ Key Features

- 🔄 **Multi-Tone Adaptation:** Generate emails in 6 distinct tones: Formal, Friendly, Urgent, Apologetic, Persuasive, Neutral  
- ⚖️ **Tone Comparison:** Generate the same email in multiple tones side-by-side to choose the best fit  
- 🎯 **Tone Transformation:** Paste an existing email and instantly rewrite it into a different tone while preserving all facts  
- 🧠 **NLP Context Extraction:** Automatically detects and preserves key entities (Dates, Amounts, Action Items) from prompts  
- 📊 **Confidence Scoring:** Verifies how many key points were covered in the generated email  
- ⚡ **Blazing Fast:** Powered by Groq API (Llama 3.1) for lightning-fast email generation  

---

## 🏗️ System Architecture

```
User Interface (Streamlit)
            │
            ▼
Backend API (FastAPI)
            │
            ▼
Prompt Builder (Tone + Context Rules)
            │
            ▼
LLM Engine (Groq AI - Llama 3.1)
            │
            ▼
Post Processor (Clean + Extract Subject/Body)
            │
            ▼
JSON Response → Frontend
```

---

## 🛠️ Tech Stack

| Component        | Technology                  | Purpose                              |
|----------------|---------------------------|--------------------------------------|
| Frontend        | Streamlit                 | Interactive Web UI                   |
| Backend         | FastAPI                   | High-performance API routing         |
| AI Engine       | Groq (Llama-3.1-8b)       | Fast & efficient text generation     |
| Data Validation | Pydantic                  | Input sanitization & validation      |
| Environment     | Python Dotenv             | Secure API key management           |

---

## 🚀 Quick Start (How to Run)

### 📌 Prerequisites
- Python 3.11+
- Groq API Key (free)

---

### 📥 Installation Steps

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/email-tone-system.git
cd email-tone-system
```

#### 2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup environment variables
Create a `.env` file:

```env
GROQ_API_KEY=gsk_your_actual_key_here
MODEL_NAME=llama-3.1-8b-instant
```

#### 5. Run the project

**Option 1 (Easy - Windows):**
```bash
start.bat
```

**Option 2 (Manual):**

Backend:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
python -m streamlit run streamlit_app.py
```

---

## 📂 Project Structure

```text
email-tone-system/
│
├── .env                    # Secret API Keys
├── .gitignore             # Ignored files for Git
├── requirements.txt       # Dependencies
├── start.bat              # One-click startup
├── streamlit_app.py       # Frontend UI
│
└── app/
    ├── main.py            # FastAPI entry point
    ├── config.py          # Configuration loader
    │
    ├── api/
    │   └── routes.py      # API endpoints
    │
    ├── models/
    │   └── schemas.py     # Pydantic models
    │
    ├── services/
    │   └── generator.py   # Core AI logic
    │
    └── utils/
        └── tone_lexicon.py # Tone rules dictionary
```

---

## 💡 How to Use

- ✍️ **Generate Tab:** Enter recipient, sender, key points, select tone → generate email  
- ⚖️ **Compare Tab:** View multiple tones side-by-side  
- 🎯 **Adapt Tab:** Paste existing email → rewrite in selected tone instantly  

---

## 🔮 Future Scope

- 🌍 Multi-language email generation (Hindi, Spanish, etc.)  
- 🧠 Email thread context awareness  
- 🎯 Fine-tuned LLM for business emails  
- 💾 Database integration for email history  

---

## 🙏 Acknowledgements

- Groq — ultra-fast inference API  
- Streamlit — simple UI development  
- FastAPI — powerful backend framework

---

## 👩‍💻 Author

**Savaira Majeed**

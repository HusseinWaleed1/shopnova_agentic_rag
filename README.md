# 🛍️ ShopNova — Agentic RAG Customer Support System

> A production-ready AI customer support agent powered by LangGraph, OpenAI, Pinecone, and FastAPI. Deployed on Railway + Streamlit Cloud.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-purple)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Deployed](https://img.shields.io/badge/Deployed-Railway%20%2B%20Streamlit-success)

---

## 🧠 What is Agentic RAG?

Unlike traditional RAG (retrieve → answer), this system uses a **multi-node LangGraph agent** that:

- **Routes** queries intelligently: RAG / Web Search / Direct Answer / Small Talk
- **Judges** if retrieved knowledge is sufficient using an LLM-as-a-judge pattern
- **Falls back** to live web search when the knowledge base isn't enough
- **Maintains** conversation memory across sessions

---

## ✨ Features

- 📄 PDF upload → auto-chunked → embedded → stored in Pinecone
- 🧭 Intelligent router with 4 route types
- ⚖️ RAG sufficiency judge (LLM-as-a-judge)
- 🌐 Web search fallback via Tavily
- 💾 Per-session conversation memory
- 🔘 Toggle web search on/off from the UI
- 📊 Analytics dashboard (queries, RAG hit rate, avg response time)
- 🔬 Agent workflow trace panel
- 🐳 Fully containerized with Docker
- 🚀 Production deployed (not just localhost)

---

## 🗂️ Project Structure

```
DEPLOY_AGENTIC_RAG/
├── backend/
│   ├── agent.py          # LangGraph multi-node agent
│   ├── analytics.py      # SQLite analytics logger
│   ├── config.py         # Environment config
│   ├── main.py           # FastAPI app & endpoints
│   ├── vectorstore.py    # Pinecone vector store
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py            # Streamlit main app
│   ├── dashboard.py      # Analytics dashboard
│   ├── ui_component.py   # UI components
│   ├── backend_api.py    # API client
│   ├── session_manager.py
│   ├── config.py
│   ├── Dockerfile
│   └── requirements.txt
├── data/
│   └── shopnova_knowledge_base.pdf
├── .env.example
└── .gitignore
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4 Turbo |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | Pinecone (Serverless) |
| Web Search | Tavily Search API |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Charts | Plotly |
| Analytics | SQLite |
| PDF Parsing | PyPDFLoader |
| Containers | Docker |
| Backend Deploy | Railway |
| Frontend Deploy | Streamlit Cloud |

---

## 🚀 Agent Flow

```
User Query
    ↓
Router LLM
    ↓           ↓            ↓           ↓
RAG Lookup  Web Search  Direct Answer  End (small talk)
    ↓
Judge LLM (sufficient?)
    ↓              ↓
Answer Node    Web Search fallback
    ↓
Final Response → User
```

---

## 🛠️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/shopnova-agentic-rag.git
cd shopnova-agentic-rag
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX=deploy-agentic-rag
TAVILY_API_KEY=tvly-...
OPENAI_EMBED_MODEL=text-embedding-3-small
DOC_SOURCE_DIR=data
```

### 3. Run the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Run the frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🐳 Docker

```bash
# Backend
cd backend
docker build -t shopnova-backend .
docker run -p 8000:8000 --env-file ../.env shopnova-backend

# Frontend
cd frontend
docker build -t shopnova-frontend .
docker run -p 8501:8501 shopnova-frontend
```

---

## ☁️ Deployment

### Backend → Railway

1. Connect your GitHub repo to Railway
2. Set root directory to `backend/`
3. Set start command:
```
sh -c "cd backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
```
4. Add all environment variables from `.env` to Railway dashboard

### Frontend → Streamlit Cloud

1. Connect your GitHub repo to Streamlit Cloud
2. Set main file path to `frontend/app.py`
3. Add in Secrets:
```
FASTAPI_BASE_URL = "https://your-backend-url.railway.app"
```

---

## 📊 Analytics Dashboard

The dashboard tracks:
- Total queries
- RAG hit rate vs Web search usage
- Average response time
- Recent query history

Data is persisted in SQLite (`analytics.db`) and exposed via `/analytics/` endpoint.

---

## 📁 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/` | Send a message to the agent |
| POST | `/upload-document/` | Upload a PDF to the knowledge base |
| GET | `/analytics/` | Get usage analytics |
| GET | `/health` | Health check |

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX` | Pinecone index name |
| `TAVILY_API_KEY` | Tavily Search API key |
| `OPENAI_EMBED_MODEL` | Embedding model name |
| `FASTAPI_BASE_URL` | Backend URL (frontend only) |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT

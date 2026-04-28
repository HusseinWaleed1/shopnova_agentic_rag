import os
from dotenv import load_dotenv
load_dotenv()

# vectore database

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_INDEX=os.getenv("PINECONE_INDEX","deploy-agentic-rag")

# OpenAI
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Tavily
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

# Embedding Model
OPENAI_EMBED_MODEL=os.getenv("OPENAI_EMBED_MODEL","text-embedding-3-small")


# paths (adjust as needed)
DOC_SOURCE_DIR=os.getenv("DOC_SOURCE_DIR","data")

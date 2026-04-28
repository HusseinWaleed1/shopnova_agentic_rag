import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone,ServerlessSpec

from config import PINECONE_API_KEY, PINECONE_INDEX, OPENAI_EMBED_MODEL
# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
# Initialize embeddings once (reused everywhere)
embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL)


def _get_or_create_index():
    """Ensures the Pinecone index exists, creates it if not."""
    if PINECONE_INDEX not in pc.list_indexes().names():
        print(f"Creating new Pinecone index: {PINECONE_INDEX}...")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print(f"Created index: {PINECONE_INDEX}")

def _get_vectorstore() -> PineconeVectorStore:
    """Returns a PineconeVectorStore instance."""
    _get_or_create_index()
    return PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embeddings)
# retriever function
def get_retriever():
    """Returns the Pinecone vector store retriever."""
    return _get_vectorstore().as_retriever()

def add_document_to_vectorstore(text_content: str):
    """Splits and adds a text document to the Pinecone vector store."""
    if not text_content:
        raise ValueError("Document content cannot be empty.")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    documents = text_splitter.create_documents([text_content])
    print(f"Splitting document into {len(documents)} chunks for indexing...")
    
    _get_vectorstore().add_documents(documents)
    print(f"Successfully added {len(documents)} chunks to '{PINECONE_INDEX}'.")
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from app.config import MISTRAL_API_KEY

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def build_vector_store():
    # Only try to build if there is a key, otherwise return None (for testing/mocking)
    if not MISTRAL_API_KEY or MISTRAL_API_KEY == "your_mistral_api_key_here":
        return None
        
    policy_path = os.path.join(DATA_DIR, "policies.md")
    
    headers_to_split_on = [
        ("##", "Rule"),
        ("###", "Condition"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    with open(policy_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    md_header_splits = markdown_splitter.split_text(md_text)
    
    try:
        embeddings = MistralAIEmbeddings(mistral_api_key=MISTRAL_API_KEY)
        vectorstore = FAISS.from_documents(md_header_splits, embeddings)
    except Exception:
        return None
    
    return vectorstore

def search_policy(query: str, k: int = 2) -> str:
    vectorstore = build_vector_store()
    if not vectorstore:
        with open(os.path.join(DATA_DIR, "policies.md"), "r", encoding="utf-8") as f:
            return f.read()
        
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    return "\n\n".join([doc.page_content for doc in docs])

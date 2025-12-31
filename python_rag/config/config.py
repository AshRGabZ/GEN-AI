"""
Configuration settings for the RAG chatbot.
Contains API keys, database URIs, model names, and other constants.
"""

# API Configuration
ANTHROPIC_API_KEY = "<ANTHROPIC_API_KEY>"
MODEL_NAME = "claude-sonnet-4-5-20250929"

# Database Configuration
MONGODB_URI = "mongodb://admin:admin@localhost:27017"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "learning_rag"

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# RAG Configuration
SIMILARITY_SEARCH_K = 3  # Number of documents to retrieve
SIMILARITY_THRESHOLD = 0.75  # Threshold for query validation

# Prompt Templates
SYSTEM_PROMPT_TEMPLATE = """Answer the question using the context below.

Context:
{context}

IMPORTANT Instructions:
1. You MUST use the tools to format your final answer.
2. In your answer, ALWAYS include the source information (File Location and Page number) from the context.
3. Format it like: 'Source: [File Location], Page [Page number]'
4. Pass your complete answer WITH source information as the msg parameter to the tool.
"""

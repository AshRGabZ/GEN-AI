# Python RAG Chatbot

A Retrieval Augmented Generation (RAG) chatbot that answers questions about Python programming using LangGraph, Anthropic Claude, and Qdrant vector database.

## Project Structure

```
python_rag/
├── __init__.py                      # Package initialization
├── main.py                          # Main entry point for the chatbot
├── run.py                           # Convenience script to run the chatbot
├── README.md                        # Project documentation
│
├── config/                          # Configuration and constants
│   ├── __init__.py
│   └── config.py                    # API keys, database URIs, model settings
│
├── tools/                           # Tool definitions for LLM
│   ├── __init__.py
│   └── tools.py                     # Message formatting tools (beginner/advanced)
│
├── graph/                           # LangGraph workflow components
│   ├── __init__.py
│   ├── state.py                     # State definition for the graph
│   ├── nodes.py                     # Node functions (validate, retrieve, agent, etc.)
│   └── workflow.py                  # Graph structure and edge definitions
│
├── vector_db/                       # Vector database operations
│   ├── __init__.py
│   └── push_to_vector_db.py        # Script to index documents into Qdrant
│
└── utils/                           # Utility functions
    ├── __init__.py
    └── chat_interface.py            # Chat loop and user interaction utilities
```

## Features

- **RAG Pipeline**: Retrieves relevant context from a vector database before generating responses
- **Query Validation**: Validates if questions are related to Python programming
- **Adaptive Responses**: Formats answers for beginner or advanced users using specialized tools
- **Conversation History**: Maintains chat history using MongoDB checkpointer
- **Source Attribution**: Includes source file location and page numbers in responses

## Setup

1. **Install Dependencies**:
   ```bash
   pip install langchain langchain-community langchain-qdrant langchain-huggingface
   pip install anthropic langgraph pymongo qdrant-client
   ```

2. **Start Required Services**:
   - MongoDB (for conversation history)
   - Qdrant (for vector database)

3. **Index Documents**:
   ```bash
   cd python_rag/vector_db
   python push_to_vector_db.py
   ```

4. **Run the Chatbot**:
   
   Option 1 - Using the run script (recommended):
   ```bash
   cd python_rag
   python run.py
   ```
   
   Option 2 - Direct execution:
   ```bash
   cd python_rag
   python main.py
   ```

## Configuration

Edit [`config/config.py`](config/config.py) to update:
- API keys (Anthropic)
- Database URIs (MongoDB, Qdrant)
- Model names and parameters
- RAG settings (similarity threshold, number of documents to retrieve)

## Workflow

1. **Validate Query**: Checks if the question is related to Python programming
2. **Retrieve Context**: Fetches relevant documents from the vector database
3. **Generate Answer**: Uses Claude with retrieved context to generate a response
4. **Format Response**: Applies beginner or advanced formatting based on user level
5. **Return Result**: Displays the formatted answer with source attribution

## Tools

- **modify_message_for_beginner**: Simplifies responses for beginners
- **modify_message_for_advanced**: Provides in-depth technical responses for experts

## Notes

- Update the API key in [`config/config.py`](config/config.py) before running
- Ensure MongoDB and Qdrant are running before starting the chatbot
- The vector database must be populated with documents before use

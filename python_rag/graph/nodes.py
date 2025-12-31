"""
Node functions for the LangGraph workflow.
Each node represents a step in the RAG pipeline.
"""

import anthropic
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

from graph.state import State
from config import (
    ANTHROPIC_API_KEY,
    MODEL_NAME,
    QDRANT_URL,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    SIMILARITY_SEARCH_K,
    SYSTEM_PROMPT_TEMPLATE,
)
from tools import TOOLS


# Initialize clients and models
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name=QDRANT_COLLECTION_NAME
)

llm = init_chat_model(model=MODEL_NAME, model_provider="anthropic", api_key=ANTHROPIC_API_KEY)
llm_with_tools = llm.bind_tools(TOOLS)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_TEMPLATE),
    ("placeholder", "{messages}"),
    ("human", "{input}")
])


def validate_user_query(state: State) -> dict:
    """Validate if the user query is related to Python programming."""
    user_query = state["user_query"]

    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": (
                    "Answer only Yes or No.\n"
                    "Is the following question related to Python programming?\n\n"
                    f"Question: {user_query}"
                )
            }
        ],
    )

    raw_msg = message.content[0].text.strip().lower()
    is_valid = raw_msg.startswith("yes")

    return {"is_valid_query": is_valid}


def retrieve_node(state: State) -> dict:
    """Retrieve relevant documents from the vector database."""
    docs = vector_db.similarity_search(
        query=state["user_query"],
        k=SIMILARITY_SEARCH_K
    )

    context = "\n\n".join(
        f"""page content: {d.page_content}\n File Location: {d.metadata["source"]}\n Page number: {d.metadata["page"]}"""
        for d in docs
    )

    return {"retrieved_context": context}


def agent_node(state: State) -> dict:
    """Generate response using the LLM with retrieved context."""
    chain = prompt | llm_with_tools

    response = chain.invoke({
        "input": state["user_query"],
        "context": state["retrieved_context"],
        "messages": state.get("messages", [])
    })

    return {"messages": [response]}


def invalid_query_response(state: State) -> dict:
    """Return a message for invalid queries."""
    return {
        "messages": [
            AIMessage(content="Sorry, your query is not relevant to Python programming. Please ask questions related to Python.")
        ]
    }


def route_after_validation(state: State) -> str:
    """Route based on query validation result."""
    return "valid" if state["is_valid_query"] else "invalid"


def route_after_answer(state: State) -> str:
    """Route based on whether tools need to be called."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

"""
State definitions for the LangGraph workflow.
"""

from typing import Annotated, Optional, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class State(TypedDict):
    """State object for the RAG chatbot graph."""
    user_query: str
    retrieved_context: Optional[str]
    messages: Annotated[List[BaseMessage], add_messages]
    is_valid_query: Optional[bool]
    conversation: Annotated[List[BaseMessage], add_messages]

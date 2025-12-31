"""
LangGraph workflow definition for the RAG chatbot.
Defines the graph structure and edges between nodes.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from graph.state import State
from graph.nodes import (
    validate_user_query,
    retrieve_node,
    agent_node,
    invalid_query_response,
    route_after_validation,
    route_after_answer,
)
from tools import TOOLS


def create_graph():
    """Create and configure the LangGraph workflow."""
    # Create the tool node that will automatically execute tools
    tool_node = ToolNode(TOOLS)

    # Initialize the graph
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("validate", validate_user_query)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("invalid_query_response", invalid_query_response)

    # Add edges
    graph.add_edge(START, "validate")

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "valid": "retrieve",
            "invalid": "invalid_query_response",
        }
    )

    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", "tools")
    
    # After tools are executed, END (don't loop back)
    graph.add_edge("tools", END)
    graph.add_edge("invalid_query_response", END)

    return graph

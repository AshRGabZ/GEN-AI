"""
Chat interface utilities for the RAG chatbot.
Handles user interaction and conversation flow.
"""

from langgraph.checkpoint.mongodb import MongoDBSaver
from config import MONGODB_URI


def run_chat_loop(compiled_graph):
    """
    Run the interactive chat loop with conversation history.
    
    Args:
        compiled_graph: The compiled LangGraph workflow
    """
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        compiled_graph_with_memory = compiled_graph.compile(checkpointer=checkpointer)
        
        # Get user's thread ID
        thread_id = input("Enter your name (for conversation history): ").strip() or "default_user"
        
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        
        print(f"\n🤖 Chat started! (thread_id: {thread_id})")
        print("Ask me anything about Python programming. Type 'exit', 'quit', or 'bye' to end.\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n👋 Goodbye! Your conversation history has been saved.")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            print("\n🤔 Processing...\n")
            
            # Invoke with only the new user query - checkpointer handles history
            result = compiled_graph_with_memory.invoke(
                {"user_query": user_input},
                config
            )
            
            # Print the final response
            if "messages" in result and result["messages"]:
                final_message = result["messages"][-1]
                if hasattr(final_message, 'content'):
                    print(f"Assistant: {final_message.content}\n")
            else:
                print("Assistant: No response generated.\n")
            
            print("-" * 50 + "\n")


def run_simple_chat(compiled_graph):
    """
    Run a simple chat loop without conversation history.
    
    Args:
        compiled_graph: The compiled LangGraph workflow
    """
    print("\n🤖 Chat started!")
    print("Ask me anything about Python programming. Type 'exit', 'quit', or 'bye' to end.\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Skip empty inputs
        if not user_input:
            continue
        
        print("\n🤔 Processing...\n")
        
        # Invoke with the user query
        result = compiled_graph.invoke({"user_query": user_input})
        
        # Print the final response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, 'content'):
                print(f"Assistant: {final_message.content}\n")
        else:
            print("Assistant: No response generated.\n")
        
        print("-" * 50 + "\n")

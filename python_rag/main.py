"""
Main entry point for the Python RAG Chatbot.
This chatbot answers questions about Python programming using RAG (Retrieval Augmented Generation).
"""

from langgraph.checkpoint.mongodb import MongoDBSaver
from graph import create_graph
from config import MONGODB_URI


def main():
    """Main function to run the RAG chatbot."""
    # Create the graph workflow
    graph = create_graph()
    
    # Compile the graph with MongoDB checkpointer for conversation history
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        compiled_graph = graph.compile(checkpointer=checkpointer)
        
        # Get user's thread ID for conversation history
        thread_id = input("Enter your name (for conversation history): ").strip() or "default_user"
        
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        
        print(f"\n🤖 Chat started! (thread_id: {thread_id})")
        print("Ask me anything about Python programming. Type 'exit', 'quit', or 'bye' to end.\n")
        
        # Main chat loop
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
            
            # Invoke the graph with the user query
            # The checkpointer automatically handles conversation history
            result = compiled_graph.invoke(
                {"user_query": user_input},
                config
            )
            
            # Print the final response
            if "messages" in result and result["messages"]:
                final_message = result["messages"][-1]
                if hasattr(final_message, 'content'):
                    print(f"Assistant Final Message:\n{final_message.content}\n")
            else:
                print("Assistant: No response generated.\n")
            
            print("-" * 50 + "\n")


if __name__ == "__main__":
    main()

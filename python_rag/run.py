#!/usr/bin/env python3
"""
Convenience script to run the Python RAG Chatbot.
This script can be run from anywhere and handles the import paths correctly.
"""

import sys
from pathlib import Path

# Add the parent directory to the Python path so imports work correctly
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Now import and run the main function
from python_rag.main import main

if __name__ == "__main__":
    main()

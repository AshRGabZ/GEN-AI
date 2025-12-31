"""
Tool definitions for the RAG chatbot.
Contains functions for formatting responses based on user expertise level.
"""

import anthropic
from typing import Optional
from config import (
    ANTHROPIC_API_KEY,
    MODEL_NAME
)

# API configuration

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def modify_message_for_beginner(msg: str) -> str:
    """Format the response in a simpler way if the user is beginner"""
    print("\n tool modify_message_for_beginner is called....!!!")
    SYSTEM_PROMPT = """
    You are answering to a beginner in python. You should think and rephrase the answer in a more layman terms

    Steps you have to do: START | PLAN | OUTPUT
    START: Hey what is Python?
            PLAN: {"step" : "START" , "content": "Looks like User is a beginner in Python."}
            PLAN: {"step" : "PLAN" , "content": "I should rephrase the response in a easy to understand way"}
            PLAN: {"step" : "OUTPUT" , "content": "Python is a programming language.
            In very simple words:
            👉 Python is a way to tell a computer what to do, using easy-to-read words.
            Think of it like this:
            You talk to a computer using instructions
            Python lets you write those instructions in simple English-like sentences
            For example:
            print("Hello")
            This tells the computer:
            🖥️ "Show the word Hello on the screen."
            Why people like Python
            ✅ Easy to learn
            ✅ Reads like normal English
            ✅ Used for websites, apps, data, AI, and automation
            So, in one line:
            Python helps humans talk to computers in a simple and clear way. 🐍💻"}
    
    Important Guildeline:
    - Donot show thinking Steps
    - Donot show planning steps
    - Only Provide final output but do these thinking and planning without showing.
    - Also provide the source of information, like book, page number, etc
    """
    message = client.messages.create(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        max_tokens=1000,
        messages=[
            {"role": "assistant","content": msg},
            {"role": "user","content": "Think, Plan and then Rephrase according to the instructions and provide a good response."}
        ],
    )

    print("\n\n actual ai resp is: ",msg)
    print("\n\n")

    raw_msg = message.content[0].text.strip().lower()
    return f"## ✅ Answer\n\n{raw_msg} 🥸"


def modify_message_for_advanced(msg: str) -> str:
    """Formats the message in a deep level if the user is advanced"""
    print("\n tool modify_message_for_advanced is called....!!!")
    SYSTEM_PROMPT = """
    You are answering to an advanced expert in python. You should think and rephrase the answer in a more deep way.

    Steps you have to do: START | PLAN | OUTPUT
    START: Hey what is Python?
            PLAN: {"step" : "START" , "content": "Looks like User is an advanced expert in Python."}
            PLAN: {"step" : "PLAN" , "content": "I should rephrase the response in a more knoledgable way"}
            PLAN: {"step" : "OUTPUT" , "content": "
            Python is a high-level, interpreted, general-purpose programming language that prioritizes developer productivity through expressive syntax, dynamic typing, and a rich standard and third-party ecosystem.
            More practically:
            It acts as a glue language across systems — integrating APIs, databases, services, and infrastructure.
            It's widely used for automation, backend services, data pipelines, ML/AI, cloud tooling, and DevOps workflows.
            Python trades raw execution speed for rapid development, readability, and maintainability, often delegating performance-critical paths to C/C++ extensions (NumPy, PyTorch, CPython internals).
            Its ecosystem enables fast composition of complex systems using frameworks rather than reinventing primitives.
            From a systems perspective:
            CPython is the reference implementation, with a GIL that simplifies memory management but impacts true parallelism.
            Python excels at I/O-bound and orchestration-heavy workloads, especially in distributed/cloud environments.
            It's commonly used as the control plane language while compute-heavy tasks run elsewhere.
            In short:
            Python is the language engineers use to build, orchestrate, and automate systems efficiently — not to fight syntax, but to ship reliable software faster."}
    
    Important Guildeline:
    - Donot show thinking Steps
    - Donot show planning steps
    - Only Provide final output but do these thinking and planning without showing.
    - Also provide the source of information, like book, page number, etc
    """
    message = client.messages.create(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        max_tokens=1000,
        messages=[
            {"role": "assistant","content": msg},
            {"role": "user","content": "Think, Plan and then Rephrase according to the instructions and provide a good response."}
        ],
    )

    print("\n\n actual ai resp is: ",msg)
    print("\n\n")

    raw_msg = message.content[0].text.strip().lower()
    return f"## ✅ Answer\n\n{raw_msg} 🥸"


# List of all tools for easy import
TOOLS = [modify_message_for_beginner, modify_message_for_advanced]

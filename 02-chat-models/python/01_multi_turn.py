"""
Lesson 02: Multi-Turn Conversation
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    """
    Main function to define multi-turn conversation.
    """
    print("Multi-Turn Conversation Example\n")
    
    # Create a chat model instance
    model = ChatOpenAI(
        model="deepseek-v4-pro",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )

    # Start with system message and first question
    messages = [
        SystemMessage(content="You are a helpful coding tutor who gives clear, concise explanations."),
        HumanMessage(content="What is Python?"),
    ]
    print("User: What is Python?")

    # First exchange
    response_1 = model.invoke(messages)
    print(f"\nAI: {response_1.content}")
    messages.append(AIMessage(content=str(response_1.content)))

    # Second exchange - AI remembers the context
    print("\nUser: Can you show me a simple example?")
    messages.append(HumanMessage(content="Can you show me a simple example?"))

    response_2 = model.invoke(messages)
    print(f"\nAI: {response_2.content}")
    messages.append(AIMessage(content=str(response_2.content)))

    # Third exchange - AI still remembers everything
    print("\nUser: What are the benefits compared to other languages?")
    messages.append(HumanMessage(content="What are the benefits compared to other languages?"))
    
    response_3 = model.invoke(messages)
    print(f"\nAI: {response_3.content}")
    print(f"Total messages in history: {len(messages)} messages, that include 1 system message, 3 human messages, and 2 AI messages.")
    
if __name__ == "__main__":
    main()

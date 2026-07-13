"""
Lesson 01 - Message Types in LangChain
This example demonstrates how to use different message types (SystemMessage, HumanMessage).
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    """
    Main function to use system message and human message.
    """
    print("Understanding Message Types.\n")

    model = ChatOpenAI(
        model="deepseek-v4-pro", # or deepseek-v4-flash for faster response
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    # Using structured messages for better control
    messages = [
        SystemMessage(content="You are a helpful AI assistant who explains things simply."),
        HumanMessage(content="Explain quantum computing to a 10-year-old.")
    ]
    response = model.invoke(messages)

    print("AI Response: \n")
    print(response.content)
    print("\nNotice how the SystemMessage influenced the response style!")

if __name__ == "__main__":
    main()
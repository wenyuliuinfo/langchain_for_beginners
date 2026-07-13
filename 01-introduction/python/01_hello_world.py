"""
Lesson 01 - Hello World with LangChain.
This example demonstrates a basic LLM call using ChatOpenAI.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    """
    Main function to call the LLM model.
    """
    print("Hello LangChain!")

    model = ChatOpenAI(
        model="deepseek-v4-pro", # or deepseek-v4-flash for faster option
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )

    # Make the first AI call
    response = model.invoke("What is LangChain in one sentence?")
    print("AI Response:", response.content)
    print("Success! You just made your first LangChain call!")

if __name__ == "__main__":
    main()
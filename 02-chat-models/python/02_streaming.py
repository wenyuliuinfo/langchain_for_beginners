"""
Lesson 02 - Streaming Response
"""

import os
import sys
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def non_streaming_example():
    """
    Function to demo non-streaming chat.
    """
    print("Non-Streaming (traditional way): \n")
    
    model = ChatOpenAI(
        model="deepseek-v4-pro",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    start_time = time.time()
    response = model.invoke("Explain how the internet work in 2 paragraphs.")
    end_time = time.time()

    print(response.content)
    elapsed_ms = (end_time - start_time) * 1000
    print(f"\n  Received after: {elapsed_ms:.0f}ms\n")

def streaming_example():
    """
    Function to demo streaming chat.
    """
    print("\n" + "=" * 80)
    print("AI (streaming):")

    model = ChatOpenAI(
        model="deepseek-v4-pro",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    start_time = time.time()
    first_chunk_time = 0
    
    for chunk in model.stream("Explain how the internet works in 2 paragraphs."):
        if first_chunk_time == 0:
            first_chunk_time = time.time()
        print(chunk.content, end="", flush=True)
   
    print("\n\nStream complete!")
    end_time = time.time()

    print(f"\nFirst chunk arrived: {(first_chunk_time - start_time) * 1000:.0f}ms")
    print(f"Stream completed: {(end_time - start_time) * 1000:.0f}ms")
    print("\nNotice how streaming feels more responsive!")

def main():
    print("Comparing Streaming vs. Non-Streaming\n")
    print("=" * 80)

    non_streaming_example()
    streaming_example()

if __name__ == "__main__":
    main()
    
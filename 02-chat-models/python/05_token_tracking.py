"""
Lesson 02 - Token Usage Tracking Example
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def track_token_usage():
    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    print("Token Usage Tracking Example\n")
    response = model.invoke("Explain what Python is in 2 sentences.")
    usage = response.usage_metadata

    if usage:
        print("Token Breakdown:")
        print(f"  Prompt tokens:        {usage.get('input_tokens', 'N/A')}")
        print(f"  Completion tokens:    {usage.get('output_tokens', 'N/A')}")
        print(f"  Total tokens:         {usage.get('total_tokens', 'N/A')}")
    else:
        print("Token usage information not available in response metadata.")

    print("\nResponse:")
    print(response.content)

if __name__ == "__main__":
    track_token_usage()
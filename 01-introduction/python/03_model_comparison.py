"""
Lesson 01 - Model Comparison in LangChain
This example shows how to compare different AI models.
"""

import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    """
    Main function to compare different models.
    """
    print("Comparing AI Models\n")
    
    prompt = "Explain recursion in programming in one sentence."
    models = ["deepseek-v4-pro", "deepseek-v4-flash"]

    for model_name in models:
        print(f"\nTesting model: {model_name}")
        print("-"*50)

        model = ChatOpenAI(
            model=model_name,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        start_time = time.time() 
        response = model.invoke(prompt)
        duration = (time.time() - start_time) * 1000

        print(f"Response: {response.content}")
        print(f"  Time: {duration:.0f}ms")

    print("\nComparison complete!")
    print("\nKey Observations: ")
    print("  - deepseek-v4-pro is more capable and detailed")
    print("  - deepseek-v4-flash is faster and uses fewer resources")
    print("  - Choose based on your needs: speed vs. capability")

if __name__ == "__main__":
    main()
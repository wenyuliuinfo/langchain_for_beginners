"""
Lesson 02 - Model Parameters
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def temperature_comparison():
    """
    Function to compare different temperatures.
    """
    model_name = "deepseek-v4-pro"
    prompt = "Write a creative opening line for a sci-fi story about time traveling."
    temperatures = [0, 1]
    tries = 1

    for temp in temperatures:
        print(f"\nTemperature: {temp}")
        print("-" * 80)

        model = ChatOpenAI(
            model=model_name,
            temperature=temp,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        try:
            for i in range(1, tries+1):
                response = model.invoke(prompt)
                print(f"  Try {i}: {response.content}")
        except Exception as error:
            error_msg = str(error)
            if "temperature" in error_msg.lower():
                print(f"This model does not support temperature={temp}. Skipping...")
                print(f"Error: {error_msg}")
            else:
                raise

    print("\nGeneral Temperature Guidelines:")
    print("  - Lower values (0-0.3): More deterministic, consistent responses.")
    print("  - Medium values (0.7-1.0): Balanced creativity and consistency.")
    print("  - Higher values (1.5-2.0): More creative and varied response.")

def max_tokens_example():
    """
    Function to text with max token setup.
    """
    print("\n\nMax Tokens Limit\n")
    print("=" * 80)

    model_name = "deepseek-v4-flash"
    prompt = "Write a detailed explanation of machine learning in 5 paragraphs."
    token_limits = [800, 1500]

    for max_tokens in token_limits:
        print(f"\nMax Tokens: {max_tokens}")
        print("-" * 80)

        model = ChatOpenAI(
            model=model_name,
            max_tokens=max_tokens,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        try:
            response = model.invoke(prompt)
            print(response.content)
            print(f"\n (Character count: {len(response.content)})")
        except Exception as error:
            error_msg = str(error)
            if "max_tokens" in error_msg.lower():
                print(f"This model does not support max_tokens={max_tokens}. Skipping...")
                print(f"Error: {error_msg}")
            else:
                raise

    print("\nObservation:")
    print("  - Lower max tokens = shorter responses.")
    print("  - Response may be cut off if limit is too low.")
    print("  - Use max tokens to control costs and response length.")

def main():
    print("Model Parameters Tutorial\n")
    temperature_comparison()
    max_tokens_example()

    print("\n\nSummary: ")
    print("  - Lower temperatures: Consistent, factual responses.")
    print("  - Higher temperatures: Creative, varied responses.")
    print("  - Always check your model's supported parameter ranges.")

if __name__ == "__main__":
    main()
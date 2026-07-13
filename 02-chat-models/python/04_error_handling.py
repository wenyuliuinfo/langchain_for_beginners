"""
Lesson 02 - Error Handling with Built-in Retries
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def robust_call(prompt: str, max_retries: int=3) -> str:
    """
    Makes an API call with automatic retry logic using LangChain's built-in with_retry().
    """
    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    # Use LangChain's built-in retry logic
    model_with_retry = model.with_retry(stop_after_attempt=max_retries)
    print(f"Making calls with automatic retry {max_retries} attempts...")
    response = model_with_retry.invoke(prompt)
    print("Success!")

    return str(response.content)

def error_examples():
    """
    Demonstrates different error scenarios.
    """
    print("Error Handling Examples\n")
    print("=" * 80)
    model_name = "deepseek-v4-flash"
    
    # Example 1: Invalid API key
    print("\n1. Example: Invalid API Key\n")
    try:
        bad_model = ChatOpenAI(
            model=model_name,
            api_key="invalid_key",
            base_url=DEEPSEEK_BASE_URL
        )
        print("Attempting call with invalid API key...")
        bad_model.invoke("Hello!")
    except Exception as error:
        error_msg = str(error)[:100] + "..." if len(str(error)) > 100 else str(error)
        print(f"Caught error: {error_msg}")

    # Example 2: Normal with_retry() usage
    print("\n2. Example: Using with_retry() with Valid Credentials\n")
    try:
        response = robust_call("What is 5+5?")
        print(f"Response: {response}")
        print("No retries needed when everything works correctly.\n")
    except Exception as error:
        print(f"All retries failed: {error}")

    # Example 3: Error categorization
    print("\n3. Example: Categorizing Different Error Types\n")
    try:
        bad_model = ChatOpenAI(
            model=model_name,
            api_key="invalid_key",
            base_url=DEEPSEEK_BASE_URL
        )
        print("Testing error categorization with invalid API key...")
        bad_model.invoke("Hello!")
    except Exception as error:
        error_msg = str(error).lower()
        error_type = "Unknown error"
        solution = "Check the error message for details."
        
        if "401" in error_msg or "unauthorized" in error_msg or "invalid" in error_msg:
            error_type = "Authentication Error (401)"
            solution = "Verify your API key is correct."
        elif "429" in error_msg or "rate limit" in error_msg:
            error_type = "Rate Limit Error (429)"
            solution = "Use with_retry() to handle rate limits automatically."
        elif "timeout" in error_msg:
            error_type = "Timeout Error"
            solution = "Increase timeout or use with_retry()."

        print(f"Error type detected: {error_type}")
        print(f"Solution: {solution}")

def show_best_practices():
    """
    Best practices for error handling.
    """
    print("\n\nError Handling Best Practices\n")
    print("=" * 80)

    print("""
    1. Always wrap API calls in try-except.
    2. Use built-in retry logic with with_retry().
    3. Handle specific error types.
    4. Log errors for debugging.
    5. Provide helpful error messages to users.
    6. Have fallback behavior.
    7. Monitor error rates in production.
    """)

def main():
    error_examples()
    show_best_practices()
    print("\nRemember: Good error handling makes your app reliable!")

if __name__ == "__main__":
    main()
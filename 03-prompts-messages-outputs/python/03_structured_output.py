"""
Lesson 03 - Structured Output Example
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, EmailStr, Field

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

class Person(BaseModel):
    """
    Information about a person.
    """
    name: str = Field(description="The person's full name. Combine first and last names if separate.")
    age: int = Field(description="The person's age in years.")
    email: str = Field(description="The person's email address.")
    occupation: str = Field(description="The person's job or profession. Use this exact field name, not 'profession' or 'job'.")

def main():
    print("Structured Output Example\n")

    model_name = "deepseek-v4-pro"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    structured_model = model.with_structured_output(Person, method="json_mode")
    print("Testing with different inputs:\n")
    print("=" * 80)

    # Test 1: Complete information
    print("\n1. Complete Information:\n")
    result_1 = structured_model.invoke(
        "Extract the person's information from the text and return valid JSON."
        "My name is Alice Johnson, I'm 28 years old, work as a software engineer, and you can reach me at alice.j@email.com"
    )

    print("Structured Output (typed):")
    print(result_1.model_dump_json(indent=2))
    print("\nType-safe field access:")
    print(f"  Name: {result_1.name}")
    print(f"  Age:  {result_1.age} years old")
    print(f"  Email: {result_1.email}")
    print(f"  Occupation: {result_1.occupation}")

    # Test 2: Casual conversation
    print("\n" + "=" * 80)
    print("\n2. From Casual Conversation:\n")
    result_2 = structured_model.invoke(
        "Extract the person's information from the text and return valid JSON."
        "Hey! I'm Bob, a 35-year-old data scientist. You can email me at bob.smith@company.com"
    )
    print("Extracted Data:")
    print(result_2.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
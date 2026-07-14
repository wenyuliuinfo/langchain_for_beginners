"""
Lesson 03 - Multiple Template Formats
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    print("Template Formats Example\n")
    print("=" * 80)

    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )

    # Format 1: ChatPromptTemplate (structured messages)
    print("\n1. ChatPromptTemplate (Recommended for chat models):\n")
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a {role} who speaks in {style} style."),
        ("human", "{question}"),
    ])
    chain_1 = chat_template | model
    result_1 = chain_1.invoke({
        "role": "pirate captain",
        "style": "dramatic and adventurous",
        "question": "What is Python?",
    })
    print("Pirate response:")
    print(result_1.content)

    # Format 2: PromptTemplate (simple string-based)
    print("\n" + "=" * 80)
    print("\n2. PromptTemplate (simple string format): \n")
    string_template = PromptTemplate.from_template(
        "Write a {adjective} {item} about {topic}."
    )
    formatted_prompt = string_template.format(
        adjective="funny",
        item="limerick",
        topic="Python developers",
    )

    print("Generated prompt:", formatted_prompt)
    result_2 = model.invoke(formatted_prompt)
    print("\nResponse:")
    print(result_2.content)

if __name__ == "__main__":
    main()
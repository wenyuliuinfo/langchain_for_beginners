"""
Lesson 03 - Messages vs. Templates - Understanding the Two Paradigms
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def main():
    print("Messages vs. Templates: Two Approaches\n")
    print("=" * 80)
        
    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    # Approach 1: Messages
    print("\nAPPROACH 1: Message Arrays\n")
    messages = [
        SystemMessage(content="You are a helpful translator."),
        HumanMessage(content="Translate 'Hello, World!' to French."),
    ]
    print("Message Structure:")
    for i, msg in enumerate(messages):
        print(f"  {i+1}. {msg.type}:\"{msg.content}\"")
    
    message_response = model.invoke(messages)
    print(f"\nResponse: {message_response.content}\n")

    # Approach 2: Templates (classic approach)
    print("=" * 80)
    print("\nAPPROACH 2: Templates\n")
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful translator."),
        ("human", "Translate {text} to {language}"),
    ])
    template_chain = template | model
    template_response = template_chain.invoke({
        "text": "Hello, world!",
        "language": "French",
    })
    print(f"Response: {template_response.content}\n")

if __name__ == "__main__":
    main()
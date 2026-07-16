"""
Lesson 04 - Multiple Tools
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
SERP_API_KEY = os.getenv("SERP_API_KEY")

class CalculatorInput(BaseModel):
    """
    Input for calculator.
    """
    expression: str = Field(description="Math expression to evaluate")

class SearchInput(BaseModel):
    """
    Input for search.
    """
    query: str = Field(description="Search query")

class WeatherInput(BaseModel):
    """
    Input for weather.
    """
    city: str = Field(description="City name")

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error occurred: {e}"

@tool(args_schema=SearchInput)
def search(query: str) -> str:
    """
    Look up factual information on the internet. 
    Use for: geography (capitals, countries, cities), 
    historical facts, current events, definitions, 
    biographies, or verifying information.
    """
    params = {
        "q": query,
        "location": "China",
        "hl": "en",
        "gl": "cn",
        "api_key": SERP_API_KEY
    }
    # Create the search object and execute it
    search = GoogleSearch(params)
    results = search.get_dict()

    # Check for feature snippet first
    if "featured_snippet" in results:
        snippet = results["featured_snippet"]["snippet"]
    elif results.get("organic_results"):
        snippet = results["organic_results"][0]["snippet"]

    return snippet

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    """
    params = {
        "q": "What is temperature for city: " + city,
        "location": "China",
        "hl": "en",
        "gl": "cn",
        "api_key": SERP_API_KEY
    }
    # Create the search object and execute it
    search = GoogleSearch(params)
    results = search.get_dict()

    # Check for feature snippet first
    if "featured_snippet" in results:
        snippet = results["featured_snippet"]["snippet"]
    elif results.get("organic_results"):
        snippet = results["organic_results"][0]["snippet"]

    return f"Current temperature in {city}: {snippet}"

def main():
    print("Multiple Tools Demo\n")
    print("=" * 80 + "\n")

    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    model_with_tools = model.bind_tools([calculator, search, get_weather])

    system_prompt = ("""
        You are a helpful assistant with access to tools. For any questions about facts,
        geography, history, current information, or general knowledge, you MUST use the 
        appropriate tool rather than answering from your training data.
    """)
    queries = [
        "What is 125*8?",
        "What's the capital of France?",
        "What's the weather in Tokyo?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        response = model_with_tools.invoke(messages)
        if response.tool_calls and len(response.tool_calls) > 0:
            tool_call = response.tool_calls[0]
            print(f"  Choose tool: {tool_call["name"]}")
            print(f"  Args: {tool_call["args"]}")
        else:
            print("  No tool call generated.")
        print("-" * 80)

if __name__ == "__main__":
    main()
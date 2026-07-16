"""
Lesson 04 - Complete Tool Execution Loop
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
SERP_API_KEY = os.getenv("SERP_API_KEY")

class WeatherInput(BaseModel):
    """
    Input for Weather Tool.
    """
    city: str = Field(description="City name.")

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
    print("Complete Tool Execution Loop\n")
    print("="*80 + "\n")

    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    model_with_tools = model.bind_tools([get_weather])
    query = "What's the weather in London?"
    print(f"User: {query}\n")

    # --- STEP 1. LLM GENERATES TOOL CALL (Planning) ---
    print("=== STEP 1: LLM GENERATES TOOL CALL ===")
    print("(The LLM's role: Planning - decides what to do)\n")

    response_1 = model_with_tools.invoke([HumanMessage(content=query)])
    if not response_1.tool_calls or len(response_1.tool_calls) == 0:
        print("No tool calls generated")
        return
    
    tool_call = response_1.tool_calls[0]
    print("LLM decided to call:", tool_call["name"])
    print("  With arguments:", tool_call["args"])
    print("  Tool call ID:", tool_call["id"])
    print("\nNote: The LLM only describe what to do - it didn't execute anything!\n")

    # --- STEP 2. YOUR CODE EXECUTES THE TOOL (Doing) ---
    print("=== STEP 2: YOUR CODE EXECUTES THE TOOL ===")
    print("(Your code's role: Doing - actually performs the action)\n")

    tool_result = get_weather.invoke(tool_call["args"])
    print("Tool executed successfully!")
    print("  Real result:", tool_result)
    print("\nNote: This is where the actual API call happens!\n")

    # --- STEP 3. SEND RESULTS BACK TO LLM (Communicating) ---
    print("=== STEP 3: SEND RESULTS BACK TO LLM ===")
    print("(The LLM's role: Communicating - converts data to natural language)\n")
    
    messages = [
        HumanMessage(content=query),
        AIMessage(content=str(response_1.content), tool_calls=response_1.tool_calls),
        ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]),
    ]
    final_response = model.invoke(messages)
    print("LLM generated final response:")
    print(" ", final_response.content)

if __name__ == "__main__":
    main()

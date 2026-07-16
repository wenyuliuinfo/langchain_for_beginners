"""
Lesson 05 - Agent with Checkpointer for Memory

Use checkpointers for:
- Maintaining conversation history
- Enabling multi-turn conversations
- Persisting agent state between calls
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
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

def main():
    print("Agent with Memory (Checkpointer) Example\n")
    print("=" * 80 + "\n")

    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    
    # Create a memory saver for conversation persistence
    memory = MemorySaver()

    # Create agent with checkpointer for memory
    agent = create_agent(
        model,
        tools=[calculator, search],
        checkpointer=memory,
    )

    # Configuration for this conversation thread
    config = {"configurable": {"thread_id": "user-1"}}
    system_prompt = ("""
        You are a helpful assistant with access to tools. For any questions about facts,
        geography, history, current information, or general knowledge, you MUST use the 
        appropriate tool rather than answering from your training data.
    """)

    print("Test 1: First calculation")
    print("-" * 80)
    query_1 = "What is 25*8?"
    print(f"User: {query_1}\n")
    messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query_1)
    ]
    response_1 = agent.invoke({"messages": messages}, config)
    last_response_1 = response_1["messages"][-1]
    print(f"Agent: {last_response_1.content}\n\n")

    print("Test 2: Follow-up question (agent remembers context)")
    print("-" * 80)
    query_2 = "Now multiply that result by 2."
    print(f"User: {query_2}\n")
    messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query_2)
    ]
    response_2 = agent.invoke({"messages": messages}, config)
    last_response_2 = response_2["messages"][-1]
    print(f"Agent: {last_response_2.content}\n\n")

    print("Test 3: Another follow-up")
    print("-" * 80)
    query_3 = "What was my original calculation?"
    print(f"User: {query_3}\n")
    messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query_3)
    ]
    response_3 = agent.invoke({"messages": messages}, config)
    last_response_3 = response_3["messages"][-1]
    print(f"Agent: {last_response_3.content}\n\n")

if __name__ == "__main__":
    main()
"""
Lesson 05 - Create agent with Middleware

Middleware can intercept and modify agent behavior at various stages:
- before_model: Before each LLM call
- after_model: After each LLM response
- wrap_model_call: Around each LLM call
- wrap_tool_call: Around each tool call
"""

import os

from typing import Any, Callable
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain.agents.middleware.types import ModelResponse
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
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
    if "error" in query.lower():
        return "Error: Search service temporarily unavailable."
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

# Middleware 1: Dynamic Model Selection
# Switches to a more capable model for complex conversations
class DynamicModelMiddleware(AgentMiddleware):
    """
    Switch to a more capable model for complex conversations.
    """
    def __init__(self, messages_threshold: int=10):
        super().__init__()
        self.messages_threshold = messages_threshold
        self._flash_model = ChatOpenAI(
            model="deepseek-v4-flash",
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            max_retries=1,
        )
        self._pro_model = ChatOpenAI(
            model="deepseek-v4-pro",
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            max_retries=1,
        )

    def wrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
        messages = request.state.get("messages", [])
        message_count = len(messages)
        print(f"  [Middleware] Message count: {message_count}")

        if message_count > self.messages_threshold:
            print("  [Middleware] Would switch to deepseek-v4-pro.")
            selected_model = self._pro_model
        else:
            print("  [Middleware] Use deepseek-v4-flash.")
            selected_model = self._flash_model
        request = request.override(model=selected_model)
        return handler(request)

# Middleware 2: Tool Error Handler
# Catches tool failures and provides helpful fallback messages
class ToolErrorMiddleware(AgentMiddleware):
    """
    Catch tool failures and provide graceful fallbacks.
    """
    def wrap_tool_call(self, request: Any, handler: Callable[[Any], ToolMessage]) -> ToolMessage:
        try:
            return handler(request)
        except Exception as e:
            tool_name = request.tool_call.get("name", "unknown")
            print(f"  [Middleware] Tool {tool_name} failed: {e}")
            return ToolMessage(
                content=f"I encountered an error while using the {tool_name} tool."
                        f"Let me try a different approach to answer your question.",
                        tool_call_id=request.tool_call.get("id", ""),
            )

def main():
    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        max_retries=1,
    )

    # Create agent with middleware
    agent = create_agent(
        model,
        tools=[calculator, search],
        middleware=[
            DynamicModelMiddleware(messages_threshold=10),
            ToolErrorMiddleware(),
        ],
    )
    system_prompt = ("""
        You are a helpful assistant with access to tools. For any questions about facts,
        geography, history, current information, or general knowledge, you MUST use the 
        appropriate tool rather than answering from your training data.
    """)

    # Test 1: Simple Calculation
    print("Test 1: Simple calculation")
    print("-" * 80)

    query_1 = "What is 25*8?"
    print(f"User: {query_1}\n")
    messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query_1)
    ]
    response_1 = agent.invoke({"messages": messages})
    last_response_1 = response_1["messages"][-1]
    print(f"Agent: {last_response_1.content}\n\n")

    # Test 2: Search with error handling (triggers error middleware)
    print("Test 2: Search with error handling")
    print("-" * 80)

    query_2 = "Search for information about error handling"
    print(f"User: {query_2}\n")
    messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query_2)
    ]
    response_2 = agent.invoke({"messages": messages})
    last_response_2 = response_2["messages"][-1]
    print(f"Agent: {last_response_2.content}\n\n")

     # Test 3: Search with more than threshold queries (triggers model selection middleware)
    print("Test 3: Search with more queries")
    print("-" * 80)

    queries = [
        "Tell me about LangChain.",
        "Tell me about LangGraph.",
        "Tell me about LangSmith."
    ]
    print(f"User: {queries}\n")
    messages = [
            SystemMessage(content=system_prompt)
    ]
    for query in queries:
        messages.append(HumanMessage(content=query))

    response_3 = agent.invoke({"messages": messages})
    last_response_3 = response_3["messages"]
    for m in last_response_3:
        m.pretty_print()

if __name__== "__main__":
    main()
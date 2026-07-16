"""
Lesson 04 - Binding and Invoking Tools
"""

import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

class CalculatorInput(BaseModel):
    """
    Input for Calculator.
    """
    expression: str = Field(description="Math expression to evaluate")

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

def main():
    print("Tool Calling Demo\n")
    print("=" * 80 + "\n")

    model_name = "deepseek-v4-flash"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    model_with_tools = model.bind_tools([calculator])
    print("Asking: What is 25 * 17? \n")

    # Invoke with a question
    response = model_with_tools.invoke("What is 25 * 17?")

    print("Response content:", response.content)
    print("\nTool calls:", json.dumps(
        [
            {"name": tc["name"], "args": tc["args"], "id": tc["id"]}
            for tc in response.tool_calls
        ] if response.tool_calls else [],
        indent=2,
    ))
    if response.tool_calls and len(response.tool_calls) > 0:
        print("\n" + "-" * 80)
        print("\nThe LLM generated a tool call!")
        print("Tool name:", response.tool_calls[0]["name"])
        print("Arguments:", response.tool_calls[0]["args"])
        print("Tool call ID:", response.tool_calls[0]["id"])

if __name__ == "__main__":
    main()
"""
Lesson 06 - Multi-Server MCP Integration

Servers used:
- Context7: Documentation tools (HTTP, remote)
- Local Calculator: Math tools (stdio, local subprocess)
"""

import asyncio
import os

from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

SCRIPT_DIR = Path(__file__).parent

async def main():
    print("Connecting to multiple MCP servers...\n")

    # Path to local calculator server
    server_path = SCRIPT_DIR / "servers" / "stdio_calculator_server.py"

    # Create MCP client connected to Multiple servers
    client = MultiServerMCPClient(
        {
            "context7": {
                "transport": "streamable_http",
                "url": "https://mcp.context7.com/mcp",
            },
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": [str(server_path)],
            },
        }
    )

    try:
        # 1. Get tools from all connected servers
        print("Fetching tools from all servers...")
        tools = await client.get_tools()
        print(f"Retrieved {len(tools)} total tools from 2 servers:\n")
        
        context7_tools = [t for t in tools if "library" in t.name or "resolve" in t.name]
        cal_tools = [t for t in tools if t.name in ("calculate", "convert_temperature")]

        print("From Context7 (Documentation)")
        for tool in context7_tools:
            print(f"  - {tool.name}: {tool.description}")

        print("From local calculator:")
        for tool in cal_tools:
            print(f"  - {tool.name}: {tool.description}")

        # 2. Create model
        model_name = "deepseek-v4-flash"
        model = ChatOpenAI(
            model=model_name,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

        # 3. Create agent with tools from all servers
        agent = create_agent(model, tools)

        # 4. Test 1: Agent use Calculator Tool
        print("Test 1: Math question (should use calculator)\n")
        math_query = "What is 24*4?"
        print(f"User: {math_query}")
    
        math_response = await agent.ainvoke({"messages": [("human", math_query)]})
        print(f"Agent: {math_response["messages"][-1].content}\n")

        # 5. Test 2: Agent use Context 7 Tool
        print("Test 2: Documentation question (should use Context7)\n")
        docs_query = "How do I use FastAPI to create REST API? Get documentation."
        print(f"User: {docs_query}")

        docs_response = await agent.ainvoke({"messages": [("human", docs_query)]})
        print(f"Agent: {docs_response["messages"][-1].content}\n")

        # 6. Test 3: Agent uses Both tools in sequence
        print("Test 3: Combined question (should use both tools)\n")
        combined_query = (
            "Calculate 15*8, then look up Python documentation about async/await if the result is greater than 100"
        )
        print(f"User: {combined_query}")
    
        combined_response = await agent.ainvoke({"messages": [("human", combined_query)]})
        print(f"Agent: {combined_response["messages"][-1].content}\n")

    except Exception as e:
        print(f"Error with multi-server MCP: {e}")
        if hasattr(e, "message"):
            print(f"  Message: {e.message}")

    finally:
        print("\nAll MCP connections closed.")

if __name__ == "__main__":
    asyncio.run(main())
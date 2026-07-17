"""
Lesson 06 - MCP Error Handling & Production Patterns
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load env variable for API Key
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

async def create_mcp_client_safely(config: dict) -> MultiServerMCPClient | None:
    """
    Utility: Safe MCP Client creation with error handling.
    """
    try:
        print("Attempting to connect to MCP server...")
        client = MultiServerMCPClient(config)
        tools = await client.get_tools()
        print(f"Connected! Retrieved {len(tools)} tools")
        return client
    except Exception as e:
        print(f"Failed to connect to MCP server: {e}")
        return None

async def check_mcp_health(client: MultiServerMCPClient) -> bool:
    """
    Check health of MCP server connection.
    """
    try:
        tools = await asyncio.wait_for(client.get_tools(), timeout=5.0)
        is_healthy = len(tools) > 0
        print("MCP server is healthy." if is_healthy else "MCP server returned no tools.")
        return is_healthy
    except asyncio.TimeoutError:
        print("MCP server is unhealthy: Health check timeout")
        return False
    except Exception as e:
        print(f"MCP server is unhealthy: {e}")
        return False

async def main():
    print("MCP Error Handling & Retry Patterns\n")

    # Pattern 1: Try primary server, fall back to alternative
    print("Pattern 1: Primary + Fallback Strategy\n")
    mcp_client: MultiServerMCPClient | None = None
    tools: list = []

    try:
        # Try Context7 server
        print("Trying primary server (Context7)...")
        mcp_client = await create_mcp_client_safely(
            {
                "context7": {
                    "transport": "streamable_http",
                    "url": "https://mcp.context7.com/mcp",
                }
            }
        )
        if not mcp_client:
            # If Context7 fails, you could fall back to alternative server
            print("\nPrimary failed, trying fallback server...")
            raise RuntimeError("No MCP servers available")

        # Get tools with error handling
        try:
            print("\nFetching tools from MCP server...")
            tools = await mcp_client.get_tools()
            print(f"Retrieved {len(tools)} tools successfully\n")
            for tool in tools:
                print(f"  - {tool.name}")
        except Exception as e:
            print(f"Failed to fetch tools: {e}")
            print("Fallback: Using empty tools array")
            tools = []

        # Pattern 2: Create Model with Built-in Retry Logic
        print("\n\nPattern 2: Using LangChain's Built-in Retry\n")
        if not tools:
            print("No tools available - agent will run without MCP tools.")
            print("This is graceful degradation - app continues to work!")
        model_name = "deepseek-v4-flash"
        model = ChatOpenAI(
            model=model_name,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
        # Wrap the model with retry functionality
        model_with_retry = model.with_retry(
            retry_if_exception_type=(Exception,),
            stop_after_attempt=3,
        )
        print("Model configured for agent use.")
        print("  - For retries, wrap agent.ainvoke() with tenacity or custom retry")
        print("  - LangChain's with_retry() works on individual model cells")
        # Use the wrapped model in the agent creation
        #agent = create_agent(model_with_retry, tools)
        agent = create_agent(model, tools)

        # Pattern 3: Execute with timeout and error handling
        print("\n\nPattern 3: Query Execution with Timeout\n")
        query = "How do I use Python's asyncio library? Get the latest documentation." 
        print(f"User: {query}")

        try:
            timeout_seconds = 30
            response = await asyncio.wait_for(
                agent.ainvoke({"messages": [("human", query)]}),
                timeout=timeout_seconds,
            )
            last_message = response["messages"][-1]
            print(f"Agent: {last_message.content}\n")
        except asyncio.TimeoutError:
            print("Query failed: Query timeout")
            print("Fallback: Providing cached/default response")
            print("Agent: I'm experiencing connectivity issues. Please try again later.")
        except Exception as e:
            print(f"Query failed: {e}")
            print("Fallback: Providing cached/default response")
            print("Agent: I'm experiencing connectivity issues. Please try again later.")    

        # Pattern 4: Health checks
        print("\nPattern 4: MCP Server Health Check\n")
        is_healthy = await check_mcp_health(mcp_client)
        print(f"\nHealth status: {'Healthy' if is_healthy else 'Unhealthy'}")

    except Exception as e:
        print(f"\nCritical error: {e}")
        print("In production, this would trigger alerts and fallback to cached data.")
    
    finally:
        if mcp_client:
            try:
                print("\nMCP Connection closed gracefully.")
            except Exception as e:
                print(f"Error closing MCP Connection: {e}")

if __name__ == "__main__":
    asyncio.run(main())
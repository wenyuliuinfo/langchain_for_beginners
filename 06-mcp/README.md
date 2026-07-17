# Model Context Protocol (MCP)
In this chapter, you'll learn how to connect AI agents to external services using the Model Context Protocol (MCP) - an open standard that provides a universal interface for AI applications to access tools and data source. You'll discover how MCP simplifies integration with services like GitHub, database, and documentation systems, and how to use MCP tools seamlessly with the agents you built.


## Model Context Protocol (MCP)
In previous lesson, you created tools (calculator, weather search) by writing the implementation code yourself. This works great for custom tools specific to your application.

But what about connecting to existing services or cases where tools need to be used across different AI applications? Imagine needing tools for:
- GitHub (create issues, search code, manage PRs)
- Calendar (check availability, create events)
- Your company database (query data, get schemas)
- Documentation systems (fetch docs, resolve references)

Writing custom integrations for each service means dealing with different APIs, authentication methods, and data formats. This is where Model Context Protocol (MCP) comes in.

### What is MCP?
**Model Context Protocol (MCP)** is an open standard that lets AI applications connect to external tools and data sources through a universal interface. It's like USB-C for AI applications.

**The Problem**: Building an AI assistant that needs to access Calendar details, databases, GitHub, and more means writing custom integrations for each service with different APIs, auth methods, and data formats.

**The MCP Solution**: Services expose their capabilities through a standard protocol. Your agent connects once and gets access to everything.

### Architecture
<img src="images/Screenshot 2026-07-17 at 7.15.26 AM.png" alt="MCP Architecture" width="600"/>

Each **MCP Server** is a program that exposes tools through the protocol. Your agent connects and can use all available tools.

### Transport Types
MCP defines two standard transport mechanisms for client-server communication:

| Transport | Communication Method | When to Use | Example |
| -------- | -------- | -------- | -------- | 
| Streamable HTTP | Network-based (client -> server over network) | When MCP server is accessed via URL | `{"transport": "streamable_http", "url": "https://api.mycompany.com/mcp"}` |
| stdio | Process-based (parent <-> child via streams) | When MCP server runs as subprocess of your application | `{"transport": "stdio", "command": "python", "args": ["server.py"]}` |

**Understanding stdin and stdout**:
- **stdin** (standard input): Where a program reads input - like text from keyboard or piped data.
- **stdout** (standard output): Where a program writes output - like text to console or screen.
- With stdio transport, the client and server talk to each other through these streams, like two programs connected via a pipe.

<img src="images/Screenshot 2026-07-17 at 7.23.54 AM.png" alt="Transport Type" width="600"/>

### Why MCP Matters

| Without MCP | With MCP |
| -------- | -------- |
| Custom integration per service | One standard protocol |
| Separate auth for each | Unified approach |
| Time intensive to add services | Quicker to add services |


## How to Get Started
1. Clone the repository:
```bash
git clone https://github.com/wenyuliuinfo/langchain_for_beginners.git
cd langchain_for_beginners/
```

2. Install the prerequisites:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
```

3. Run the application:
```bash
cd 06-mcp/python
python 01_mcp_multi_server.py
```
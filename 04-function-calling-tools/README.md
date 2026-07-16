# Function Calling and Tools
In this chapter, you'll learn how to extend AI capabilities beyond text generation by enabling function calling and tools. You'll discover how LLMs can invoke functions with structured arguments, create type-safe tools using Pydantic schemas, and build systems where AI can trigger real-world actions like API calls, database queries, or calculations.


## What is Function Calling?
Function calling transforms LLMs from text generators into action coordinators. Instead of just producing text, LLMs can trigger real-world operations - checking weather, querying databases, calling APIs, and more.

### Understanding the Execution Model
Critical concept: The LLM never executes functions directly. Here's what actually happens:

1. LLM's Role (Planning):
    - Analyzes user request
    - Determines which functions to call
    - Generates structured function calls with arguments
    - Returns this as JSON
2. Your Code's Role (Doing):
    - Receives function call descriptions
    - Actually executes the functions
    - Gets real results (API Calls, calculations, etc.)
    - Sends results back to LLM
3. LLM's Role Again (Communicating):
    - Incorporates function results into natural response
    - Returns helpful answer to user

### Why this Separation Matters
Security and Control: Your code decides what functions exist and controls execution. You can reject dangerous operations.

<img src="images/Screenshot 2026-07-16 at 7.44.49 AM.png" alt="Function Calling" width="600"/>


## Creating Tools with the @tool Decorator
In LangChain Python, tools are created using the `@tool` decorator with Pydantic schemas for type safety.

If you're new to Pydantic, it's a Python library for data validation using Python type annotations. Think of it as a way to describe what valid input looks like. Pydantic validates data at runtime and provides excellent type inference.

You want to give your AI real-time calculator capabilities. Without tools, the AI can only guess at calculations or say "I can't do math." With a calculator tool, the AI can recognize when a calculation is needed and request execution of the actual computation.


## Binding Tools to Models
Use `bind_tools()` to make tools available to the LLM.

You've created a calculator tool, but how does the AI know it exists? The tool sits in your code, disconnected from the AI. You need to tell the AI "here are the tools you can use" and let the AI decide when to call them. That's where `.bind_tools()` comes in - it connects tools to the model so the AI can intelligently choose when to use them.

<img src="images/Screenshot 2026-07-16 at 7.52.03 AM.png" alt="Binding Tools" width="600"/>


## Handling Tool Execution
In this example, you'll see the complete flow: LLM generates tool call, your code executes the tool, and results return to LLM for the final response.

<img src="images/Screenshot 2026-07-16 at 7.53.52 AM.png" alt="Tool Calling Loop" width="600"/>


## Multiple Tools
LLMs can choose from multiple tools based on the query.

You're building an AI assistant that needs different capabilities - math calculations, web searches, and weather lookups. Instead of creating separate AI instances or complex routing logic, you want one AI that intelligently chooses the right tool for each task. The AI should automatically pick the calculator for "What is 25*4?", search tool for "What's the capital of France?".


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
cd 04-function-calling-tools/python
python 01_messages_templates.py
```
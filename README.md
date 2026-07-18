# LangChain for Beginners

This repository is a comprehensive, code-first learning path for mastering [LangChain](https://www.langchain.com/), the leading framework for building applications powered by Large Language Models (LLMs). It is based on Microsoft's "LangChain for Beginners" course but focuses heavily on practical, executable Python code.

## 🎯 About This Repository

LangChain has become an essential tool for AI developers. This repository is designed to take you from the absolute basics to advanced concepts like **Agentic RAG**, providing a structured, hands-on learning experience. Each module contains clear, well-commented Python scripts and Jupyter Notebooks that you can run and experiment with.

The goal is to move beyond theory and provide you with the practical skills needed to build robust, production-ready LLM applications using the LangChain ecosystem.

## 📂 Repository Structure

The content is organized into a progressive set of modules, each focusing on a core LangChain concept.

```
langchain_for_beginners/
    ├── 01-introduction/ # Core concepts and setting up LangChain
    ├── 02-chat-models/ # Working with chat-based LLMs
    ├── 03-prompts-messages-outputs/ # Prompt engineering, messages, and parsing outputs
    ├── 04-function-calling-tools/ # Enabling LLMs to use external tools and functions
    ├── 05-agents/ # Building autonomous agents that can reason and act
    ├── 06-mcp/ # Model Context Protocol
    ├── 07-documents-embeddings/ # Handling documents and creating embeddings
    ├── 08-agentic-rag/ # Advanced Retrieval-Augmented Generation with agents
    ├── .env.example # Example environment variables file
    ├── .gitignore
    ├── README.md
    └── requirements.txt # All required Python dependencies
```


Each module folder typically contains:
*   **`README.md`**: A detailed guide for that specific lesson.
*   **`.py` Python scripts**: More structured code for applications.

## 🚀 Getting Started

### Prerequisites

To effectively use this repository, you should have:
- Solid knowledge of Python programming.
- A basic understanding of LLMs and prompt engineering.
- An API key for an LLM provider (e.g., OpenAI, Azure OpenAI, Anthropic, or a local model via Ollama).

### Installation & Running the Code

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/wenyuliuinfo/langchain_for_beginners.git
    cd langchain_for_beginners
    ```

2. **Set up a Python environment:**
It's highly recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies:**
All necessary packages are listed in requirements.txt.
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your API Keys:**
Most projects will require an API key. Copy the .env.example file to .env in the root directory and add your keys:
    ```bash
    cp .env.example .env
    # Edit .env with your credentials (e.g., OPENAI_API_KEY="your-key-here")
    ```

5. **Run a Module:**
Navigate into a module folder and execute the main Python script.
    ```bash
    cd 02-chat-models/python
    python 01_multi_turn.py
    ```

## 🧠 Key Topics & Learning Path

This repository is structured to guide you through the entire LangChain ecosystem.

### 1. Introduction (01-introduction)
Core Concepts: Understand what LangChain is, its architecture, and its core components (Models, Prompts, Chains, Agents, Memory).

Setup: Install LangChain and get ready to build.

### 2. Chat Models (02-chat-models)
Chat vs. Completion: Learn the difference and how to use LangChain's chat model interfaces.

Message Types: Work with SystemMessage, HumanMessage, and AIMessage to create structured conversations.

### 3. Prompts, Messages, and Outputs (03-prompts-messages-outputs)
Prompt Templates: Create reusable and dynamic prompts.

Output Parsers: Structure LLM responses into useful Python objects (e.g., lists, JSON).

### 4. Function Calling & Tools (04-function-calling-tools)
Tool Definition: Learn how to define functions and make them callable by an LLM.

Tool Binding: Bind tools to chat models to enable them to take actions.

### 5. Agents (05-agents)
Agent Architecture: Understand the reasoning loop and how agents decide which tools to use.

Agent Types: Explore different agent types (e.g., ReAct, OpenAI Tools).

### 6. MCP (06-mcp)
Model Context Protocol: Introduction to MCP for standardized model interactions.

### 7. Documents & Embeddings (07-documents-embeddings)
Document Loading: Load data from various sources (PDFs, web pages, etc.).

Text Splitting: Chunk documents for efficient processing.

Embeddings & Vector Stores: Create embeddings and store them in vector databases (e.g., Chroma, FAISS) for semantic search.

### 8. Agentic RAG (08-agentic-rag)
The Peak of the Learning Path: Combine agents with RAG (Retrieval-Augmented Generation).

Advanced Reasoning: Build an agent that can intelligently retrieve and synthesize information from external documents to answer complex, multi-step queries.

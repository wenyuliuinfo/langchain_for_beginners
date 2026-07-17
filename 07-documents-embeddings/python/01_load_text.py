"""
Lesson 07 - Loading Text Files
"""

from pathlib import Path
from langchain_community.document_loaders import TextLoader

def main():
    print("Loading Text Files Example\n")

    # Create data directory if it doesn't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)

    # Create sample text file
    sample_text = """
LangChain: A Framework for AI Applications

LangChain is a framework for building applications with large language models.
It provides a comprehensive set of tools and abstractions that make it easier
to work with LLMs in production environments.

Key Features:
- Model Abstraction: Work with different AI providers using the same interface
- Prompt Management: Create reusable, testable prompts with templates
- Document Processing: Load, split, and manage documents efficiently
- Vector Stores: Store and retrieve embeddings for semantic search
- Tools: Extend AI capabilities with custom functions and APIs
- Agents: Build AI systems that can make decisions and use tools
- Memory: Maintain conversation context across interactions

The framework is designed to be modular and composable, allowing developers
to build complex AI applications by combining simple, reusable components.

Getting Started:
Install LangChain using pip, configure your API keys, and start
building AI-powered applications with just a few lines of code.
    """.strip()

    sample_file = data_dir / "sample.txt"
    sample_file.write_text(sample_text)
    print("Created sample.txt in ./data/\n")

    # Load the document
    loader = TextLoader("./data/sample.txt")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents\n")

    # Examine the loaded document
    print("Document Properties:")
    print("-" * 80)
    print("\nContent (first 200 chars): ")
    print(docs[0].page_content[:200] + "...\n")
    
    print("Metadata:")
    print(docs[0].metadata)

if __name__ == "__main__":
    main()
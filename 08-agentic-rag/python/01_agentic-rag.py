"""
Lesson 08 - Agentic RAG System
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import ZhipuAIEmbeddings

# Load Environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL")

def main():
    print("Agentic RAG System Example\n")
    
    # 1. Initialize the embedding and model
    embeddings = ZhipuAIEmbeddings(
        api_key=ZHIPUAI_API_KEY,
        api_base=ZHIPUAI_BASE_URL,
        model="embedding-3"
    )
    
    model_name = "deepseek-v4-pro"
    model = ChatOpenAI(
        model=model_name,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )

    # 2. Create knowledge base about LangChain and RAG
    docs = [
        Document(
            page_content="LangChain was created in 2022 and quickly became popular for building LLM applications. The Python version was first, followed by LangChain.js for JavaScript/TypeScript.",
            metadata={"source": "langchain-history", "topic": "introduction"},
        ),
        Document(
            page_content="RAG (Retrieval Augmented Generation) combines document retrieval with LLM generation. It allows models to access external knowledge without retraining, making responses more accurate and up-to-date.",
            metadata={"source": "rag-explanation", "topic": "concepts"},
        ),
        Document(
            page_content="Vector stores like Pinecone, Weaviate, and Chroma enable semantic search over documents. They store embeddings and perform fast similarity searches to find relevant content.",
            metadata={"source": "vector-stores", "topic": "infrastructure"},
        ),
        Document(
            page_content="LangChain supports multiple document loaders for PDFs, web pages, databases, and APIs. Text splitters help break large documents into chunks that fit within LLM context windows while preserving semantic meaning.",
            metadata={"source": "document-processing", "topic": "development"},
        ),
    ]
    print(f"Creating vector store with {len(docs)} documents...\n")

    # 3. Create vector store
    vector_store = InMemoryVectorStore.from_documents(docs, embeddings)

    # 4. Create retrieval tool from vector store
    @tool
    def search_langchain_docs(query: str) -> str:
        """
        Search LangChain documentation for specific information about LangChain, RAG systems, vector stores, and document processing. Use this when you need factual information from the LangChain knowledge base.
        """
        print(f"  Agent is searching for: {query}")
        results = vector_store.similarity_search(query, k=2)
        return "\n\n".join(
            f"[{doc.metadata["source"]}]: {doc.page_content}"
            for doc in results
        )

    # 5. Create agent with retrieval tool
    # The agent will autonomously decide when to search vs. answer directly
    agent  = create_agent(
        model,
        tools=[search_langchain_docs],
        system_prompt="You are a helpful assistant with access to LangChain documentation. Use the search tool when you need specific information about LangChain, RAG, or vector stores. For general knowledge questions, answer directly without searching."
    )

    # 6. Ask different types of questions to see agent decision-making
    questions = [
        # General knowledge - agent should answer directly without searching
        "What is the capital of France?",
        # Document-specific questions - agent should use the retrieval tool
        "When was LangChain created?",
        "What is RAG and why is it useful?",
    ]
    print("Watch how the agent decides when to search vs. answer directly:\n")
    
    for question in questions:
        print("=" * 80)
        print(f"\nQuestion: {question}")
        
        response = agent.invoke({"messages": [HumanMessage(content=question)]})
        final_message = response["messages"][-1]
        print("Answer:", final_message.content)

if __name__ == "__main__":
    main()
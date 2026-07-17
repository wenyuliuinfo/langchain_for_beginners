"""
Lesson 07 - Working with Metadata
"""

import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    print("Document Metadata Example\n")
    
    # Create documents with rich metadata
    docs = [
        Document(
            page_content="""
LangChain is a framework for building AI applications. It provides abstractions
for working with language models, vector stores, and chains. The framework supports
multiple LLM providers including OpenAI, Anthropic, and Azure.
            """.strip(),
            metadata={
                "source": "langchain-intro.md",
                "category": "tutorial",
                "difficulty": "beginner",
                "date": "2024-01-15",
                "author": "Tech Team",
                "tags": ["langchain", "python", "ai"],
            }
        ),
        Document(
            page_content="""
RAG (Retrieval Augmented Generation) systems combine document retrieval with
language model generation. This approach allows LLMs to access external knowledge
and provide more accurate, contextual responses without retraining the model.
            """.strip(),
            metadata={
                "source": "rag-explained.md",
                "category": "concept",
                "difficulty": "intermediate",
                "date": "2024-02-20",
                "author": "AI Research Team",
                "tags": ["rag", "retrieval", "llm"],
            }
        ),
        Document(
            page_content="""
Vector databases store embeddings and enable semantic search. Unlike traditional
keyword search, semantic search understands meaning and context. Popular vector
databases include Pinecone, Weaviate, and Chroma.
            """.strip(),
            metadata={
                "source": "vector-db-guide.md",
                "category": "infrastructure",
                "difficulty": "intermediate",
                "date": "2024-03-10",
                "author": "Data Team",
                "tags": ["vectors", "embeddings", "database"],
            }
        ),
    ]

    print(f"Created {len(docs)} documents with metadata\n")

    # Display documents and their metadata
    for i, doc in enumerate(docs):
        print(f"Document {i+1}:")
        print("-" * 80)
        print("Content: ", doc.page_content[:80] + "...")
        print("\nMetadata:")
        print(json.dumps(doc.metadata, indent=2))
        print("\n")

    # Split documents - metadata is preserved
    print("=" * 80)
    print("\nSplitting documents (metadata is preserved):\n")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
    )
    split_docs = splitter.split_documents(docs)
    print(f"Split {len(docs)} documents into {len(split_docs)} chunks\n")

    # Show first few chunks with metadata
    for i, doc in enumerate(split_docs[:3]):
        print(f"Chunk {i + 1}:")
        print("Content:", doc.page_content)
        print("Source:", doc.metadata.get("source"))

    # Filter documents by metadata
    print("=" * 80)
    print("\nFiltering by metadata:\n")

    beginner_docs = [doc for doc in docs if doc.metadata.get("difficulty") == "beginner"]
    print(f"Beginner documents: {len(beginner_docs)}")
    for doc in beginner_docs:
        print(f"    - {doc.metadata.get("source")}")

if __name__ == "__main__":
    main()
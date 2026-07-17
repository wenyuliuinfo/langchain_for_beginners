# Documents, Embeddings & Semantic Search
In this chapter, you'll learn the complete pipeline for working with documents in AI applications - from loading and preparing documents to enabling intelligent semantic search. You'll discover how to load content from various sources, split it into manageable chunks, convert text into numerical embeddings, and perform similarity searches that understand meaning rather than just matching keywords.


## Part 1: Working with Documents
### Why Document Loaders?
LLMs need text input, but data comes in many formats: text files, PDFs, websites, JSON/CSV, and more. Document loaders handle the complexity of reading different formats.

<img src="images/Screenshot 2026-07-17 at 9.12.32 AM.png" alt="Document Loaders" width="600"/>

The document processing pipeline: Load documents -> Split into chunks -> Create embeddings -> Store in vector database, ready for semantic search.

### Splitting Documents
- **LLM context limits**: Models can only process ~4,00-128,000 tokens.
- **Relevance**: Smaller chunks = more precise retrieval.
- **Cost**: Smaller inputs = Lower API costs.

| Small Chunks (200-500 chars) | Large Chunks (1000-2000 chars) | 
| ------- | ------- |
| More precise | More context | 
| Better for specific questions | Better for complex topics |
| May lose context | Less precise matching |
| More chunks to process | Fewer chunks |

### Chunk Overlap
**Why overlap chunks?** Without overlap, splits mid-sentence, losing context. Without overlap, both chunks include the part preserving meaning.

**Recommended overlap**: Start with 20% of chunk size.

### Document Metadata
Metadata helps you:
- Track document source
- Filter by category, date, author
- Understand context


## Part 2: Embeddings
Embeddings convert text into numerical vectors that capture semantic meaning:
- Similar concepts -> Similar vectors
- "king" - "man" + "woman" = "queen"

<img src="images/Screenshot 2026-07-17 at 9.22.13 AM.png" alt="embeddings" width="600"/>


## Part 3: Vector Stores
Vector stores are databases optimized for storing and searching embeddings:
- Store: Add documents with their embeddings.
- Search: Find similar documents using vector similarity.


## Part 4: Semantic Search
### Keyword vs. Semantic Search
<img src="images/Screenshot 2026-07-17 at 9.24.48 AM.png" alt="Semantic Search" width="600"/>


## Part 5: Batch Processing
### Key Takeaways:
- Batch processing is typically faster
- Reduces API calls (lower costs)
- Always use `embed_documents()` for multiple texts


## Part 6: Embedding Relationships
Embeddings capture semantic relationships that can be manipulated through vector arithmetic:
```
Embedding("Puppy") - Embedding("Dog") + Embedding("Cat") ≈ Embedding("Kitten")
```

This works because embeddings encode relationships like species and life stage as separate dimensions.


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
cd 07-documents-embeddings/python
python 01_load_text.py
```
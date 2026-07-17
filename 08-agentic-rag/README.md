# Building Agentic RAG Systems
In this chapter, you'll learn to build **Agentic RAG** systems where AI agents intelligently decide when and how to search your documents to answer questions. Unlike traditional RAG that always searches regardless of need, agentic RAG gives your AI the knowledge, or searching your documents when additional context is needed.


## Agentic RAG vs. Traditional RAG
### Key Difference
**Traditional RAG**:
Every question triggers a search, even if the agent already knows the answer.
```
User Question → ALWAYS Search → Retrieve Docs → Generate Answer
```

**Agentic RAG**:
The agent uses reasoning to determine whether retrieval is necessary.
```
User Question → Agent Decides → [Search if needed] → Generate Answer
```

<img src="images/Screenshot 2026-07-17 at 10.47.46 AM.png" alt="Agentic RAG" width="600"/>

### Benefits of Agentic RAG
| Benefit | Traditional RAG | Agentic RAG | 
| ------- | ------- | ------- | 
| Efficiency | Searches every time | Only searches when needed |
| Speed | Slow for simple questions | Fast for simple, thorough for complex |
| Cost | Embedding + search cost on every query | Lower cost - searches only when necessary |
| Intelligence | Rigid, predictable | Adaptive, makes decisions |
| Complexity | Simple pipeline | Requires agent loop |


## Agentic RAG Architecture

<img src="images/Screenshot 2026-07-17 at 10.52.33 AM.png" alt="RAG Architecture" width="600"/>

### When to Use RAG vs. Prompt Engineering
**Decision Tree**:
1. Fits easily in prompt -> Prompt Engineering
2. Large knowledge base that doesn't fit -> RAG
3. Updates frequently -> RAG
4. Need source citations -> RAG

<img src="images/Screenshot 2026-07-17 at 10.55.12 AM.png" alt="RAG vs Prompt Engineering" width="600"/>


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
cd 08-agentic-rag/python
python 01_agentic_rag.py
```
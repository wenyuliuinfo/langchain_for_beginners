# Prompts, Messages, and Structured Outputs
In this chapter, you'll learn the three essential techniques for working with LLMs in LangChain: messages, prompt templates, and structured outputs. Understanding these techniques is key, because modern LangChain applications choose different approaches depending on the use case. Messages provide dynamic construction for flexible workflows like agents, templates provide reusable prompts with variable substitution, and structured outputs ensure type-safe data extraction.


## Decision Framework: Messages vs. Templates
Before diving into the code, understand when to use each approach:
<img src="images/Screenshot 2026-07-14 at 7.54.19 AM.png" alt="Decision Framework" width="800"/>

| Approach | Use For | Chapter | 
| -------- | -------- | -------- |
| Messages | Agents, dynamic workflows, multi-step reasoning, tool integration | Getting Started with Agents |
| Templates | Reusable prompts, variable substitution, consistency, RAG systems | Documents, Embeddings & Semantic Search |


## PART 1: Message-Based Prompt
Message arrays are the foundation of agent systems in LangChain. When you work with agents, you'll use message arrays as input and output.

### The Conversation Analogy
<img src="images/Screenshot 2026-07-14 at 8.01.50 AM.png" alt="Message based Prompt" width="600"/>

Think of communicating with an AI like having a conversation. Just like in human conversation, there are different types of messages:
- **System Message**: The ground rules - like telling someone before a conversation that they're playing a character.
- **Human Message**: What you say.
- **AI Message**: What the AI responds with.


## PART 2: Template-Based Prompt
Templates allow you to create reusable, maintainable prompts with variables. Think of them like "mail merge" - same format, different values.

### The Mail Merge Analogy
<img src="images/Screenshot 2026-07-14 at 8.10.09 AM.png" alt="Template based Prompt" width="600"/>

Templates work like mail merge in word processors:
- Create a template once with placeholders (`{name}`, `{product}`)
- Reuse it with different values.
- Perfect for consistent, repeatable prompts.


## PART 3: Structured Outputs with Pydantic
Use Pydantic models to get type-safe, structured data from LLMs. This ensures you get exactly the data structure you need.

### The Schema Analogy
Think of structured outputs like a form:
- You define the fields (name, email, age).
- The AI fills in the form.
- You get validated, typed data back.


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
cd 03-prompts-messages-outputs/python
python 01_messages_templates.py
```
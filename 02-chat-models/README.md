# Chat Models and Basic Interactions
In this chapter, you'll learn the art of having natural conversations with AI models. You'll learn how to maintain conversation context across multiple exchanges, stream responses in real-time for better user experience, and handle errors gracefully with retry logic. You'll also explore key parameters like temperature to control AI creativity and understand token usage for cost optimization.


## The Knowledgeable Friend Analog
Imagine you're having coffee with a knowledgeable friend.
When you talk to them:
- **You have a back-and-forth conversation**: not just one question.
- **They remember what you said earlier**: conversation context.
- **They speak as they think**: streaming response.
- **They adjust their tone**: based on your preferences - model parameters.
- **Sometimes they need clarification**: error handling.

Chat models work the same way. Unlike simple one-off questions, chat models excel at:
- Multi-turn conversations;
- Maintaining context;
- Streaming responses in real-time;
- Adapting their behavior;

<img src="images/Screenshot 2026-07-13 at 9.55.47 AM.png" alt="Chat Models" width="800"/>


## Multi-Turn Conversation
Previously, we sent single messages. But real conversations have multiple exchanges.

### How Conversation History Works
Chat models don't actually remember previous messages. Instead, you send the entire conversation history with each new message.

Think of it like this: Every time you send a message, you're showing the AI the entire conversation thread so far.

<img src="images/Screenshot 2026-07-13 at 10.00.55 AM.png" alt="Multi-turn conversation" width="800"/>

### Message Types in LangChain
LangChain provides three core message types for building conversations:

| Type | Purpose | Example | 
| ---- | ---- | ---- |
| SystemMessage | Set AI behavior and personality | `SystemMessage(content="You are a helpful coding tutor")` |
| HumanMessage | User input and questions | `HumanMessage(content="What is Python?")` |
| AIMessage | AI responses with metadata | Returned by `model.invoke()` with `content`, `usage_metadata`, `id` | 


## Streaming Response
When you ask a complex question, waiting for the entire response can feel slow. Streaming sends the response word-by-word as it's generated.

Like watching a friend think out loud instead of waiting for them to finish their entire thought.

You're building a chatbot where users ask complex questions. With regular responses, users stare at a blank screen for 5-10 seconds wondering if anything is happening. With streaming, they see words appearing immediately - just like ChatGPT - which feels much more responsive even if the total time is the same.

<img src="images/Screenshot 2026-07-13 at 10.10.34 AM.png" alt="Streaming Response" width="800"/>


## Model Parameters
You can control how the LLM responds by adjusting parameters. These can vary by provider/model so always check the documentation.

### Two Key Parameters
##### 1. Temperature (0.0-2.0)
Temperature controls randomness and creativity:
- 0.0 = Deterministic: Same question -> same answer.
  - Use for: Code generation, factual answers.
- 1.0 = Balanced: Mix of consistency and variety.
  - Use for: General conversation.
- 2.0 = Creative: Some models support up to 2.0 for more random and creative responses but is generally less predictable.
  - Use for: Creative writing, brainstorming.

##### 2. Max Tokens
What are Tokens? Tokens are the basic units of text that AI models process. Think of them as pieces of words - roughly 1 token = 4 characters or 3/4 a word.

Limits response length:
- Controls how long responses can be;
- Setting `max_tokens=100` limits the response to approximately 75 words;
- Prevents runaway costs by capping output length.


## Provider-Agnostic Initialization
LangChain provides `init_chat_model()` for provider-agnostic initialization. Think of it like universal power adapter - instead of different chargers for each device, you have one adapter that works with all of them.

### Why Use init_chat_model()?
- **Easy Provider Switching**: Change providers by updating a single string.
- **Framework Building**: Create libraries that support many providers.
- **Unified Interface**: Same code pattern works across all providers.


## Error Handling with Built-in Retries
API calls can fail due to rate limits, network issues, or temporary service problems. LangChain provides built-in retry logic with exponential backoff.

### Common Errors You'll Encounter
- **429 Too Many Requests**: Rate limit exceeded -  most common for free tiers.
- **401 Unauthorized**: Invalid API key.
- **500 Server Error**: Temporary provider issues.
- **Network Timeout**: Connection problems.


## Token Tracking and Costs
Tokens power AI models, and they directly impact cost and performance. Let's track them.


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
cd 02-chat-models/python
python 01_multi_turn.py
```
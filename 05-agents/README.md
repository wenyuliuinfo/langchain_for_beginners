# Getting Started with Agents
In this chapter, you'll learn to build AI agents that can reason about problems, select appropriate tools, and work iteratively towards solutions. You'll understand the ReAct (Reasoning + Acting) pattern by implementing agent loops step-by-step, and discover how agents autonomously choose tools to accomplish complex tasks. These skills enable you to build autonomous AI systems that can handle complex, multi-step tasks.


## What are Agents?
### Standard LLM (No Agency or Tools)
```
User: "What's the current weather in Paris?"
LLM: "I cannot access real-time weather data. I can only provide general information..."
```

### Agent with Tools
```
User: "What's the current weather in Paris?"
Agent: [Thinks] "I need to use the weather tool"
Agent: [Uses] get_weather(city="Paris")
Agent: [Observes] "18°C, partly cloudy"
Agent: [Responds] "It's currently 18°C and partly cloudy in Paris"
```
<img src="images/Screenshot 2026-07-16 at 9.49.16 AM.png" alt="Agent with Tools" width="600"/>


## The ReAct Pattern
ReAct = Reasoning + Acting

The agents follow this iterative loop:
```
1. Thought: What should I do next?
2. Action: Use a specific tool
3. Observation: What did the tool return?
4. (Repeat 1-3 as needed)
5. Final Answer: Respond to the user
```
<img src="images/Screenshot 2026-07-16 at 9.53.00 AM.png" alt="ReAct Pattern" width="600"/>


## Building Agents with create_agent()
LangChain Python provides `create_agent()` from `langchain.agents` - a high-level API that handles the ReAct loop automatically. This is the recommended approach for building production agents.

What the create_agent() does for you:
- Manages the ReAct loop (Thought -> Action -> Observation -> Repeat)
- Handles message history automatically
- Implements iteration limits to prevent infinite loops
- Provides production-ready error handling
- Returns clean, structured response


## Additional Agent Patterns
Now that you understand how to build basic agents with single and multiple tools, let's explore an additional pattern for production applications: middleware. Middleware lets you add behavior like logging, error handling, and dynamic model selection without modifying your tools or agent core logic.


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
cd 05-agents/python
python 01_create_agent_multi_tools.py
```
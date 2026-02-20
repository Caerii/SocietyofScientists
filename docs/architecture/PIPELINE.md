# Proposal Generation Pipeline

This document traces the complete lifecycle of a grant proposal generation, from user input to final output.

## Entry Points

There are three ways to start a proposal:

```python
# 1. Python API
from society_of_scientists import create_society_of_mind_system
agent, proxy, mgr = create_society_of_mind_system(task="...")
result = proxy.initiate_chat(agent, message="...")

# 2. Command line
python -m society_of_scientists "Your research topic"

# 3. REST API
POST /api/proposal/start {"task": "Your research topic"}
```

All three paths converge on `create_society_of_mind_system()` followed by `user_proxy.initiate_chat()`.

## System Initialization

When `create_society_of_mind_system(task, max_rounds=50, speaker_selection_method='round_robin', register_exa_tool=True)` is called:

```
1. Load configuration
   Settings reads .env → builds Jamba config dict
   {model, api_key, temperature, top_p, max_tokens}

2. Create agents (12 total)
   For each agent:
     a. create_agent(name, system_message, llm_config)
     b. register_model_client(agent, AI21JambaModelClient)

3. Assemble group chat
   GroupChat(agents=[all 12], max_round=50, speaker_selection_method='round_robin')
   GroupChatManager(groupchat, llm_config, system_message=moderator_prompt)

4. Wrap in SocietyOfMindAgent
   SocietyOfMindAgent("society_of_mind", chat_manager=manager, llm_config)

5. Create UserProxyAgent
   human_input_mode="NEVER", code_execution_config=False
   is_termination_msg=lambda x: True  (terminates after SoM agent responds)

6. Register tools (if enabled)
   register_function(exa_search_function, caller=som_agent, executor=user_proxy)
```

## Conversation Flow

Once `user_proxy.initiate_chat(society_of_mind_agent, message=task)` is called:

```
Step 1: UserProxy sends the task message to SocietyOfMindAgent

Step 2: SocietyOfMindAgent delegates to GroupChatManager

Step 3: GroupChatManager runs the inner group chat
        Speaker order (round-robin): planner → cv_scientist → llm_scientist →
        hw_scientist → scientist → hypothesis → objective → methodology →
        novelty → ethics → budget → critic

Step 4: For each agent's turn:
        a. Agent receives conversation history
        b. AI21JambaModelClient.create() is called
           - Converts messages to AI21 format
           - Calls AI21 chat completions API
           - Extracts token usage
           - Records usage in CostTracker
           - Returns response in AutoGen format
        c. Agent's response is added to conversation history
        d. If agent requests a tool call → UserProxy executes it

Step 5: After max_rounds or all agents have spoken:
        GroupChatManager returns the conversation

Step 6: SocietyOfMindAgent summarizes the inner conversation
        and returns a single response to UserProxy

Step 7: UserProxy receives the response
        is_termination_msg returns True → conversation ends
```

## What Each Agent Produces

The round-robin progression builds the proposal incrementally:

### Phase 1: Planning (Round 1)

**Planner** receives the user's task and outputs a structured plan:
- Overview of the grant writing process
- Breakdown of which agents should contribute what
- Sequence of actions for each agent

### Phase 2: Domain Discussion (Rounds 2-4)

**CV Scientist** reads the plan and task, contributes:
- Relevant computer vision techniques and recent papers
- How CV methods apply to the research topic
- Quantitative details (accuracy metrics, model parameters)

**LLM Scientist** reads the plan, task, and CV contribution:
- Language model techniques relevant to the topic
- Connections between LLM capabilities and the proposal
- Architectural details and benchmarks

**Hardware Scientist** reads all prior context:
- Hardware considerations for the proposed research
- Computational requirements and optimization strategies
- Relevant accelerator architectures

### Phase 3: Synthesis (Round 5)

**Scientist** reads all domain contributions and produces the initial 7-section proposal:
```json
{
  "1- hypothesis": "...",
  "2- objectives": "...",
  "3- methodology": "...",
  "4- novelty": "...",
  "5- ethics": "...",
  "6- budget": "...",
  "7- comparison": "..."
}
```

### Phase 4: Section Expansion (Rounds 6-12)

Each section agent reads the full conversation and deeply expands its section:

| Round | Agent | Expands | Adds |
|-------|-------|---------|------|
| 6 | Hypothesis | The core hypothesis | Scientific grounding, formulas, predictions |
| 7 | Objective | Expected findings | Quantitative metrics, timelines, deliverables |
| 8 | Methodology | Research methods | Algorithms, datasets, evaluation protocols |
| 9 | Novelty | What's new | Comparison to state-of-art, technical advances |
| 10 | Ethics | Implications | Societal impact, data privacy, bias concerns |
| 11 | Budget | Cost estimate | Line items, personnel, equipment, justification |
| 12 | Critic | Entire proposal | Strengths, weaknesses, improvements, key questions |

### Phase 5: Review (Round 12)

**Critic** reads everything and produces:
1. One-paragraph summary with sufficient technical detail
2. Critical scientific review with strengths, weaknesses, and improvements
3. The single most impactful question for molecular modeling, with setup steps
4. The single most impactful question for synthetic biology, with experimental steps

## Output

The final output is the complete conversation history containing all agent contributions. The proposal is not a single document — it is the concatenation of:

- The scientist's 7-section draft
- Seven expanded sections from the expander agents
- The critic's review

The `result` object returned by `initiate_chat()` contains:
- `result.chat_history` — list of all messages
- `result.summary` — the SocietyOfMindAgent's summary of the inner conversation
- `result.cost` — total cost tracked by AutoGen

## Token Usage and Costs

A typical run with `max_rounds=50` and round-robin speaking:
- 12-13 agent turns (one per agent, possibly a second round)
- Each turn: ~500-2,000 prompt tokens (growing as conversation accumulates) + ~500-2,000 completion tokens
- Total: ~10,000-30,000 tokens depending on topic complexity

At Jamba Large pricing ($0.002/$0.008 per 1K prompt/completion tokens), a typical run costs $0.05-0.15.
At Jamba Mini 2 pricing ($0.0002/$0.0004 per 1K), the same run costs $0.005-0.015.

## Tool Usage

When `register_exa_tool=True` (default), the SocietyOfMindAgent can call `exa_search(query)` during the conversation. This function:

1. Creates an `ExaSearch` instance
2. Checks for cached summaries first (default behavior)
3. If cache is available, returns formatted summaries
4. If no cache and Exa API key is configured, performs a live search
5. Returns formatted results: title, URL, and summary for the top 10 matches

In practice, agents rarely invoke the tool explicitly during round-robin execution because they already have research context embedded in their system prompts. The tool is more useful when `speaker_selection_method='auto'` allows the moderator LLM to direct agents to search for specific information.

## Customizing the Pipeline

**Change the number of rounds:** `max_rounds` controls how many agent turns are allowed. The default of 50 is generous — with 12 agents in round-robin, one full cycle is 12 rounds. Set it lower (e.g., 15) for faster runs, or higher for multi-cycle refinement.

**Change speaker selection:** `speaker_selection_method='auto'` lets the GroupChatManager's LLM decide who speaks next based on the conversation. This costs extra LLM calls but can produce more natural flow. `'round_robin'` is deterministic and cheaper.

**Disable tool registration:** `register_exa_tool=False` prevents the search tool from being available. Useful when you want agents to rely solely on their embedded knowledge.

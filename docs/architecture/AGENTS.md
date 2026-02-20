# Agent Reference

The system uses 12 agents organized into four functional groups. All agents use AI21's Jamba model through the same `AI21JambaModelClient` and share a common LLM configuration.

## Agent Roster

```
Execution order (round-robin):

  1. Planner             — plans the proposal structure
  2. CV Scientist        — contributes computer vision expertise
  3. LLM Scientist       — contributes language model expertise
  4. Hardware Scientist   — contributes AI hardware expertise
  5. Scientist           — synthesizes a 7-section proposal draft
  6. Hypothesis Agent    — expands the hypothesis section
  7. Objective Agent     — expands the objectives section
  8. Methodology Agent   — expands the methodology section
  9. Novelty Agent       — expands the novelty section
 10. Ethics Agent        — expands the ethics section
 11. Budget Agent        — expands the budget section
 12. Critic Agent        — reviews the complete proposal
```

## Orchestration

### Planner

**Name:** `planner`

**Role:** Creates a step-by-step plan for the grant proposal process. Does not execute anything — only suggests the plan for other agents to follow.

**Key prompt instructions:**
- Provide a clear overview of the plan
- Break it down with reasoning for each part
- Must not execute the plan or call any tools

**Why this agent exists:** Without an explicit plan, the round-robin conversation would lack structure. The planner's output becomes the implicit agenda that the scientist agent follows when synthesizing the proposal.

## Domain Scientists

These three agents each contribute domain expertise to the early discussion. Their prompts embed ~100 recent research paper summaries as context, giving them grounding in current literature.

### Computer Vision Scientist

**Name:** `scientist_computer_vision_engineer`

**Role:** Presents recent advances in computer vision relevant to the research topic. Suggests how CV techniques could be combined with other fields in the proposal.

**Embedded context:** 100 paper summaries covering obstacle detection (YOLO), fish monitoring, medical imaging, satellite analysis, deepfake detection, pose estimation, and other CV applications.

**Key prompt instructions:**
- Present opinions from the perspective of computer vision
- Highlight recent discoveries that could extend the research
- Explain how to combine CV advances with other fields
- Be quantitative — include numbers, formulas, sequences

### Language Models Scientist

**Name:** `scientist_ai_language_models`

**Role:** Presents recent advances in large language models, NLP, and AI systems relevant to the topic.

**Embedded context:** 100 paper summaries covering transformer architectures, fine-tuning methods, reasoning capabilities, multimodal models, and language model applications.

**Key prompt instructions:** Same structure as CV scientist, from the LLM perspective.

### AI Hardware Scientist

**Name:** `scientist_ai_hardware_engineer`

**Role:** Presents recent advances in AI hardware, accelerators, and computational infrastructure.

**Embedded context:** 100 paper summaries covering neuromorphic chips, quantum computing for ML, energy-efficient architectures, and custom AI accelerators.

**Key prompt instructions:** Same structure as CV scientist, from the hardware perspective.

## Grant Writers

The grant writer group takes the domain scientists' discussion and the planner's structure, then produces and expands a formal proposal.

### Scientist (Synthesizer)

**Name:** `scientist`

**Role:** The central agent. Reads the three domain scientists' contributions and synthesizes them into a structured grant proposal with seven mandatory sections.

**Output format:** A JSON-like structure with these keys:
```
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

**Key prompt instructions:**
- Must follow the planner's plan
- Synthesize the three scientists' outputs into a novel concept
- Be as quantitative as possible
- Include numbers, sequences, mathematical formulas
- Each section should be detailed
- Must not execute functions or tools

**Why this agent matters:** It is the bridge between the open-ended domain discussion and the structured proposal. Every subsequent agent expands on a section of this agent's output.

### Section Expander Agents

Seven agents each expand one section of the synthesized proposal. They all share the same prompt template with minor variations:

| Agent | Name | Expands | Section variable |
|-------|------|---------|-----------------|
| Hypothesis | `hypothesis_agent` | `{hypothesis}` | The hypothesis section |
| Objective | `objective_agent` | `{objective}` | Expected findings and impact |
| Methodology | `methodology_agent` | `{methodology}` | Algorithms, techniques, datasets |
| Ethics | `ethics_agent` | `{ethics}` | Ethical and societal implications |
| Comparison | `comparison_agent` | `{comparison}` | Comparison with other approaches |
| Novelty | `novelty_agent` | `{novelty}` | Novel aspects and advances |
| Budget | `budget_agent` | `{budget}` | Detailed cost estimates |

**Shared prompt pattern:**

Each expander agent:
1. Reads the original section from the scientist's proposal
2. Critically assesses it as a peer reviewer would
3. Adds specifics: chemical formulas, numbers, sequences, processing conditions, microstructures
4. Adds rationale and step-by-step reasoning
5. Comments on modeling/simulation techniques, experimental methods, or analyses
6. Outputs the expansion under a `### Expanded ...` heading

**Why seven separate agents instead of one?** Each agent focuses entirely on one section, which produces more thorough expansions than asking a single agent to expand everything at once. The section-specific focus also lets the round-robin schedule interleave different perspectives.

## Review

### Critic Agent

**Name:** `critic_agent`

**Role:** Reads the entire expanded proposal and provides:

1. **Summary** — one paragraph covering mechanisms, technologies, methods, models, and experiments
2. **Critical review** — strengths, weaknesses, and suggested improvements with scientific reasoning
3. **Molecular modeling question** — identifies the most impactful question addressable through modeling/simulation, with setup steps
4. **Synthetic biology question** — identifies the most impactful question addressable through experimental biology, with setup steps

**Important constraint:** The critic explicitly does not rate novelty or feasibility. This is intentional — the prompt states this twice. The critic focuses on scientific rigor and actionable improvements rather than subjective scoring.

## Agent Registration

Every agent is created through the compatibility layer (`utils/autogen_compat.py`) and then has the `AI21JambaModelClient` registered on it:

```python
agent = create_agent(name=..., system_message=..., llm_config=...)
register_model_client(agent, AI21JambaModelClient)
```

This two-step process is required because AutoGen needs to know which custom model client to use when the agent generates a response. The compatibility layer handles differences between AG2 and Microsoft AutoGen versions.

## Customizing Agents

To modify agent behavior, edit the prompts in `society_of_scientists/agent_list.py`. The prompts are plain strings — no special templating system. The `{variable}` references in expander prompts (like `{hypothesis}`) are prompt instructions for the LLM, not Python format strings.

To add a new domain scientist, you would:
1. Add a new prompt in `agent_list.py`
2. Create the agent in `agent_factory.py::create_scientist_agents()`
3. Add it to the `all_agents` list in `create_society_of_mind_system()`

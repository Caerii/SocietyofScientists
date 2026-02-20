# Roadmap

## Near-term

### Conversation persistence
Save and resume proposal generation sessions. Store conversation history in SQLite so users can review past proposals, resume interrupted runs, and learn from prior outputs.

### Proposal export
Generate formatted documents from agent output. Support PDF, Word, LaTeX, and Markdown export with configurable templates. The current output is raw conversation text — this would produce publication-ready grant documents.

### Streaming output
Stream agent responses in real time via WebSocket. The REST API server already has WebSocket infrastructure (`/ws` endpoint), but the agent execution currently runs synchronously. Integrating AutoGen's callback system with the WebSocket connection manager would enable live progress updates.

## Medium-term

### Human-in-the-loop control
Let users pause the conversation, inject feedback, or redirect agents mid-run. This requires switching the `UserProxyAgent` from `human_input_mode="NEVER"` to a mode that can accept input at specified points, and wiring that to the frontend.

### Configurable agent roster
Allow users to select which domain scientists participate, adjust the number of expansion rounds, or add custom agents. Currently the 12-agent roster is hardcoded in `create_society_of_mind_system()`. A configuration-driven approach would make the system adaptable to different research domains.

### Citation management
Improve the Exa search integration to produce properly formatted citations. When agents reference research papers, automatically generate BibTeX entries and insert citation markers into the proposal text.

## Longer-term

### Agent performance analytics
Track which agents contribute the most substantive content, measure response quality metrics, and identify collaboration patterns. This data could inform prompt improvements and agent configuration changes.

### Multi-model support
Allow different agents to use different LLMs. For example, domain scientists could use a large model for better reasoning while section expanders use a smaller, cheaper model. The `AI21JambaModelClient` interface is already per-agent, so this requires making model selection configurable per agent role.

### Template system
Save successful proposal structures as templates. Users could load a template to pre-configure agent prompts, section requirements, and output formatting for specific grant programs (NSF, NIH, ERC, etc.).

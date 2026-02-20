"""
Multi-Agent Grant Proposal System Example

This is a refactored version of jamba_working.py that uses the new
centralized agent factory and proper package structure.
"""
from society_of_scientists import create_society_of_mind_system

# Example task
task = "Propose a novel neural network architecture that draws inspiration from multiple disciplines."

# Create the complete system
society_of_mind_agent, user_proxy, manager = create_society_of_mind_system(
    task=task,
    max_rounds=50,
    speaker_selection_method='round_robin',
    register_exa_tool=True
)

# Run the system
print("Starting multi-agent grant proposal generation...")
result = user_proxy.initiate_chat(society_of_mind_agent, message=task)

# Process results (example - customize as needed)
print("\nGrant proposal generation complete!")
print(f"Total messages: {len(result.chat_history)}")

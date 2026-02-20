"""Basic usage example for Society of Scientists."""
from society_of_scientists import (
    create_society_of_mind_system,
    get_tracker
)

# Create the multi-agent system
society_of_mind_agent, user_proxy, manager = create_society_of_mind_system(
    task="Propose a novel neural network architecture that draws inspiration from multiple disciplines.",
    max_rounds=50,
    register_exa_tool=True
)

# Run the system
print("Starting grant proposal generation...")
result = user_proxy.initiate_chat(society_of_mind_agent, message="Propose a novel neural network architecture that draws inspiration from multiple disciplines.")

# Check costs
tracker = get_tracker()
tracker.print_summary()

print("\nGrant proposal generated successfully!")

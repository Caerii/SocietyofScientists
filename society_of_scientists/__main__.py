"""Main entry point for Society of Scientists package."""
import sys
from .agents import create_society_of_mind_system

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python -m society_of_scientists <task>")
        print("\nExample:")
        print('  python -m society_of_scientists "Propose a novel neural network architecture"')
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print("Society of Scientists - Multi-Agent Grant Proposal System")
    print("=" * 60)
    print(f"\nTask: {task}\n")
    
    # Create the system
    society_of_mind_agent, user_proxy, manager = create_society_of_mind_system(
        task=task,
        max_rounds=50,
        speaker_selection_method='round_robin',
        register_exa_tool=True
    )
    
    # Run the system
    print("Starting multi-agent collaboration...\n")
    result = user_proxy.initiate_chat(society_of_mind_agent, message=task)
    
    print("\n" + "=" * 60)
    print("Grant Proposal Generation Complete!")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    main()

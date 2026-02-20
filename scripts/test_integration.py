"""
Integration test for Society of Scientists system.

Tests the full stack: API server, agents, and functionality.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from society_of_scientists.agents import (
    create_society_of_mind_system,
    create_scientist_agents,
    create_grant_writers,
)
from society_of_scientists.utils import get_tracker, get_autogen_version, is_ag2
from society_of_scientists.config import Settings


async def test_agent_creation():
    """Test that agents can be created."""
    print("🧪 Testing agent creation...")
    try:
        from society_of_scientists.agents import get_llm_config
        llm_config = get_llm_config()
        scientists = create_scientist_agents(llm_config)
        grant_writers = create_grant_writers(llm_config)
        
        assert len(scientists) == 3, "Should have 3 scientist agents"
        assert len(grant_writers) == 8, "Should have 8 grant writer agents"
        print("✅ Agent creation: PASSED")
        return True
    except Exception as e:
        print(f"❌ Agent creation: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("🧪 Testing configuration...")
    try:
        settings = Settings()
        assert settings.AI21_API_KEY, "AI21 API key should be set"
        assert settings.EXA_API_KEY, "Exa API key should be set"
        print("✅ Configuration: PASSED")
        return True
    except Exception as e:
        print(f"❌ Configuration: FAILED - {e}")
        return False


def test_cost_tracker():
    """Test cost tracking."""
    print("🧪 Testing cost tracking...")
    try:
        tracker = get_tracker()
        tracker.track_usage(
            model="jamba-large",
            prompt_tokens=100,
            completion_tokens=50,
            operation="test"
        )
        summary = tracker.get_summary()
        assert summary["total_calls"] > 0, "Should have tracked usage"
        print("✅ Cost tracking: PASSED")
        return True
    except Exception as e:
        print(f"❌ Cost tracking: FAILED - {e}")
        return False


def test_autogen_detection():
    """Test AutoGen/AG2 detection."""
    print("🧪 Testing AutoGen detection...")
    try:
        version = get_autogen_version()
        ag2_status = is_ag2()
        print(f"   AutoGen version: {version}")
        print(f"   Is AG2: {ag2_status}")
        print("✅ AutoGen detection: PASSED")
        return True
    except Exception as e:
        print(f"❌ AutoGen detection: FAILED - {e}")
        return False


async def test_system_creation():
    """Test full system creation."""
    print("🧪 Testing system creation...")
    try:
        agent, user_proxy, manager = create_society_of_mind_system(
            task="Test task",
            max_rounds=5,
            register_exa_tool=False  # Skip tool registration for test
        )
        assert agent is not None, "Agent should be created"
        assert user_proxy is not None, "User proxy should be created"
        assert manager is not None, "Manager should be created"
        print("✅ System creation: PASSED")
        return True
    except Exception as e:
        print(f"❌ System creation: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Society of Scientists - Integration Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Configuration", test_config()))
    results.append(("AutoGen Detection", test_autogen_detection()))
    results.append(("Cost Tracker", test_cost_tracker()))
    results.append(("System Creation", await test_system_creation()))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

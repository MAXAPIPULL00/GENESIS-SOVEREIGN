"""
Simple test for NVIDIA NIM integration with Aria
Tests basic code generation without execution loop
"""

import asyncio
import os
from pathlib import Path

from core.agent import AriaAgent
from core.nvidia_nim_client import NVIDIANIMClient


async def test_simple_generation():
    """Test basic code generation using NVIDIA NIM"""

    print("\n" + "=" * 70)
    print("🧪 NVIDIA NIM + Aria Integration Test")
    print("=" * 70)

    # Initialize NIM client
    print("\n1. Initializing NVIDIA NIM Client...")
    nim_client = NVIDIANIMClient()
    print(f"   ✅ NIM Client ready")
    print(f"      LLM: {nim_client.llm_model}")
    print(f"      Embeddings: {nim_client.embedding_model}")

    # Initialize Aria with NIM
    print("\n2. Initializing Aria Agent...")
    config = {
        "nim_client": nim_client,
        "aria": {
            "ollama_url": "http://localhost:11434",  # Dummy (not used)
            "model": "nvidia-nim",
        },
        "vscode": {"workspace_path": "./test_output"},
        "learning": {"enabled": False},
    }

    aria = AriaAgent(config)
    print("   ✅ Aria ready (powered by NVIDIA NIM)")

    # Test simple code generation
    print("\n3. Testing Code Generation...")
    prompt = """Create a simple Python function that:
1. Takes a list of numbers as input
2. Returns the sum of all even numbers in the list
3. Include docstring and type hints
4. Add 2-3 test cases

Just respond with the complete, ready-to-use Python code."""

    print(f"   Prompt: {prompt[:80]}...")

    try:
        response = await aria.chat(prompt)

        print("\n✅ Code Generation Successful!")
        print("\n" + "-" * 70)
        print("Generated Code:")
        print("-" * 70)
        print(response)
        print("-" * 70)

        return True

    except Exception as e:
        print(f"\n❌ Code Generation Failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    success = await test_simple_generation()

    print("\n" + "=" * 70)
    if success:
        print("✅ TEST PASSED: NVIDIA NIM + Aria integration working!")
    else:
        print("❌ TEST FAILED: Check errors above")
    print("=" * 70)

    return success


if __name__ == "__main__":
    # Ensure NVIDIA_NIM_API_KEY is set
    if not os.getenv("NVIDIA_NIM_API_KEY"):
        print("❌ NVIDIA_NIM_API_KEY environment variable not set")
        print("   Get your key from: https://build.nvidia.com")
        exit(1)

    asyncio.run(main())

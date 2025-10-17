"""
🏆 HACKATHON DEMO - GENESIS-SOVEREIGN
AWS x NVIDIA Agentic AI Hackathon 2025

This demo showcases autonomous AI code generation using:
- NVIDIA NIM: llama-3.1-70b-instruct (LLM)
- NVIDIA NIM: nv-embedqa-e5-v5 (Embeddings)
- Autonomous agent architecture
"""

import asyncio
import os
from datetime import datetime

from core.agent import AriaAgent
from core.nvidia_nim_client import NVIDIANIMClient


async def demo_1_simple_function():
    """Demo 1: Generate a utility function"""
    print("\n" + "=" * 70)
    print("📌 DEMO 1: Simple Utility Function")
    print("=" * 70)

    nim = NVIDIANIMClient()
    aria = AriaAgent(
        {
            "nim_client": nim,
            "aria": {"ollama_url": "http://localhost:11434", "model": "nvidia-nim"},
            "vscode": {"workspace_path": "./demo_output"},
            "learning": {"enabled": False},
        }
    )

    prompt = """Create a Python function that validates email addresses using regex.
Include:
- Proper regex pattern for email validation
- Type hints
- Docstring with examples
- Error handling
- 3 test cases"""

    print(f"\n💬 Prompt: {prompt[:80]}...")
    response = await aria.chat(prompt)

    print("\n✨ Generated Code:")
    print("-" * 70)
    print(response)
    print("-" * 70)
    return response


async def demo_2_rest_api():
    """Demo 2: Generate a REST API"""
    print("\n" + "=" * 70)
    print("📌 DEMO 2: REST API with FastAPI")
    print("=" * 70)

    nim = NVIDIANIMClient()
    aria = AriaAgent(
        {
            "nim_client": nim,
            "aria": {"ollama_url": "http://localhost:11434", "model": "nvidia-nim"},
            "vscode": {"workspace_path": "./demo_output"},
            "learning": {"enabled": False},
        }
    )

    prompt = """Create a FastAPI REST API with these endpoints:
1. GET /health - health check
2. POST /users - create user (name, email)
3. GET /users/{id} - get user by id

Include:
- Pydantic models for validation
- In-memory storage (dict)
- Proper HTTP status codes
- Error handling
- Type hints throughout"""

    print(f"\n💬 Prompt: {prompt[:80]}...")
    response = await aria.chat(prompt)

    print("\n✨ Generated Code:")
    print("-" * 70)
    print(response)
    print("-" * 70)
    return response


async def demo_3_data_processing():
    """Demo 3: Data processing pipeline"""
    print("\n" + "=" * 70)
    print("📌 DEMO 3: Data Processing Pipeline")
    print("=" * 70)

    nim = NVIDIANIMClient()
    aria = AriaAgent(
        {
            "nim_client": nim,
            "aria": {"ollama_url": "http://localhost:11434", "model": "nvidia-nim"},
            "vscode": {"workspace_path": "./demo_output"},
            "learning": {"enabled": False},
        }
    )

    prompt = """Create a data processing pipeline that:
1. Reads CSV data (pandas)
2. Cleans missing values
3. Performs basic statistics
4. Exports to JSON

Include:
- Error handling for file operations
- Type hints
- Logging
- Example usage
- Sample data generation"""

    print(f"\n💬 Prompt: {prompt[:80]}...")
    response = await aria.chat(prompt)

    print("\n✨ Generated Code:")
    print("-" * 70)
    print(response)
    print("-" * 70)
    return response


async def demo_4_embeddings():
    """Demo 4: Show embedding capabilities"""
    print("\n" + "=" * 70)
    print("📌 DEMO 4: NVIDIA Retrieval Embedding NIM")
    print("=" * 70)

    nim = NVIDIANIMClient()

    documents = [
        "Python is a high-level programming language",
        "Machine learning is a subset of artificial intelligence",
        "FastAPI is a modern web framework for Python",
        "Docker containers provide application isolation",
        "Kubernetes orchestrates containerized applications",
    ]

    print("\n📄 Documents to embed:")
    for i, doc in enumerate(documents, 1):
        print(f"   {i}. {doc}")

    print("\n🔄 Generating embeddings...")
    embeddings = await nim.embed(documents)

    print(f"\n✅ Generated {len(embeddings)} embeddings")
    print(f"   Dimension: {len(embeddings[0])}")

    # Test semantic search
    query = "What is a web framework?"
    print(f"\n🔍 Query: '{query}'")

    results = await nim.retrieve_context(query, documents)

    print("\n📊 Top Results:")
    for i, result in enumerate(results[:3], 1):
        print(f"   {i}. Score: {result['score']:.3f}")
        print(f"      Text: {result['text']}")

    return results


async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("🏆 GENESIS-SOVEREIGN: Agentic AI Demo")
    print("AWS x NVIDIA Hackathon 2025")
    print("=" * 70)
    print(f"\n⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎯 Technology Stack:")
    print("   ✅ NVIDIA NIM: llama-3.1-70b-instruct (LLM)")
    print("   ✅ NVIDIA NIM: nv-embedqa-e5-v5 (Embeddings)")
    print("   ✅ Autonomous Agent Architecture")
    print("   ✅ AWS Cloud Infrastructure")

    try:
        # Run demos
        await demo_1_simple_function()

        print("\n⏸️  Press Enter to continue to Demo 2...")
        input()
        await demo_2_rest_api()

        print("\n⏸️  Press Enter to continue to Demo 3...")
        input()
        await demo_3_data_processing()

        print("\n⏸️  Press Enter to continue to Demo 4...")
        input()
        await demo_4_embeddings()

        # Summary
        print("\n" + "=" * 70)
        print("🎉 ALL DEMOS COMPLETE!")
        print("=" * 70)
        print("\n✨ What We Demonstrated:")
        print("   ✅ Autonomous code generation")
        print("   ✅ Multiple programming patterns")
        print("   ✅ NVIDIA NIM LLM integration")
        print("   ✅ NVIDIA Retrieval Embedding NIM")
        print("   ✅ Semantic search capabilities")
        print("   ✅ Production-ready code generation")

        print(f"\n⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🏆 GENESIS-SOVEREIGN: Building the Future of Autonomous AI")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("NVIDIA_NIM_API_KEY"):
        print("❌ NVIDIA_NIM_API_KEY not set!")
        print("Run: $env:NVIDIA_NIM_API_KEY='your-key'")
        exit(1)

    asyncio.run(main())

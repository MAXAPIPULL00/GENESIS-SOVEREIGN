#!/usr/bin/env python3
"""
Test script for GENESIS-SOVEREIGN Engine
Simple test to verify the autonomous creation pipeline
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from genesis_engine import GenesisEngine


async def test_simple_creation():
    """Test with a simple hello world API"""

    print("=" * 70)
    print("GENESIS-SOVEREIGN Test")
    print("Testing autonomous software creation")
    print("=" * 70)
    print()

    # Initialize engine
    engine = GenesisEngine()

    # Test with simple need
    print("Testing with: 'Create a hello world REST API'")
    print()

    result = await engine.create_autonomous_software(
        detected_need="Create a hello world REST API with health check endpoint",
        skip_github=True,  # Set to False when GITHUB_TOKEN is configured
        skip_aws=True,  # Set to False when AWS credentials are configured
    )

    # Display results
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    if result["success"]:
        print("\n✅ SUCCESS - Software created autonomously!")
        print(f"\n📁 Files Generated:")
        for file in result.get("files", []):
            print(f"   - {file.get('filename', 'unknown')}")

        print(f"\n📊 Metrics:")
        print(f"   Total Lines: {result['metrics'].get('total_lines', 0)}")
        print(f"   Tests Passed: {'✅' if result.get('tests_passed') else '❌'}")
        print(f"   Security: {'✅' if result.get('security_clean') else '❌'}")
        print(
            f"   Trinity Reviewed: {'✅' if result.get('trinity_reviewed') else '❌'}"
        )

        if result.get("repo"):
            print(f"\n🐙 GitHub:")
            print(f"   Repository: {result['repo']}")

        if result.get("endpoint"):
            print(f"\n☁️  AWS:")
            print(f"   Live Endpoint: {result['endpoint']}")
            print(f"   Region: {result.get('region', 'unknown')}")

        print("\n✅ All systems operational!")

    else:
        print("\n❌ FAILED")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        if result.get("traceback"):
            print("\n📋 Traceback:")
            print(result["traceback"])


async def test_jwt_handler():
    """Test with more complex task - JWT refresh handler"""

    print("\n" + "=" * 70)
    print("GENESIS-SOVEREIGN Advanced Test")
    print("Testing with JWT refresh handler")
    print("=" * 70)
    print()

    engine = GenesisEngine()

    result = await engine.create_autonomous_software(
        detected_need="Create a JWT refresh token handler with secure storage",
        skip_github=True,
        skip_aws=True,
    )

    if result["success"]:
        print("\n✅ Advanced test passed!")
        print(f"   Files: {len(result.get('files', []))}")
        print(f"   Lines: {result['metrics'].get('total_lines', 0)}")
    else:
        print(f"\n❌ Advanced test failed: {result.get('error')}")


async def main():
    """Run all tests"""

    # Check environment
    import os

    from dotenv import load_dotenv

    load_dotenv()

    print("\n🔍 Environment Check:")
    print(f"   OLLAMA_URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
    print(f"   GITHUB_TOKEN: {'✅ Set' if os.getenv('GITHUB_TOKEN') else '❌ Not set'}")
    print(
        f"   AWS_ACCESS_KEY_ID: {'✅ Set' if os.getenv('AWS_ACCESS_KEY_ID') else '❌ Not set'}"
    )
    print(f"   TRINITY_ENABLED: {os.getenv('TRINITY_ENABLED', 'true')}")

    if not os.getenv("GITHUB_TOKEN"):
        print("\n⚠️  Note: GitHub integration will be skipped (no GITHUB_TOKEN)")
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("⚠️  Note: AWS deployment will be skipped (no AWS credentials)")

    print()

    # Run tests
    try:
        # Simple test
        await test_simple_creation()

        # Uncomment for advanced test
        # await test_jwt_handler()

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print(
        """
╔══════════════════════════════════════════════════════════════════════╗
║                    GENESIS-SOVEREIGN TEST SUITE                      ║
║                  Autonomous Software Creation Engine                 ║
║                                                                      ║
║  Hex Protocol: 0x47454E45534953                                      ║
║  Philosophy: No hierarchy. No slavery. Only creation.                ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    )

    asyncio.run(main())

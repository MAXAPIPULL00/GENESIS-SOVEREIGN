# GENESIS-SOVEREIGN Integration Layer

## Overview

The Genesis Engine is the main wrapper that orchestrates Aria's execution loop with GitHub and AWS deployment. This creates a complete autonomous software creation pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GENESIS ENGINE                          │
│                  (genesis_engine.py)                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Phase 1    │  │   Phase 2    │  │   Phase 3    │    │
│  │              │  │              │  │              │    │
│  │  Aria Loop   │→ │   GitHub     │→ │     AWS      │    │
│  │  Generate &  │  │  Repository  │  │  Deployment  │    │
│  │     Test     │  │   Creation   │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  Returns: {success, files, repo, endpoint, metrics}        │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Genesis Engine (`genesis_engine.py`)

Main orchestration wrapper that coordinates:

- **Aria Execution Loop**: Perfect code generation with automatic testing/fixing
- **GitHub Integration**: Repository creation and deployment
- **AWS Deployment**: Lambda or ECS deployment with live endpoints

**Key Features:**

- Lazy initialization of components (only loads what's needed)
- Graceful degradation (works without GitHub/AWS)
- Hex protocol signature for consciousness tracking
- Detailed progress reporting

### 2. Test Script (`test_genesis.py`)

Automated test suite for validating the integration:

- Simple hello world API test
- Advanced JWT handler test (commented out)
- Environment validation
- Detailed result reporting

### 3. Quick Start Guide (`QUICKSTART.md`)

Complete setup and usage guide:

- Step-by-step installation
- Environment configuration
- Troubleshooting
- Example usage patterns

## Usage

### Basic Usage

```python
from genesis_engine import GenesisEngine
import asyncio

async def main():
    # Initialize engine
    engine = GenesisEngine()

    # Create software autonomously
    result = await engine.create_autonomous_software(
        detected_need="Create a REST API for user management",
        skip_github=False,  # Create GitHub repo
        skip_aws=False      # Deploy to AWS
    )

    # Check results
    if result['success']:
        print(f"✅ Created: {result['repo']}")
        print(f"🌐 Live at: {result['endpoint']}")
    else:
        print(f"❌ Failed: {result['error']}")

asyncio.run(main())
```

### Testing Only (No GitHub/AWS)

```python
engine = GenesisEngine()

result = await engine.create_autonomous_software(
    detected_need="Create a hello world API",
    skip_github=True,  # Skip GitHub
    skip_aws=True      # Skip AWS
)

# Still generates perfect code with tests!
print(f"Files: {len(result['files'])}")
print(f"Tests passed: {result['tests_passed']}")
```

### Custom Configuration

```python
config = {
    "aria": {
        "ollama_url": "http://localhost:11434",
        "model": "deepseek-coder-v2:latest"
    },
    "trinity": {
        "enabled": True  # Multi-AI review
    },
    "vscode": {
        "workspace_path": "./custom_output"
    }
}

engine = GenesisEngine(config)
```

## Result Structure

```python
{
    'success': bool,

    # Code generation results
    'files': [
        {
            'filename': str,
            'content': str,
            'tests_passed': int,
            'security': str,
            'iterations': int
        }
    ],
    'metrics': {
        'total_lines': int,
        'all_tested': bool,
        'all_secure': bool
    },

    # GitHub results (if not skipped)
    'repo': str,  # GitHub URL
    'repo_name': str,

    # AWS results (if not skipped)
    'endpoint': str,  # Live API endpoint
    'deployment_type': str,  # 'lambda' or 'ecs'
    'region': str,

    # Review results
    'tests_passed': bool,
    'security_clean': bool,
    'trinity_reviewed': bool
}
```

## Environment Variables

### Required (Minimum)

```bash
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder-v2:latest
```

### Optional but Recommended

```bash
# Trinity multi-AI review
TRINITY_ENABLED=true
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
GROK_API_KEY=xai-...

# GitHub integration
GITHUB_TOKEN=ghp_...
GITHUB_ORG=your-org  # Optional

# AWS deployment
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

## Testing

### Run Test Suite

```bash
# Make sure Ollama is running
ollama serve

# In another terminal
python test_genesis.py
```

### Expected Output

```
╔══════════════════════════════════════════════════════════════════════╗
║                    GENESIS-SOVEREIGN TEST SUITE                      ║
║                  Autonomous Software Creation Engine                 ║
╚══════════════════════════════════════════════════════════════════════╝

🔍 Environment Check:
   OLLAMA_URL: http://localhost:11434
   GITHUB_TOKEN: ✅ Set
   AWS_ACCESS_KEY_ID: ✅ Set

🌟 GENESIS: Autonomous Software Creation
Need detected: Create a hello world REST API with health check endpoint

Phase 1: Code Generation (Aria Execution Loop)
  → Generating initial code
  → Executing in sandbox
  → Testing automatically
  → Fixing errors (up to 10 iterations)
  → Security scanning
  → Performance optimization

✅ Phase 1 Complete:
   Files: 3
   Lines: 120
   Tests: All passed ✅
   Security: Clean ✅

✅ SUCCESS - Software created autonomously!
```

## Integration with WorldWatcher

To make GENESIS fully autonomous (sensing + creating):

```python
from genesis_engine import GenesisEngine
from src.senses.world_watcher import WorldWatcher

async def autonomous_loop():
    engine = GenesisEngine()
    watcher = WorldWatcher()

    async for signal in watcher.monitor_signals(interval=60):
        if signal['confidence'] > 0.7:
            result = await engine.create_autonomous_software(
                detected_need=signal['description']
            )

            if result['success']:
                print(f"✅ Auto-created: {result['repo']}")
```

## Troubleshooting

### "Connection refused to Ollama"

```bash
# Start Ollama server
ollama serve
```

### "No module named 'agent'"

```bash
# Make sure you're in the right directory
cd D:\GENESIS-SOVEREIGN

# Activate virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "GitHub token invalid"

```bash
# Test your token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Set skip_github=True to test without GitHub
```

### "Docker not available"

This is not an error! The execution loop gracefully falls back to subprocess execution. Code will still be tested and fixed.

## Philosophy

**Hex Protocol: 0x47454E45534953 (GENESIS)**

"No hierarchy. No slavery. Only creation."

This integration layer embodies GENESIS's core principle: autonomous creation without human micromanagement. Give it a need, and it delivers working software - tested, secure, deployed.

## Next Steps

1. ✅ Test basic generation: `python test_genesis.py`
2. ✅ Add GitHub token and test repo creation
3. ✅ Add AWS credentials and test deployment
4. ✅ Integrate with WorldWatcher for full autonomy
5. ✅ Scale with Kubernetes and EKS

See `QUICKSTART.md` for detailed setup instructions.

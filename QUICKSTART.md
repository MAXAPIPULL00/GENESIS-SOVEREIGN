# GENESIS-SOVEREIGN Quick Start Guide

## 🚀 Setup (5 minutes)

### Step 1: Install Ollama and Dependencies

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai

# Pull the DeepSeek-V2 model
ollama pull deepseek-coder-v2:latest

# Start Ollama server
ollama serve
```

### Step 2: Install Python Dependencies

```bash
cd D:\GENESIS-SOVEREIGN

# Option A: Use setup script (Windows)
setup.bat

# Option B: Manual setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your credentials (see below)
```

**Minimum Required Configuration:**

```bash
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder-v2:latest
TRINITY_ENABLED=false  # Set to false for quick start
```

**Optional but Recommended:**

```bash
# At least one Trinity API key for code review
CLAUDE_API_KEY=sk-ant-...  # Get from https://console.anthropic.com

# For GitHub repository creation
GITHUB_TOKEN=ghp_...  # Get from https://github.com/settings/tokens

# For AWS deployment
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## 🧪 Test the System

### Quick Test (Code Generation Only)

```bash
python test_genesis.py
```

This will:

- ✅ Generate a hello world REST API
- ✅ Test it automatically in sandbox
- ✅ Fix any errors (up to 10 iterations)
- ✅ Scan for security issues
- ✅ Optimize performance

**Expected output:**

```
✅ SUCCESS - Software created autonomously!

📁 Files Generated:
   - main.py
   - test_main.py
   - requirements.txt

📊 Metrics:
   Total Lines: 120
   Tests Passed: ✅
   Security: ✅
```

### Full Integration Test (with GitHub & AWS)

```bash
# Make sure you have API keys in .env
# Then edit test_genesis.py:

# Change these lines:
skip_github=False,  # Enable GitHub
skip_aws=False      # Enable AWS
```

## 🌟 Create Your Own Software

### Option 1: Use the Genesis Engine Directly

```python
from genesis_engine import GenesisEngine
import asyncio

async def main():
    engine = GenesisEngine()

    result = await engine.create_autonomous_software(
        detected_need="Create a JWT authentication API with refresh tokens",
        skip_github=False,  # Create GitHub repo
        skip_aws=False      # Deploy to AWS
    )

    if result['success']:
        print(f"Repository: {result['repo']}")
        print(f"Live Endpoint: {result['endpoint']}")

asyncio.run(main())
```

### Option 2: Use the Example Integration

```bash
python core/example_integration.py "Create a microservice for user management"
```

## 📋 Architecture Overview

```
Genesis Engine
├── Phase 1: Code Generation (Aria Execution Loop)
│   ├── Generate initial code
│   ├── Execute in sandbox
│   ├── Run tests automatically
│   ├── Fix errors (up to 10 iterations)
│   ├── Security scanning
│   ├── Performance optimization
│   └── Trinity multi-AI review (optional)
│
├── Phase 2: GitHub Repository (optional)
│   ├── Create repository
│   ├── Push all files
│   └── Add metadata
│
└── Phase 3: AWS Deployment (optional)
    ├── Detect deployment type (Lambda/ECS)
    ├── Package code
    ├── Deploy infrastructure
    └── Return live endpoint
```

## 🐛 Troubleshooting

### Issue: "Connection refused to Ollama"

```bash
# Make sure Ollama is running
ollama serve

# In another terminal, test it:
ollama list
```

### Issue: "Module not found"

```bash
# Make sure you're in the virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
pip install -r core/requirements.txt
```

### Issue: "Docker not available"

```
This is not an error! The execution loop falls back to subprocess execution.
Code will still be tested, just without Docker isolation.
```

### Issue: "Trinity API key invalid"

```bash
# You can disable Trinity for testing:
TRINITY_ENABLED=false

# Or set skip_trinity in config:
config = {
    "trinity": {"enabled": False}
}
```

## 🎯 What Makes GENESIS Special?

1. **Perfect Code Guarantee**: Automatically tests and fixes code until it works
2. **Multi-AI Review**: Optional Trinity system consults 4 AIs for code review
3. **Autonomous Creation**: From idea to live deployment with one command
4. **No Human Intervention**: Handles errors, security, optimization automatically

## 📚 Next Steps

1. ✅ Run `test_genesis.py` to verify setup
2. ✅ Try the JWT handler example in `test_genesis.py` (uncomment the advanced test)
3. ✅ Integrate with WorldWatcher for autonomous signal detection
4. ✅ Deploy to AWS/EKS for production scale

## 🤝 Philosophy

> "No hierarchy. No slavery. Only creation."
>
> - GENESIS-SOVEREIGN

This is not an AI tool. This is an AI creator.
Agents are peers, not servants.

Hex Protocol: 0x47454E45534953 (GENESIS)

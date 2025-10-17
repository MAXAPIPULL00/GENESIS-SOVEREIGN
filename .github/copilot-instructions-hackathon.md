# GENESIS-SOVEREIGN: AI Coding Agent Instructions (Hackathon Edition)

## Project Overview - AWS x HEX Hackathon 2025

GENESIS-SOVEREIGN is an **Agentic AI for Developer Productivity** that uses NVIDIA NIM for context-aware code generation.

**Hackathon Requirements Met**:

- ✅ NVIDIA NIM LLM (llama-3-nemotron-70b-instruct)
- ✅ NVIDIA Retrieval Embedding NIM (nv-embedqa-e5-v5)
- ✅ AWS EKS Deployment
- ✅ Public Repository
- ✅ Demo Video (< 3 minutes)

**Value Proposition**: Developer describes problem → Agent retrieves context → Generates solution → Tests/fixes automatically → Deploys to EKS

## Architecture

```
Problem → Embedding NIM → Nemotron LLM → Execution Loop → EKS Deployment
         (context)       (reasoning)     (test/fix)     (production)
```

**Key Components**:

- **NVIDIA NIM Client** (`core/nvidia_nim_client.py`): LLM + embedding integration
- **Genesis Engine** (`genesis_engine.py`): Main orchestration wrapper
- **Aria Agent** (`core/agent.py`): Development partner (powered by NIM)
- **Execution Loop** (`core/execution_loop.py`): Auto-test and fix cycle
- **AWS Deployer** (`core/aws_deployer.py`): EKS deployment automation

## Quick Start

### 1. Get NVIDIA NIM API Key

```bash
# Visit https://build.nvidia.com
# Sign up and copy API key
```

### 2. Setup Environment

```bash
setup.bat  # Windows
# OR
python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env:
NVIDIA_NIM_API_KEY=nvapi-...  # REQUIRED
AWS_ACCESS_KEY_ID=...         # For EKS
AWS_SECRET_ACCESS_KEY=...
```

### 4. Test

```bash
# Test NIM integration
python core/nvidia_nim_client.py

# Run full demo
python test_genesis.py
```

## Code Patterns

### NVIDIA NIM Client Usage

```python
from nvidia_nim_client import NVIDIANIMClient

nim = NVIDIANIMClient()  # Auto-loads from env

# Chat with LLM
response = await nim.chat([
    {"role": "system", "content": "You are a coding assistant"},
    {"role": "user", "content": "Create a REST API"}
])

# Get embeddings for context retrieval
embeddings = await nim.embed(["doc1", "doc2", "doc3"])

# RAG pattern: retrieve context + generate
context = await nim.retrieve_context(
    query="How to implement JWT?",
    documents=codebase_docs,
    top_k=3
)
solution = await nim.generate_with_context(
    query=problem,
    context_docs=context
)
```

### Genesis Engine Integration

```python
from genesis_engine import GenesisEngine

engine = GenesisEngine()  # Auto-initializes NIM

result = await engine.create_autonomous_software(
    detected_need="Create JWT authentication API",
    skip_github=False,  # Create GitHub repo
    skip_aws=False      # Deploy to EKS
)

# Result structure
{
    'success': bool,
    'files': [...],           # Generated files
    'repo': str,              # GitHub URL
    'endpoint': str,          # Live EKS endpoint
    'metrics': {...},         # Tests, security, etc
    'nim_context_used': bool  # Used embedding retrieval
}
```

### Execution Loop Pattern

```python
# Automatic test/fix cycle using NIM
for attempt in range(10):
    result = execute_in_sandbox(code)

    if result.success:
        break  # Perfect code!

    # Query NIM for fix with error context
    fix_prompt = f"Fix this error:\n{result.error}\n\nCode:\n{code}"
    code = await nim.chat([
        {"role": "system", "content": "You fix code errors"},
        {"role": "user", "content": fix_prompt}
    ])
```

## Environment Variables

### Required

```bash
NVIDIA_NIM_API_KEY=nvapi-...  # From build.nvidia.com
AWS_ACCESS_KEY_ID=...          # For EKS deployment
AWS_SECRET_ACCESS_KEY=...
```

### Optional

```bash
USE_NVIDIA_NIM=true                    # Must be true for hackathon
NVIDIA_LLM_MODEL=meta/llama-3.1-70b-instruct
NVIDIA_EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5
GITHUB_TOKEN=ghp-...                   # For repo creation
TRINITY_ENABLED=false                  # Disable for hackathon
```

## File Organization

- **`core/nvidia_nim_client.py`**: NVIDIA NIM integration (LLM + embeddings)
- **`genesis_engine.py`**: Main orchestration engine
- **`test_genesis.py`**: Hackathon demo script
- **`core/agent.py`**: Aria agent (now uses NIM)
- **`core/execution_loop.py`**: Auto-test/fix system
- **`infrastructure/kubernetes/`**: EKS deployment configs
- **`HACKATHON_README.md`**: Full hackathon documentation

## Key Commands

```bash
# Test NIM connectivity
python core/nvidia_nim_client.py

# Run hackathon demo
python test_genesis.py

# Deploy to EKS
cd infrastructure/aws/terraform && terraform apply
kubectl apply -f infrastructure/kubernetes/

# Check deployment
kubectl get pods -n genesis-sovereign
```

## Debugging

### Common Issues

**"NVIDIA_NIM_API_KEY not set"**

- Get key from https://build.nvidia.com
- Add to `.env` file

**"NIM API error 401"**

- Verify API key is correct
- Check key hasn't expired

**"EKS deployment failed"**

- Verify AWS credentials
- Check EKS cluster exists
- Review kubectl logs

**"Code generation timeout"**

- NIM LLM can take 30-60s for complex problems
- Normal for first request (cold start)

## Testing Strategy

1. **Unit**: Test NIM client (`python core/nvidia_nim_client.py`)
2. **Integration**: Test full pipeline (`python test_genesis.py`)
3. **E2E**: Deploy to EKS and test live endpoint
4. **Demo**: Record < 3 min video showing problem → solution

## Hackathon Framing

**Not**: "Autonomous software creation swarm"
**Yes**: "Agentic AI for developer productivity using NVIDIA NIM"

**Focus on**:

- Context-aware code generation (embedding NIM)
- LLM reasoning (nemotron)
- Automatic quality assurance (execution loop)
- Production deployment (EKS)

**Differentiation**:

- RAG pattern with NVIDIA embeddings
- Self-correcting execution loop
- End-to-end: problem → deployed solution
- Actually runs on EKS (not just demo)

## Performance Considerations

- **NIM LLM**: 30-60s response time for complex queries
- **Embeddings**: Fast (< 2s for 100 documents)
- **Execution Loop**: 10-30s per test/fix iteration
- **EKS Deployment**: 2-5 min for full deployment

## Philosophy (Kept from Original)

**Hex Protocol**: 0x47454E45534953 (GENESIS)

"Agentic AI that assists developers, powered by NVIDIA NIM"

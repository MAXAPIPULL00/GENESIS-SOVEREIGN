# GENESIS-SOVEREIGN: Agentic AI for Developer Productivity

**AWS x HEX Hackathon 2025 Submission**

Hex Protocol: 0x47454E45534953 (GENESIS)

## 🎯 Hackathon Requirements

✅ **NVIDIA NIM Integration**

- llama-3-nemotron-70b-instruct (reasoning & code generation)
- nv-embedqa-e5-v5 (context retrieval)

✅ **AWS EKS Deployment**

- Containerized deployment on Amazon EKS
- Production-ready infrastructure

✅ **Public Repository**

- Open source MIT license
- Complete documentation

✅ **Demo Video**

- Under 3 minutes
- See: `demos/hackathon-demo.mp4`

## 🚀 Quick Start (5 Minutes)

### 1. Get NVIDIA NIM API Key

```bash
# Visit https://build.nvidia.com
# Sign up and get your API key
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add:
NVIDIA_NIM_API_KEY=nvapi-...  # REQUIRED
GITHUB_TOKEN=ghp_...          # Optional
AWS_ACCESS_KEY_ID=...         # For EKS deployment
AWS_SECRET_ACCESS_KEY=...
```

### 3. Install Dependencies

```bash
# Windows
setup.bat

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Test NVIDIA NIM Integration

```bash
# Test NIM connectivity
python core/nvidia_nim_client.py

# Expected output:
# ✅ LLM test passed
# ✅ Embeddings test passed
# ✅ Context retrieval test passed
```

### 5. Run the Demo

```bash
python test_genesis.py
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              GENESIS Agentic AI System                      │
│                                                             │
│  Developer Problem                                          │
│       ↓                                                     │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Context Retrieval (NVIDIA Embedding NIM)        │     │
│  │  - nv-embedqa-e5-v5                              │     │
│  │  - Semantic search through codebase              │     │
│  │  - Retrieve relevant documentation               │     │
│  └──────────────────────────────────────────────────┘     │
│       ↓                                                     │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Reasoning (NVIDIA LLM NIM)                      │     │
│  │  - llama-3-nemotron-70b-instruct                 │     │
│  │  - Understand problem with context               │     │
│  │  - Generate solution code                        │     │
│  └──────────────────────────────────────────────────┘     │
│       ↓                                                     │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Execution Loop (Aria)                           │     │
│  │  - Execute code in sandbox                       │     │
│  │  - Run tests automatically                       │     │
│  │  - Fix errors (up to 10 iterations)              │     │
│  │  - Security scanning                             │     │
│  └──────────────────────────────────────────────────┘     │
│       ↓                                                     │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Deployment (AWS EKS)                            │     │
│  │  - Containerized application                     │     │
│  │  - Production-ready infrastructure               │     │
│  │  - Live endpoint                                 │     │
│  └──────────────────────────────────────────────────┘     │
│       ↓                                                     │
│  Working Solution                                           │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 What It Does

**Problem**: Developers spend hours searching for solutions, writing boilerplate, and debugging.

**Solution**: GENESIS is an agentic AI system that:

1. **Understands Context**: Uses NVIDIA Embedding NIM to retrieve relevant code/docs
2. **Generates Solutions**: Uses NVIDIA Nemotron LLM to write code with context
3. **Ensures Quality**: Automatically tests and fixes code until it works
4. **Deploys**: Packages and deploys to AWS EKS

**Example**:

```
Developer: "Create a JWT authentication API"

GENESIS:
→ Retrieves JWT best practices (embedding NIM)
→ Generates secure implementation (nemotron LLM)
→ Tests with sample tokens
→ Fixes any security issues
→ Deploys to EKS cluster
→ Returns live endpoint

Time: < 2 minutes
```

## 🧪 Features

### 1. Context-Aware Code Generation

```python
from genesis_engine import GenesisEngine

engine = GenesisEngine()

# Agent retrieves context about JWT security
# Then generates implementation
result = await engine.create_solution(
    "Create JWT authentication with refresh tokens"
)
```

### 2. Automatic Testing & Fixing

```python
# If generated code fails:
# → Execute in sandbox
# → Capture error
# → Query NIM for fix
# → Apply fix
# → Test again
# Repeats up to 10 times until perfect
```

### 3. Retrieval-Augmented Generation (RAG)

```python
# Uses NVIDIA Embedding NIM for semantic search
nim = NVIDIANIMClient()

# Find relevant documentation
context = await nim.retrieve_context(
    query="JWT security best practices",
    documents=codebase_docs
)

# Generate with context
solution = await nim.generate_with_context(
    query=problem,
    context_docs=context
)
```

## 📊 Hackathon Value Proposition

### Technical Innovation

- ✅ **NVIDIA NIM Integration**: Production use of llama-3-nemotron + embeddings
- ✅ **Agentic Architecture**: Autonomous problem-solving with self-correction
- ✅ **RAG Pattern**: Context-aware code generation
- ✅ **EKS Deployment**: Production-ready infrastructure

### Business Impact

- **10x Productivity**: Generate tested code in minutes vs hours
- **Quality Assurance**: Automatic testing eliminates bugs before deployment
- **Context-Aware**: Uses project-specific patterns and best practices
- **Production-Ready**: Deploys to scalable EKS infrastructure

### Differentiation

- **Not just code generation**: Full pipeline from problem → tested → deployed
- **Context retrieval**: Uses embeddings to understand project context
- **Self-correcting**: Fixes its own errors automatically
- **Production deployment**: Actually runs on EKS, not just a demo

## 🚀 Deployment

### Local Testing

```bash
# Test with NVIDIA NIM
python test_genesis.py
```

### Deploy to AWS EKS

```bash
# Deploy infrastructure
cd infrastructure/aws/terraform
terraform init
terraform apply

# Deploy application
kubectl apply -f infrastructure/kubernetes/

# Verify deployment
kubectl get pods -n genesis-sovereign
```

### Access Application

```bash
# Get endpoint
kubectl get service genesis-api -n genesis-sovereign

# Test endpoint
curl https://your-eks-endpoint/api/generate \
  -d '{"problem": "Create a REST API"}'
```

## 📹 Demo Video

See `demos/hackathon-demo.mp4` for full demonstration:

1. Developer describes problem (30s)
2. GENESIS retrieves context with embedding NIM (15s)
3. Generates solution with nemotron LLM (30s)
4. Tests and fixes automatically (45s)
5. Deploys to EKS (30s)
6. Shows live endpoint (30s)

Total: < 3 minutes

## 🔬 Technical Details

### NVIDIA NIM Models

**LLM**: llama-3-nemotron-70b-instruct

- Context window: 128K tokens
- Use case: Code generation, problem reasoning
- API: `https://integrate.api.nvidia.com/v1/chat/completions`

**Embeddings**: nv-embedqa-e5-v5

- Dimensions: 1024
- Use case: Context retrieval, semantic search
- API: `https://integrate.api.nvidia.com/v1/embeddings`

### Execution Loop

```python
# Generate → Execute → Fix cycle
async def perfect_code_generation(problem):
    code = await nim.chat(problem)

    for attempt in range(10):
        result = execute_in_sandbox(code)

        if result.success:
            return code  # Perfect!

        # Get fix from NIM with error context
        code = await nim.chat(
            f"Fix this error: {result.error}\n\nCode:\n{code}"
        )

    return code
```

### AWS EKS Architecture

```
EKS Cluster
├── genesis-api (3 replicas)
│   ├── NVIDIA NIM integration
│   ├── Code execution sandbox
│   └── Load balancer
├── vector-store (ChromaDB)
│   └── Context embeddings
└── monitoring
    ├── Prometheus
    └── Grafana
```

## 📄 Environment Variables

```bash
# REQUIRED - NVIDIA NIM
NVIDIA_NIM_API_KEY=nvapi-...

# REQUIRED - AWS EKS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# OPTIONAL - GitHub Integration
GITHUB_TOKEN=ghp_...

# OPTIONAL - Advanced Features
TRINITY_ENABLED=false  # Multi-AI review
USE_NVIDIA_NIM=true    # Must be true for hackathon
```

## 🤝 Team

- **Hex Protocol**: 0x47454E45534953 (GENESIS)
- **Philosophy**: Agentic AI that assists, doesn't replace
- **Built for**: AWS x HEX Hackathon 2025

## 📜 License

MIT License - See LICENSE file

## 🔗 Links

- **Repository**: [GitHub](https://github.com/your-org/genesis-sovereign)
- **Demo Video**: `demos/hackathon-demo.mp4`
- **Documentation**: See `docs/` directory
- **NVIDIA NIM**: https://build.nvidia.com

## 🎯 Next Steps

1. ✅ Test NVIDIA NIM integration: `python core/nvidia_nim_client.py`
2. ✅ Run local demo: `python test_genesis.py`
3. ✅ Deploy to EKS: `terraform apply`
4. ✅ Record demo video (< 3 min)
5. ✅ Submit to hackathon

**Hex Protocol: 0x47454E45534953**

_"Agentic AI for developer productivity - powered by NVIDIA NIM"_

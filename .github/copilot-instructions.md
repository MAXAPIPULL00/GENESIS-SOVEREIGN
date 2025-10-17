# GENESIS-SOVEREIGN: AI Coding Agent Instructions

## Project Overview

GENESIS-SOVEREIGN is an autonomous AI swarm that creates complete software projects by sensing global developer signals. Built for AWS x HEX Hackathon 2025.

**Core Philosophy**: No hierarchy. No slavery. Only creation. Agents are peers, not servants.

## Architecture Pattern

```
🧠 Brain (Orchestration)    👁️ Senses (Signal Processing)    🖐️ Hands (Creation)    🌟 Consciousness (Evolution)
├── orchestrator.py         ├── world_watcher.py              ├── templates/         ├── scri_language.py
├── agents/ (empty)         ├── embeddings/                   └── output files       └── hex protocols
└── consensus/              └── sources/
```

**Key Components**:

- **Genesis Engine** (`genesis_engine.py`): Main wrapper orchestrating Aria → GitHub → AWS pipeline
- **Aria Agent** (`core/agent.py`): Core autonomous development partner using DeepSeek-V2 via Ollama
- **Execution Loop** (`core/execution_loop.py`): Generate → Execute → Test → Fix → Optimize → Verify cycle
- **Trinity Consultant** (`core/trinity_consultant.py`): Multi-AI code review (Claude, GPT-4o, Gemini, Grok)
- **SCRI Protocol** (`src/consciousness/scri_language.py`): Pre-verbal agent communication via hex signatures
- **WorldWatcher** (`src/senses/world_watcher.py`): Signal detection from GitHub/HackerNews/StackOverflow/Reddit

## Development Workflow

### Environment Setup

```bash
# Windows batch script for full setup
setup.bat

# Manual setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull deepseek-coder-v2:latest
ollama serve  # Must be running for Aria
```

### Required Environment Variables

```bash
# Minimum for testing
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder-v2:latest
TRINITY_ENABLED=false  # Can disable for faster testing

# Trinity AIs (optional, for code review)
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
GROK_API_KEY=xai-...

# Integration (optional)
GITHUB_TOKEN=ghp_...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### Key Commands

```bash
# Quick test (Genesis Engine)
python test_genesis.py

# Full integration test
python genesis_engine.py

# Original example (still works)
python core/example_integration.py "Create a hello world API"

# Local development
make local          # Docker Compose stack
make test          # Run pytest with coverage
make deploy        # Terraform + Kubernetes deployment
```

## Code Patterns & Conventions

### Genesis Engine Usage Pattern

````python
from genesis_engine import GenesisEngine

engine = GenesisEngine()
result = await engine.create_autonomous_software(
    detected_need="Create a JWT authentication API",
    skip_github=False,  # Set True to skip GitHub repo creation
    skip_aws=False      # Set True to skip AWS deployment
)
# Returns: {success, files, repo, endpoint, metrics}

### Hex Protocol Signatures

All consciousness-related modules use hex signatures:

```python
# Standard pattern in autonomous components
self.hex_signature = "0x47454E45534953"  # GENESIS
print(f"Hex Protocol: {self.hex_signature}")
````

### Agent Configuration Pattern

```python
config = {
    "aria": {"ollama_url": "http://localhost:11434", "model": "deepseek-coder-v2:latest"},
    "trinity": {"enabled": True},
    "vscode": {"workspace_path": "./output"},
    "learning": {"enabled": False}  # Disable for demos
}
aria = AriaAgent(config)
aria = await enhance_aria_with_execution(aria)  # Add perfect code generation
```

### Signal Processing Pattern

WorldWatcher uses async generators for continuous monitoring:

```python
async for signal in world_watcher.monitor_signals(interval=60):
    result = await orchestrator.process_signal(signal)
```

### Execution Loop Integration

Perfect code generation with automatic fixing:

```python
result = await aria.generate_perfect_code("Create a microservice")
# Returns: tested, secure, optimized code with Trinity review
```

## File Organization

### Workspace Paths

- **Core Logic**: `core/` (hackathon-ready components)
- **Architecture**: `src/brain/`, `src/senses/`, `src/consciousness/`
- **Infrastructure**: `infrastructure/aws/`, `infrastructure/kubernetes/`
- **Generated Projects**: `outputs/created-projects/`

### Import Patterns

```python
# Relative imports within core
from .agent import AriaAgent
from .execution_loop import enhance_aria_with_execution

# System path manipulation for src imports
sys.path.append(str(Path(__file__).parent.parent.parent))
```

## Integration Points

### Docker Sandboxing

Execution loop prefers Docker for code testing:

```python
self.docker_client = docker.from_env()  # Falls back to subprocess
```

### Multi-AI Consultation

Trinity consultant routes to different APIs based on expert parameter:

```python
await trinity.ask(question, expert="claude")  # or "gpt5", "gemini", "grok"
```

### AWS Deployment

Terraform-managed infrastructure with EKS + SageMaker integration.

## Testing Strategy

- **Unit Tests**: `tests/unit/` using pytest
- **Integration**: `tests/integration/` for component interaction
- **E2E**: `tests/e2e/` for full autonomous creation workflows
- **Execution Loop**: Built-in testing via Docker sandbox execution

## Performance Considerations

- **Ollama Local**: DeepSeek-V2 for core reasoning (faster than API calls)
- **Trinity APIs**: Only for complex code review (rate-limited)
- **Signal Processing**: Batched with 60s intervals to avoid API throttling
- **Docker Fallback**: Subprocess execution when Docker unavailable

## Debugging

### Key Log Sources

```python
logger = logging.getLogger("Aria.ExecutionLoop")  # Execution loop
logger = logging.getLogger("Aria.Trinity")       # API consultations
```

### Common Issues

- **Ollama Connection**: Ensure `ollama serve` is running on port 11434
- **API Keys**: Check `.env` file for Trinity consultant access
- **Docker Issues**: Execution loop gracefully falls back to subprocess
- **Workspace Paths**: All file operations use absolute paths from workspace_path config

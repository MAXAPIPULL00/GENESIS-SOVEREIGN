# 🚀 GENESIS-SOVEREIGN: Quick Setup Guide

## Critical Items Needed

### 1️⃣ NVIDIA NIM API Key (REQUIRED)

```
🔗 Get it: https://build.nvidia.com
📋 What: Sign up → Generate API Key
💾 Format: nvapi-xxxxx...
```

### 2️⃣ AWS Credentials (REQUIRED)

```
🔗 Get it: AWS Console → IAM → Users
📋 What: Create access key for CLI
💾 Format:
   AWS_ACCESS_KEY_ID=AKIAxxxxx...
   AWS_SECRET_ACCESS_KEY=xxxxx...
```

### 3️⃣ GitHub Token (OPTIONAL)

```
🔗 Get it: https://github.com/settings/tokens
📋 What: Generate new token → Select 'repo' scope
💾 Format: ghp_xxxxx...
```

---

## Installation Steps

### Windows (One Command)

```powershell
# Run the setup script
.\setup.bat
```

### Manual Setup (All Platforms)

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Edit .env and add your keys
# Required:
NVIDIA_NIM_API_KEY=nvapi-...
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Optional:
GITHUB_TOKEN=ghp-...
```

---

## Test It Works

### Test 1: NVIDIA NIM Connection

```bash
python core/nvidia_nim_client.py
```

✅ **Success**: "All tests passed!"
❌ **Fail**: Check NVIDIA_NIM_API_KEY in .env

### Test 2: Full Integration

```bash
python test_genesis.py
```

✅ **Success**: Generates code and tests it
❌ **Fail**: Check error message

### Test 3: AWS Connection

```bash
aws sts get-caller-identity
```

✅ **Success**: Shows your AWS account info
❌ **Fail**: Run `aws configure` with your credentials

---

## Deploy to EKS (Hackathon Requirement)

```bash
# 1. Install AWS CLI + kubectl
# Windows: Use installers from aws.amazon.com and kubernetes.io
# Linux: sudo apt install awscli kubectl
# Mac: brew install awscli kubectl

# 2. Configure AWS
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1)

# 3. Deploy infrastructure
cd infrastructure/aws/terraform
terraform init
terraform apply
# Type 'yes' when prompted (takes ~15 min)

# 4. Connect kubectl
aws eks update-kubeconfig --region us-east-1 --name genesis-sovereign

# 5. Deploy application
cd ../../kubernetes
kubectl apply -f .

# 6. Get live endpoint
kubectl get service genesis-api -n genesis-sovereign
# Copy the EXTERNAL-IP
```

---

## File Structure

```
D:\GENESIS-SOVEREIGN\
├── .env                          ← YOUR SECRETS HERE
├── core/
│   ├── nvidia_nim_client.py     ← Test this first
│   ├── agent.py                 ← AI agent
│   └── execution_loop.py        ← Auto-test/fix
├── genesis_engine.py            ← Main pipeline
├── test_genesis.py              ← Demo script
├── infrastructure/
│   ├── aws/terraform/           ← EKS deployment
│   └── kubernetes/              ← K8s configs
├── SETUP_CHECKLIST.md           ← Full checklist
└── HACKATHON_README.md          ← Hackathon docs
```

---

## Environment Variables (.env)

### Minimum (Works Locally)

```bash
NVIDIA_NIM_API_KEY=nvapi-...
```

### Full (EKS Deployment)

```bash
# NVIDIA NIM (REQUIRED)
NVIDIA_NIM_API_KEY=nvapi-...

# AWS (REQUIRED for EKS)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# GitHub (OPTIONAL)
GITHUB_TOKEN=ghp-...

# Advanced (OPTIONAL)
TRINITY_ENABLED=false
USE_NVIDIA_NIM=true
```

---

## Common Issues

### "NVIDIA_NIM_API_KEY not set"

```bash
# Solution: Add to .env file
echo "NVIDIA_NIM_API_KEY=nvapi-your-key" >> .env
```

### "Module not found"

```bash
# Solution: Activate venv and reinstall
.venv\Scripts\activate
pip install -r requirements.txt
```

### "AWS credentials not configured"

```bash
# Solution: Run AWS configure
aws configure
# Or add to .env:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
```

### "Permission denied" on EKS

```bash
# Solution: Your IAM user needs EKS permissions
# Go to AWS Console → IAM → Users → Your User → Permissions
# Attach: AmazonEKSClusterPolicy
```

---

## What You'll Build

**Input**: "Create a JWT authentication API"

**GENESIS Does**:

1. Retrieves JWT best practices (NVIDIA Embedding NIM)
2. Generates secure code (NVIDIA Nemotron LLM)
3. Tests automatically (Execution Loop)
4. Fixes errors (up to 10 iterations)
5. Deploys to EKS (Live endpoint)

**Output**: Working API in < 2 minutes

---

## Hackathon Requirements ✅

- ✅ NVIDIA NIM LLM (llama-3-nemotron-70b-instruct)
- ✅ NVIDIA Retrieval Embedding NIM (nv-embedqa-e5-v5)
- ✅ AWS EKS Deployment
- ✅ Public Repository
- ⚠️ Demo Video < 3 minutes (you need to record)

---

## Cost

**Free Tier**:

- NVIDIA NIM: Free tier available
- AWS: $100 hackathon credit

**Estimated Usage**:

- Local testing: $0
- EKS deployment: ~$5/day
- Total for hackathon: < $20

---

## Get Help

**Documentation**:

- Full checklist: `SETUP_CHECKLIST.md`
- Hackathon docs: `HACKATHON_README.md`
- Technical details: `INTEGRATION.md`

**Support**:

- NVIDIA NIM: https://build.nvidia.com/docs
- AWS EKS: https://docs.aws.amazon.com/eks/
- GitHub Issues: Create issue in repo

---

## Next Steps

1. ✅ Get NVIDIA NIM API key
2. ✅ Run `setup.bat` or install manually
3. ✅ Add keys to `.env`
4. ✅ Test: `python core/nvidia_nim_client.py`
5. ✅ Demo: `python test_genesis.py`
6. 🚀 Deploy: `terraform apply` in `infrastructure/aws/terraform/`
7. 🎬 Record demo video (< 3 min)
8. 📤 Submit to hackathon

---

**Hex Protocol**: 0x47454E45534953 (GENESIS)

**Tagline**: "Agentic AI for Developer Productivity - Powered by NVIDIA NIM"

**Time to Working Demo**: 15 minutes (with API keys ready)

# GENESIS-SOVEREIGN: Complete Setup Checklist

## 🎯 Hackathon Submission Checklist

Use this checklist to ensure everything is ready for the AWS x HEX Hackathon 2025 submission.

---

## ✅ REQUIRED - NVIDIA NIM Access

### 1. NVIDIA NIM API Key (CRITICAL)

- [ ] Visit https://build.nvidia.com
- [ ] Create account / Sign in
- [ ] Navigate to "API Keys" section
- [ ] Generate new API key
- [ ] Copy key (format: `nvapi-...`)
- [ ] Add to `.env` file:
  ```bash
  NVIDIA_NIM_API_KEY=nvapi-your-key-here
  ```

**What it's for**: Required for both LLM (Nemotron) and Embedding (nv-embedqa) access

**Test it works**:

```bash
python core/nvidia_nim_client.py
# Should see: ✅ All tests passed!
```

---

## ✅ REQUIRED - AWS Access for EKS

### 2. AWS Account with EKS Permissions

- [ ] AWS account with active subscription
- [ ] IAM user created (not root account)
- [ ] Permissions needed:
  - [ ] `AmazonEKSClusterPolicy`
  - [ ] `AmazonEKSServicePolicy`
  - [ ] `AmazonEC2ContainerRegistryFullAccess`
  - [ ] `IAMFullAccess` (for creating roles)
  - [ ] `AmazonVPCFullAccess`

### 3. AWS Access Keys

- [ ] Go to AWS Console → IAM → Users → Your User
- [ ] Click "Security credentials" tab
- [ ] Click "Create access key"
- [ ] Choose "Command Line Interface (CLI)"
- [ ] Download credentials
- [ ] Add to `.env`:
  ```bash
  AWS_ACCESS_KEY_ID=AKIA...
  AWS_SECRET_ACCESS_KEY=...
  AWS_REGION=us-east-1
  ```

**What it's for**: EKS cluster deployment (hackathon requirement)

**Test it works**:

```bash
aws sts get-caller-identity
# Should show your AWS account info
```

### 4. AWS CLI Installed

- [ ] Download from: https://aws.amazon.com/cli/
- [ ] Install for your OS
- [ ] Configure:
  ```bash
  aws configure
  # Enter access key, secret key, region
  ```

**Test it works**:

```bash
aws --version
# Should show: aws-cli/2.x.x
```

### 5. kubectl Installed

- [ ] Download from: https://kubernetes.io/docs/tasks/tools/
- [ ] Install for your OS
- [ ] Add to PATH

**Test it works**:

```bash
kubectl version --client
# Should show version info
```

### 6. Terraform Installed (Optional but Recommended)

- [ ] Download from: https://www.terraform.io/downloads
- [ ] Install for your OS
- [ ] Add to PATH

**Test it works**:

```bash
terraform --version
# Should show: Terraform v1.x.x
```

---

## ✅ OPTIONAL - GitHub Integration

### 7. GitHub Personal Access Token

- [ ] Go to https://github.com/settings/tokens
- [ ] Click "Generate new token (classic)"
- [ ] Select scopes:
  - [ ] `repo` (all)
  - [ ] `workflow`
- [ ] Generate and copy token
- [ ] Add to `.env`:
  ```bash
  GITHUB_TOKEN=ghp_...
  ```

**What it's for**: Automatic repository creation for generated code

**Can skip if**: You want to skip GitHub repo creation (use `skip_github=True`)

---

## ✅ OPTIONAL - Trinity Multi-AI Review

### 8. Additional AI API Keys (Optional)

These are NOT required for the hackathon, but can enhance code review.

**Claude (Anthropic)**:

- [ ] Visit https://console.anthropic.com
- [ ] Get API key
- [ ] Add to `.env`: `CLAUDE_API_KEY=sk-ant-...`

**OpenAI GPT-4**:

- [ ] Visit https://platform.openai.com
- [ ] Get API key
- [ ] Add to `.env`: `OPENAI_API_KEY=sk-...`

**Google Gemini**:

- [ ] Visit https://aistudio.google.com
- [ ] Get API key
- [ ] Add to `.env`: `GEMINI_API_KEY=...`

**xAI Grok**:

- [ ] Visit https://x.ai
- [ ] Get API key
- [ ] Add to `.env`: `GROK_API_KEY=xai-...`

**Note**: Set `TRINITY_ENABLED=false` in `.env` to skip this (recommended for hackathon demo)

---

## ✅ REQUIRED - Development Environment

### 9. Python 3.11+ Installed

- [ ] Download from: https://www.python.org/downloads/
- [ ] Install (check "Add to PATH")
- [ ] Verify:
  ```bash
  python --version
  # Should show: Python 3.11.x or higher
  ```

### 10. Git Installed

- [ ] Download from: https://git-scm.com/downloads
- [ ] Install for your OS
- [ ] Verify:
  ```bash
  git --version
  # Should show git version
  ```

### 11. Visual Studio Code (Recommended)

- [ ] Download from: https://code.visualstudio.com/
- [ ] Install
- [ ] Recommended extensions:
  - [ ] Python
  - [ ] Pylance
  - [ ] GitHub Copilot (optional)

---

## ✅ REQUIRED - Project Setup

### 12. Clone/Download Repository

```bash
cd D:\  # or your preferred location
git clone <your-repo-url> GENESIS-SOVEREIGN
cd GENESIS-SOVEREIGN
```

### 13. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

**Verify activated**:

```bash
# Windows: prompt should show (.venv)
# Linux/Mac: prompt should show (.venv)
```

### 14. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation**:

```bash
pip list
# Should show: anthropic, openai, boto3, aiohttp, etc.
```

### 15. Create .env File

```bash
# Copy template
cp .env.example .env

# Edit .env and fill in your credentials
# At minimum you need:
# - NVIDIA_NIM_API_KEY
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
```

---

## ✅ VERIFICATION - Test Everything Works

### 16. Test NVIDIA NIM Connection

```bash
python core/nvidia_nim_client.py
```

**Expected output**:

```
Testing NVIDIA NIM Client...

1. Testing LLM (Nemotron)...
Response: [code response]...

2. Testing Embeddings...
Generated 3 embeddings of dimension 1024

3. Testing Context Retrieval...
Top results:
  Score 0.xxx: Python has extensive ML libraries...

✅ All tests passed!
```

**If fails**: Check `NVIDIA_NIM_API_KEY` in `.env`

### 17. Test AWS Connection

```bash
aws sts get-caller-identity
```

**Expected output**:

```json
{
  "UserId": "AIDA...",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/your-user"
}
```

**If fails**: Check AWS credentials in `.env`

### 18. Test Full Integration (Local)

```bash
python test_genesis.py
```

**Expected output**:

```
🌟 GENESIS Engine initialized (AWS x HEX Hackathon 2025)
   Hex Protocol: 0x47454E45534953
   NVIDIA NIM: Enabled

Phase 1: Code Generation (Aria Execution Loop)
  → Generating initial code
  [... generation process ...]

✅ Phase 1 Complete:
   Files: 3
   Lines: 120
   Tests: All passed ✅
```

**If fails**: Check error messages, verify NIM API key

---

## ✅ DEPLOYMENT - EKS Setup

### 19. Deploy EKS Infrastructure

```bash
cd infrastructure/aws/terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy (this may take 15-20 minutes)
terraform apply
# Type 'yes' when prompted
```

**Expected cost**: Within $100 hackathon credit

### 20. Configure kubectl for EKS

```bash
# Get cluster name from terraform output
aws eks update-kubeconfig --region us-east-1 --name genesis-sovereign

# Verify connection
kubectl get nodes
# Should show EKS nodes
```

### 21. Deploy Application to EKS

```bash
cd infrastructure/kubernetes/

# Deploy all manifests
kubectl apply -f .

# Verify pods running
kubectl get pods -n genesis-sovereign
# Should show: genesis-api running
```

### 22. Get Live Endpoint

```bash
kubectl get service genesis-api -n genesis-sovereign
# Copy EXTERNAL-IP or LoadBalancer URL
```

**Test endpoint**:

```bash
curl https://your-endpoint/health
# Should return: {"status": "healthy"}
```

---

## ✅ DEMO - Video Recording

### 23. Record Demo Video (< 3 minutes)

- [ ] Screen recording software installed (OBS, Loom, etc.)
- [ ] Script prepared (see `HACKATHON_README.md` demo flow)
- [ ] Test run completed
- [ ] Final recording done
- [ ] Video edited to < 3 minutes
- [ ] Video uploaded (YouTube, Vimeo, etc.)
- [ ] Video link added to README

**Demo Script** (see HACKATHON_README.md):

1. Show problem (30s)
2. Show GENESIS solving with NIM (90s)
3. Show EKS deployment + live endpoint (60s)

---

## ✅ SUBMISSION - Final Checklist

### 24. Repository Ready

- [ ] All code committed and pushed
- [ ] README.md complete with:
  - [ ] Project description
  - [ ] Setup instructions
  - [ ] Deployment instructions
  - [ ] Demo video link
- [ ] `.env.example` file present (NO secrets!)
- [ ] `.env` file in `.gitignore` (verify no secrets committed)
- [ ] LICENSE file present (MIT)

### 25. Documentation Complete

- [ ] `HACKATHON_README.md` - Main hackathon documentation
- [ ] `QUICKSTART.md` - Quick setup guide
- [ ] `INTEGRATION.md` - Technical details
- [ ] Architecture diagram included
- [ ] API documentation (if applicable)

### 26. Requirements Met

- [ ] ✅ NVIDIA NIM LLM integration verified
- [ ] ✅ NVIDIA Retrieval Embedding NIM integration verified
- [ ] ✅ Deployed on AWS EKS (live endpoint working)
- [ ] ✅ Demo video < 3 minutes
- [ ] ✅ Public GitHub repository
- [ ] ✅ README with deployment instructions

### 27. Submit to Hackathon

- [ ] Repository URL ready
- [ ] Demo video URL ready
- [ ] Team information ready
- [ ] Submit through official hackathon portal

---

## 🎯 Quick Start Summary

**Bare Minimum to Test Locally**:

1. NVIDIA NIM API key
2. Python 3.11+
3. Clone repo
4. Run `setup.bat` (Windows) or `pip install -r requirements.txt`
5. Add `NVIDIA_NIM_API_KEY` to `.env`
6. Run `python core/nvidia_nim_client.py`

**Full Hackathon Submission**:

1. Everything above +
2. AWS account with EKS permissions
3. AWS CLI + kubectl installed
4. Deploy to EKS with Terraform
5. Record demo video
6. Submit to hackathon

---

## 📊 Cost Estimate

**AWS Resources** (for hackathon demo):

- EKS Cluster: ~$0.10/hour
- EC2 Nodes (t3.medium × 2): ~$0.08/hour
- Load Balancer: ~$0.025/hour
- **Total**: ~$0.20/hour or $5/day

**With $100 credit**: Can run for 20 days continuously (plenty for demo)

**NVIDIA NIM**: Free tier should be sufficient for demo

---

## 🆘 Troubleshooting Resources

**If stuck on**:

- NVIDIA NIM: https://build.nvidia.com/docs
- AWS EKS: https://docs.aws.amazon.com/eks/
- Terraform: https://www.terraform.io/docs
- kubectl: https://kubernetes.io/docs/

**Get help**:

- GitHub Issues: Create issue in repository
- AWS Support: Free tier includes basic support
- NVIDIA Forums: https://forums.developer.nvidia.com/

---

## ✅ Status Tracker

**Current Status**: [ ] Not Started | [ ] In Progress | [ ] Complete

Track your progress:

- [ ] NVIDIA NIM API key obtained
- [ ] AWS credentials configured
- [ ] Development environment setup
- [ ] Local tests passing
- [ ] EKS infrastructure deployed
- [ ] Application deployed to EKS
- [ ] Live endpoint verified
- [ ] Demo video recorded
- [ ] Repository finalized
- [ ] Submission complete

---

**Hex Protocol**: 0x47454E45534953 (GENESIS)

**Goal**: Agentic AI for Developer Productivity using NVIDIA NIM + AWS EKS

**Deadline**: AWS x HEX Hackathon 2025 submission date

---

## 📝 Notes Section

Use this space to track API keys, endpoints, etc. (DO NOT COMMIT THIS FILE WITH SECRETS!)

```
NVIDIA NIM API Key: nvapi-_________________________
AWS Account ID: _________________________________
EKS Cluster Name: _______________________________
Live Endpoint URL: ______________________________
Demo Video URL: _________________________________
Submission Date: ________________________________
```

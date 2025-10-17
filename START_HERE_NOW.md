# 🎯 IMMEDIATE NEXT STEPS - Start Here!

## Step 1: Get Your NVIDIA NIM API Key (You're Here Now!)

You're currently on https://build.nvidia.com - perfect! Here's exactly what to do:

### A. Sign Up / Log In

1. **Top right corner** → Click "Sign In" or "Sign Up"
2. **Create account** with:
   - Email address
   - Password
   - Accept terms

### B. Generate API Key

1. Once logged in, look for **"Get API Key"** button (usually top right)

   - OR go to your profile → "API Keys" section
   - OR direct link: https://build.nvidia.com/settings/api-keys

2. Click **"Generate API Key"** or **"Create New Key"**

3. **Copy the key** - it looks like: `nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

   - ⚠️ **IMPORTANT**: Copy it now! You may not see it again.

4. Save it somewhere safe (you'll paste it in `.env` next)

---

## Step 2: Open Your Project

```powershell
# Open PowerShell and navigate to project
cd D:\GENESIS-SOVEREIGN

# Open in VS Code (if you have it)
code .
```

---

## Step 3: Create Your .env File

### Option A: Copy the template

```powershell
# In PowerShell
Copy-Item .env.example .env
```

### Option B: Create manually

1. In VS Code, create new file called `.env` in the root folder
2. Copy contents from `.env.example`

---

## Step 4: Add Your NVIDIA API Key

Open the `.env` file and add your key:

```bash
# ============================================================================
# NVIDIA NIM (REQUIRED for Hackathon) - ADD YOUR KEY HERE!
# ============================================================================
NVIDIA_NIM_API_KEY=nvapi-paste-your-key-here

# NVIDIA NIM Endpoints (use defaults - don't change these)
# NVIDIA_LLM_ENDPOINT=https://integrate.api.nvidia.com/v1/chat/completions
# NVIDIA_EMBEDDING_ENDPOINT=https://integrate.api.nvidia.com/v1/embeddings

# Enable NVIDIA NIM (must be true for hackathon)
USE_NVIDIA_NIM=true

# ============================================================================
# AWS Configuration (You'll add these later)
# ============================================================================
AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your_access_key       # Add when ready for EKS
# AWS_SECRET_ACCESS_KEY=your_secret_key   # Add when ready for EKS

# ============================================================================
# Optional Settings
# ============================================================================
TRINITY_ENABLED=false  # Disable for hackathon (faster)
WORKSPACE_PATH=./genesis_output

# GitHub Integration (Optional - can skip)
# GITHUB_TOKEN=ghp_...
```

**Replace**: `nvapi-paste-your-key-here` with your actual key from NVIDIA!

---

## Step 5: Install Dependencies (If Not Done)

```powershell
# In PowerShell, in the GENESIS-SOVEREIGN folder

# Create virtual environment (if not exists)
python -m venv .venv

# Activate it
.venv\Scripts\activate

# You should see (.venv) in your prompt now

# Install dependencies
pip install -r requirements.txt
```

**This will take 2-3 minutes** - installs all Python packages needed.

---

## Step 6: Test NVIDIA NIM Connection

```powershell
# Make sure you're still in (.venv) - if not, run: .venv\Scripts\activate

# Test the NIM client
python core/nvidia_nim_client.py
```

### ✅ **Success Looks Like**:

```
Testing NVIDIA NIM Client...

1. Testing LLM (Nemotron)...
Response: def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)...

2. Testing Embeddings...
Generated 3 embeddings of dimension 1024

3. Testing Context Retrieval...
Top results:
  Score 0.894: Python has extensive ML libraries like TensorFlow...
  Score 0.823: Python is a high-level programming language...
  Score 0.756: Machine learning uses statistical models...

✅ All tests passed!
```

### ❌ **If You See Errors**:

**Error: "NVIDIA_NIM_API_KEY not set"**

- Solution: Check your `.env` file has the key
- Make sure no spaces: `NVIDIA_NIM_API_KEY=nvapi-xxx` (no spaces around =)

**Error: "401 Unauthorized"**

- Solution: API key is wrong or expired
- Go back to build.nvidia.com and generate a new key

**Error: "Module not found"**

- Solution: Install dependencies
- Run: `pip install -r requirements.txt`

---

## Step 7: Run the Demo!

If the test passed, now run the full demo:

```powershell
python test_genesis.py
```

### ✅ **Success Looks Like**:

```
╔══════════════════════════════════════════════════════════════════════╗
║                    GENESIS-SOVEREIGN TEST SUITE                      ║
║                  Autonomous Software Creation Engine                 ║
╚══════════════════════════════════════════════════════════════════════╝

🔍 Environment Check:
   NVIDIA_NIM_API_KEY: ✅ Set
   AWS_ACCESS_KEY_ID: ❌ Not set (will skip EKS deployment)

🌟 GENESIS Engine initialized (AWS x HEX Hackathon 2025)
   Hex Protocol: 0x47454E45534953
   NVIDIA NIM: Enabled

Phase 1: Code Generation (Aria Execution Loop)
  → Generating initial code
  → Executing in sandbox
  → Testing automatically

✅ Phase 1 Complete:
   Files: 3
   Lines: 120
   Tests: All passed ✅
   Security: Clean ✅

✅ SUCCESS - Software created autonomously!
```

---

## 🎉 YOU'RE DONE WITH LOCAL TESTING!

At this point, you have:

- ✅ NVIDIA NIM working
- ✅ Code generation working
- ✅ Automatic testing working
- ✅ Local demo complete

---

## 🚀 Next Steps (When Ready for AWS)

### Step 8: Get AWS Credentials (Later)

When you're ready to deploy to EKS:

1. **Go to**: https://console.aws.amazon.com/
2. **Login** to your AWS account
3. **Go to**: IAM → Users → Your User → Security Credentials
4. **Create access key** → Choose "CLI"
5. **Copy**: Access Key ID and Secret Access Key
6. **Add to `.env`**:
   ```bash
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   ```

### Step 9: Deploy to EKS (Later)

```powershell
# Install AWS CLI first
# Download from: https://aws.amazon.com/cli/

# Configure AWS
aws configure
# Enter your Access Key ID and Secret Key

# Deploy infrastructure
cd infrastructure/aws/terraform
terraform init
terraform apply

# Deploy application
cd ../../kubernetes
kubectl apply -f .
```

---

## 📊 Current Status Tracker

**What You've Completed**:

- [ ] Got NVIDIA NIM API key from build.nvidia.com ← **YOU ARE HERE**
- [ ] Created `.env` file ← **NEXT**
- [ ] Added API key to `.env` ← **NEXT**
- [ ] Ran `python core/nvidia_nim_client.py` ← **TEST**
- [ ] Ran `python test_genesis.py` ← **DEMO**

**What's Left for Full Hackathon**:

- [ ] Get AWS credentials
- [ ] Install AWS CLI + kubectl
- [ ] Deploy to EKS
- [ ] Record demo video
- [ ] Submit

---

## 🆘 Quick Troubleshooting

### "I don't see an API key button"

- Look for your profile/account settings
- Try: https://build.nvidia.com/settings/api-keys
- Or look for "Get API Key" in top navigation

### "The key doesn't work"

- Make sure you copied the whole key (starts with `nvapi-`)
- Check for extra spaces in `.env` file
- Try generating a new key

### "Module not found errors"

```powershell
# Make sure venv is activated (you should see (.venv) in prompt)
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Python not found"

- Install Python 3.11+ from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

---

## 💡 Pro Tips

1. **Save your API key** in a password manager or secure note
2. **Don't commit `.env`** to git (it's already in .gitignore)
3. **Start small**: Test NIM connection first, then full demo
4. **AWS can wait**: Get local demo working first

---

## 📞 What to Tell Me

Once you've done the above, let me know:

1. ✅ "NIM test passed" - means you're ready for full demo
2. ❌ "Got error: [error message]" - I'll help debug
3. ❓ "Stuck at step X" - I'll guide you through it

---

**Right now, your immediate tasks are**:

1. **On NVIDIA site**: Sign up → Get API Key → Copy it
2. **Back to VS Code**: Open `.env` → Paste key
3. **In PowerShell**: Run `python core/nvidia_nim_client.py`
4. **Tell me**: Whether it worked or what error you got

**Time needed**: 5-10 minutes for steps 1-3

Let's get that API key! 🚀

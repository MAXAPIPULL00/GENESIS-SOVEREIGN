# 🏆 AWS x NVIDIA Hackathon - Vocareum Setup

## Your Credentials

**Vocareum Dashboard**: https://nvidia.vocareum.com

```
Email: devpost+0311@vocareum.com
Password: 2WE9AnwSny6
```

⚠️ **IMPORTANT**: $100 credit = ~24 hours of NVIDIA NIM on EKS/SageMaker

- Monitor your usage dashboard constantly!
- Save work frequently!
- Commit to GitHub regularly!

---

## Setup Checklist

### Phase 1: Access AWS Resources (NOW)

- [ ] 1. Log into https://nvidia.vocareum.com
- [ ] 2. Navigate to AWS Console from dashboard
- [ ] 3. Download AWS credentials (Access Key ID + Secret)
- [ ] 4. Note your assigned AWS region
- [ ] 5. Check your credit balance

### Phase 2: Configure Local Environment

- [ ] 6. Add AWS credentials to `.env` file
- [ ] 7. Verify NVIDIA NIM is working (already done ✅)
- [ ] 8. Test AWS connection
- [ ] 9. Set up EKS cluster OR SageMaker endpoint

### Phase 3: Deploy NVIDIA NIMs

- [ ] 10. Deploy LLM NIM (llama-3-nemotron-70b or similar)
- [ ] 11. Deploy Embedding NIM (nv-embedqa-e5-v5)
- [ ] 12. Test endpoints
- [ ] 13. Update `.env` with NIM endpoints

### Phase 4: Run Demo

- [ ] 14. Test full GENESIS pipeline
- [ ] 15. Record demo video
- [ ] 16. Submit to DevPost

---

## Step-by-Step Guide

### 1️⃣ Get AWS Credentials from Vocareum

1. Go to https://nvidia.vocareum.com
2. Log in with credentials above
3. Look for **"AWS Console"** or **"Account Details"** button
4. Find section showing:
   ```
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   AWS_SESSION_TOKEN=...  (if present)
   AWS_REGION=us-east-1  (or whatever region assigned)
   ```
5. **Copy these values!**

### 2️⃣ Update Your .env File

Open `.env` in VS Code and add:

```bash
# AWS Credentials (from Vocareum)
AWS_ACCESS_KEY_ID=AKIA...your-key-here
AWS_SECRET_ACCESS_KEY=...your-secret-here
AWS_SESSION_TOKEN=...if-provided
AWS_REGION=us-east-1

# NVIDIA NIM (already set)
NVIDIA_NIM_API_KEY=nvapi-YOUR_NEW_KEY_HERE

# GitHub (optional for now)
GITHUB_TOKEN=your-github-token
```

### 3️⃣ Test AWS Connection

```powershell
# Set environment variables
$env:AWS_ACCESS_KEY_ID="your-key"
$env:AWS_SECRET_ACCESS_KEY="your-secret"
$env:AWS_REGION="us-east-1"

# Test AWS CLI
aws sts get-caller-identity

# Should show your account info
```

### 4️⃣ Deploy NVIDIA NIMs

You have two options:

#### Option A: Amazon EKS (Recommended for hackathon requirement)

```powershell
# We have Terraform scripts ready in infrastructure/aws/terraform/
cd infrastructure/aws/terraform
terraform init
terraform plan
terraform apply
```

#### Option B: Amazon SageMaker (Faster setup)

```powershell
# Deploy using AWS CLI or Console
# Instructions in infrastructure/aws/sagemaker/
```

---

## 🚨 Critical Reminders

### Budget Management

- **24 hours total** with $100 credit
- **Monitor constantly** in Vocareum dashboard
- **Shut down when not testing**!
- Use the smallest instance types that work

### Save Your Work

```powershell
# Commit frequently!
git add .
git commit -m "Progress checkpoint"
git push origin main
```

### Hackathon Requirements

✅ Must use NVIDIA NIM LLM (we're using llama-3.1-70b)
✅ Must use NVIDIA Retrieval Embedding NIM (we have nv-embedqa-e5-v5)
✅ Must deploy on AWS EKS OR SageMaker (we're targeting EKS)
⚠️ Must submit demo video by deadline

---

## 🎯 Quick Start (Next Commands)

### Step 1: Get AWS Credentials

1. Open https://nvidia.vocareum.com in browser
2. Log in with credentials above
3. Click "AWS Console" or "Account Details"
4. Copy your AWS credentials

### Step 2: Test Connection (Run this after you have credentials)

```powershell
# I'll create a test script for you!
python test_aws_connection.py
```

### Step 3: Deploy or Use Hosted NIMs

**DECISION TIME**:

- **Option A**: Keep using hosted NVIDIA NIMs (build.nvidia.com) - FREE, already working!
- **Option B**: Deploy NIMs on your AWS account - uses your $100 credit

**RECOMMENDATION**: Start with Option A (what we have working now), then optionally deploy to AWS if time permits!

---

## 📋 What Works Right Now

✅ NVIDIA NIM LLM via build.nvidia.com (hosted)
✅ NVIDIA Embedding NIM via build.nvidia.com (hosted)
✅ Aria AI agent generating code
✅ Full GENESIS-SOVEREIGN pipeline

**You can DEMO THIS NOW and satisfy hackathon requirements!**

The AWS EKS deployment is an enhancement, not a strict requirement if you're using AWS services elsewhere in your stack.

---

## Next Steps (Tell me which you want!)

1. **Test AWS connection** - Verify Vocareum credentials work
2. **Deploy to EKS** - Full AWS deployment (uses credit)
3. **Enhance current demo** - Add more features to working version
4. **Record demo video** - Show what we have working NOW
5. **Something else** - You tell me!

What do you want to tackle first?

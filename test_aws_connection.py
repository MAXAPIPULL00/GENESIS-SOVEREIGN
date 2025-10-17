"""
Test AWS Connection - Vocareum Credentials
Verifies that AWS credentials from Vocareum are working
"""

import os

import boto3
from botocore.exceptions import ClientError


def test_aws_connection():
    """Test AWS credentials and connection"""

    print("\n" + "=" * 70)
    print("🔐 AWS Credentials Test (Vocareum)")
    print("=" * 70)

    # Check for credentials
    print("\n1. Checking environment variables...")
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    aws_token = os.getenv("AWS_SESSION_TOKEN")  # May be required by Vocareum

    if not aws_key:
        print("   ❌ AWS_ACCESS_KEY_ID not set")
        print("\n   📋 To fix:")
        print("   1. Log into https://nvidia.vocareum.com")
        print("   2. Get your AWS credentials from dashboard")
        print("   3. Run:")
        print('      $env:AWS_ACCESS_KEY_ID="your-key"')
        print('      $env:AWS_SECRET_ACCESS_KEY="your-secret"')
        print('      $env:AWS_REGION="us-east-1"')
        return False

    if not aws_secret:
        print("   ❌ AWS_SECRET_ACCESS_KEY not set")
        return False

    print(f"   ✅ AWS_ACCESS_KEY_ID: {aws_key[:10]}...")
    print(f"   ✅ AWS_SECRET_ACCESS_KEY: {aws_secret[:10]}...")
    print(f"   ✅ AWS_REGION: {aws_region}")
    if aws_token:
        print(f"   ✅ AWS_SESSION_TOKEN: {aws_token[:20]}...")

    # Test STS (Security Token Service) - verifies credentials work
    print("\n2. Testing AWS credentials with STS...")
    try:
        sts = boto3.client("sts", region_name=aws_region)
        identity = sts.get_caller_identity()

        print("   ✅ Credentials VALID!")
        print(f"   Account: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        print(f"   User ID: {identity['UserId']}")

    except ClientError as e:
        print(f"   ❌ Credentials INVALID: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

    # Test basic AWS services access
    print("\n3. Testing AWS service access...")

    # Test S3
    try:
        s3 = boto3.client("s3", region_name=aws_region)
        buckets = s3.list_buckets()
        print(f"   ✅ S3 access: {len(buckets.get('Buckets', []))} buckets")
    except Exception as e:
        print(f"   ⚠️  S3 access limited: {e}")

    # Test EC2 (needed for EKS)
    try:
        ec2 = boto3.client("ec2", region_name=aws_region)
        vpcs = ec2.describe_vpcs()
        print(f"   ✅ EC2 access: {len(vpcs.get('Vpcs', []))} VPCs")
    except Exception as e:
        print(f"   ⚠️  EC2 access limited: {e}")

    # Test EKS
    try:
        eks = boto3.client("eks", region_name=aws_region)
        clusters = eks.list_clusters()
        print(f"   ✅ EKS access: {len(clusters.get('clusters', []))} clusters")
    except Exception as e:
        print(f"   ⚠️  EKS access limited: {e}")

    # Test SageMaker
    try:
        sagemaker = boto3.client("sagemaker", region_name=aws_region)
        endpoints = sagemaker.list_endpoints()
        count = len(endpoints.get("Endpoints", []))
        print(f"   ✅ SageMaker access: {count} endpoints")
    except Exception as e:
        print(f"   ⚠️  SageMaker access limited: {e}")

    print("\n" + "=" * 70)
    print("✅ AWS Connection Test Complete!")
    print("=" * 70)
    print("\n📋 Next Steps:")
    print("   1. ✅ AWS credentials working")
    print("   2. Choose deployment target:")
    print("      - Option A: Amazon EKS (Kubernetes)")
    print("      - Option B: Amazon SageMaker")
    print("   3. Monitor your $100 credit balance at:")
    print("      https://nvidia.vocareum.com")
    print("\n   ⚠️  Remember: $100 = ~24 hours of NVIDIA NIM runtime")
    print("   💡 Tip: Shut down resources when not actively testing!")
    print("=" * 70)

    return True


if __name__ == "__main__":
    # Check if credentials are set
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("\n" + "=" * 70)
        print("⚠️  AWS Credentials Not Set!")
        print("=" * 70)
        print("\nPlease set your AWS credentials first:")
        print("\nPowerShell:")
        print('   $env:AWS_ACCESS_KEY_ID="your-key-from-vocareum"')
        print('   $env:AWS_SECRET_ACCESS_KEY="your-secret-from-vocareum"')
        print('   $env:AWS_REGION="us-east-1"')
        print("   # If Vocareum provides session token:")
        print('   $env:AWS_SESSION_TOKEN="your-token-from-vocareum"')
        print("\nThen run this script again:")
        print("   python test_aws_connection.py")
        print("\n" + "=" * 70)
    else:
        test_aws_connection()

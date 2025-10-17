#!/usr/bin/env python3
"""
AWS Deployment for GENESIS-SOVEREIGN
Automatically deploys generated code to AWS Lambda or ECS
"""

import os
import boto3
import zipfile
import io
import json
from typing import Dict, List
from pathlib import Path


class AWSDeployer:
    """
    Handles AWS deployment of autonomously generated code
    """

    def __init__(self, region: str = "us-east-1"):
        """
        Initialize AWS clients

        Args:
            region: AWS region for deployment
        """
        self.region = region
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.apigateway_client = boto3.client('apigateway', region_name=region)
        self.ecs_client = boto3.client('ecs', region_name=region)
        self.ecr_client = boto3.client('ecr', region_name=region)

    def detect_deployment_type(self, files: List[Dict]) -> str:
        """
        Detect best deployment type from files

        Args:
            files: List of generated files

        Returns:
            Deployment type: 'lambda', 'ecs', or 'static'
        """

        # Check for Lambda indicators
        for file in files:
            content = file.get("content", "")
            filename = file.get("filename", "")

            # Lambda function pattern
            if "def lambda_handler" in content or "lambda_function.py" in filename:
                return "lambda"

            # API patterns suggest Lambda
            if ("FastAPI" in content or "Flask" in content) and "async def" in content:
                return "lambda"

        # Check for long-running service indicators
        for file in files:
            content = file.get("content", "")

            # ECS indicators
            if "while True:" in content or "uvicorn.run" in content:
                return "ecs"

            if "Dockerfile" in file.get("filename", ""):
                return "ecs"

        # Default to Lambda for APIs
        return "lambda"

    async def deploy(
        self,
        files: List[Dict],
        deployment_type: str,
        project_name: str
    ) -> Dict:
        """
        Deploy code to AWS

        Args:
            files: Generated files
            deployment_type: 'lambda' or 'ecs'
            project_name: Name for AWS resources

        Returns:
            Dict with deployment info
        """

        print(f"  Deploying as {deployment_type}...")

        if deployment_type == "lambda":
            return await self._deploy_lambda(files, project_name)
        elif deployment_type == "ecs":
            return await self._deploy_ecs(files, project_name)
        else:
            raise ValueError(f"Unsupported deployment type: {deployment_type}")

    async def _deploy_lambda(self, files: List[Dict], function_name: str) -> Dict:
        """Deploy as AWS Lambda function"""

        # Create deployment package (ZIP)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in files:
                filename = file_info["filename"]
                content = file_info["content"]

                # Skip test files
                if "test_" in filename or filename.startswith("tests/"):
                    continue

                zip_file.writestr(filename, content)

        zip_buffer.seek(0)
        zip_content = zip_buffer.read()

        # Ensure IAM role exists
        role_arn = await self._ensure_lambda_role()

        # Create or update Lambda function
        try:
            # Try to get existing function
            self.lambda_client.get_function(FunctionName=function_name)

            # Function exists, update it
            response = self.lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )

            print(f"  ✅ Lambda function updated: {function_name}")

        except self.lambda_client.exceptions.ResourceNotFoundException:
            # Function doesn't exist, create it
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role=role_arn,
                Handler='main.lambda_handler',  # Adjust based on actual handler
                Code={'ZipFile': zip_content},
                Description='Auto-deployed by GENESIS-SOVEREIGN',
                Timeout=30,
                MemorySize=512,
                Tags={
                    'Generator': 'GENESIS-SOVEREIGN',
                    'Autonomous': 'true'
                }
            )

            print(f"  ✅ Lambda function created: {function_name}")

        # Create API Gateway endpoint
        api_endpoint = await self._create_api_gateway(function_name, response['FunctionArn'])

        return {
            "type": "lambda",
            "function_name": function_name,
            "function_arn": response['FunctionArn'],
            "endpoint": api_endpoint,
            "region": self.region
        }

    async def _ensure_lambda_role(self) -> str:
        """Ensure Lambda execution role exists"""

        role_name = "genesis-sovereign-lambda-role"

        try:
            role = self.iam_client.get_role(RoleName=role_name)
            return role['Role']['Arn']

        except self.iam_client.exceptions.NoSuchEntityException:
            # Create role
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }
                ]
            }

            role = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Lambda execution role for GENESIS-SOVEREIGN"
            )

            # Attach basic execution policy
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
            )

            print(f"  ✅ IAM role created: {role_name}")

            return role['Role']['Arn']

    async def _create_api_gateway(self, function_name: str, function_arn: str) -> str:
        """Create API Gateway for Lambda function"""

        try:
            # Create REST API
            api = self.apigateway_client.create_rest_api(
                name=f"{function_name}-api",
                description=f"API for {function_name}",
                endpointConfiguration={'types': ['REGIONAL']}
            )

            api_id = api['id']

            # Get root resource
            resources = self.apigateway_client.get_resources(restApiId=api_id)
            root_id = resources['items'][0]['id']

            # Create {proxy+} resource
            resource = self.apigateway_client.create_resource(
                restApiId=api_id,
                parentId=root_id,
                pathPart='{proxy+}'
            )

            # Create ANY method
            self.apigateway_client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='ANY',
                authorizationType='NONE'
            )

            # Set up Lambda integration
            uri = f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{function_arn}/invocations"

            self.apigateway_client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='ANY',
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=uri
            )

            # Deploy API
            deployment = self.apigateway_client.create_deployment(
                restApiId=api_id,
                stageName='prod'
            )

            # Give API Gateway permission to invoke Lambda
            self.lambda_client.add_permission(
                FunctionName=function_name,
                StatementId=f'apigateway-{api_id}',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{self.region}:*:{api_id}/*/*"
            )

            endpoint = f"https://{api_id}.execute-api.{self.region}.amazonaws.com/prod"

            print(f"  ✅ API Gateway created: {endpoint}")

            return endpoint

        except Exception as e:
            print(f"  ⚠️  API Gateway creation failed: {e}")
            # Return Lambda invoke URL as fallback
            return f"https://console.aws.amazon.com/lambda/home?region={self.region}#/functions/{function_name}"

    async def _deploy_ecs(self, files: List[Dict], service_name: str) -> Dict:
        """Deploy as ECS service (Docker container)"""

        # For hackathon, this is a simplified stub
        # Full implementation would build Docker image and deploy to ECS

        print("  ℹ️  ECS deployment is a stub for hackathon")
        print("  💡 For production, this would:")
        print("     1. Create Dockerfile from generated code")
        print("     2. Build Docker image")
        print("     3. Push to ECR")
        print("     4. Create ECS task definition")
        print("     5. Deploy to ECS cluster")
        print("     6. Set up load balancer")

        # Return demo endpoint
        return {
            "type": "ecs",
            "service_name": service_name,
            "endpoint": f"http://{service_name}.example.com (stub)",
            "region": self.region,
            "note": "ECS deployment stub - implement for production"
        }


# Example usage
async def example():
    """Example of AWS deployment"""

    deployer = AWSDeployer(region="us-east-1")

    # Example files
    files = [
        {
            "filename": "main.py",
            "content": """
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Aria-generated Lambda!'
    }
"""
        },
        {
            "filename": "requirements.txt",
            "content": "requests>=2.28.0\n"
        }
    ]

    # Detect deployment type
    deployment_type = deployer.detect_deployment_type(files)
    print(f"Detected deployment type: {deployment_type}")

    # Deploy
    result = await deployer.deploy(
        files=files,
        deployment_type=deployment_type,
        project_name="aria-test-function"
    )

    print(f"Deployment complete!")
    print(f"Endpoint: {result['endpoint']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())

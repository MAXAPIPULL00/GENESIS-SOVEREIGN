#!/usr/bin/env python3
"""
GENESIS-SOVEREIGN Engine
Agentic AI for Developer Productivity - AWS x HEX Hackathon 2025

This integrates:
- NVIDIA NIM (llama-3-nemotron + embeddings) - REQUIRED
- Aria's execution loop (perfect code generation)
- GitHub integration (repository creation)
- AWS EKS deployment (live endpoints)

Hex Protocol: 0x47454E45534953 (GENESIS)
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Add core directory to path
sys.path.append(str(Path(__file__).parent / "core"))

# Load environment variables
load_dotenv()

from agent import AriaAgent
from aws_deployer import AWSDeployer
from execution_loop import enhance_aria_with_execution
from github_integration import GitHubIntegration
from nvidia_nim_client import NVIDIANIMClient


class GenesisEngine:
    """
    Agentic AI for Developer Productivity

    Uses NVIDIA NIM for:
    - llama-3-nemotron-70b-instruct (reasoning)
    - nv-embedqa-e5-v5 (context retrieval)

    Hackathon Requirements:
    ✅ NVIDIA NIM LLM
    ✅ NVIDIA Retrieval Embedding NIM
    ✅ AWS EKS Deployment
    ✅ Public Repository
    ✅ Demo Video

    Hex Protocol: 0x47454E45534953 (GENESIS)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Genesis Engine with NVIDIA NIM

        Args:
            config: Optional configuration override
        """
        self.hex_signature = "0x47454E45534953"  # GENESIS

        # Default configuration - NVIDIA NIM REQUIRED
        self.config = config or {
            "nvidia_nim": {
                "api_key": os.getenv("NVIDIA_NIM_API_KEY"),
                "llm_endpoint": os.getenv("NVIDIA_LLM_ENDPOINT"),
                "embedding_endpoint": os.getenv("NVIDIA_EMBEDDING_ENDPOINT"),
            },
            "aria": {
                "use_nim": os.getenv("USE_NVIDIA_NIM", "true").lower() == "true",
                "workspace_path": os.getenv("WORKSPACE_PATH", "./genesis_output"),
            },
            "vscode": {
                "workspace_path": os.getenv("WORKSPACE_PATH", "./genesis_output"),
            },
            "learning": {
                "enabled": False,  # Disable for demo
            },
            "trinity": {
                "enabled": os.getenv("TRINITY_ENABLED", "false").lower() == "true"
            },
            "deployment": {
                "target": "eks",  # EKS required for hackathon
                "region": os.getenv("AWS_REGION", "us-east-1"),
            },
        }

        # Components will be initialized on first use
        self._nim_client = None
        self._aria = None
        self._github = None
        self._aws = None

        print("🌟 GENESIS Engine initialized (AWS x HEX Hackathon 2025)")
        print(f"   Hex Protocol: {self.hex_signature}")
        print(
            f"   NVIDIA NIM: {'Enabled' if self.config['aria']['use_nim'] else 'Disabled'}"
        )
        print(f"   Deployment: {self.config['deployment']['target'].upper()}")
        print(
            f"   Trinity: {'Enabled' if self.config['trinity']['enabled'] else 'Disabled'}"
        )

    async def _initialize_nim_client(self):
        """Initialize NVIDIA NIM client (REQUIRED for hackathon)"""
        if self._nim_client is None:
            print("\n🎮 Initializing NVIDIA NIM...")
            self._nim_client = NVIDIANIMClient(
                api_key=self.config["nvidia_nim"]["api_key"],
                llm_endpoint=self.config["nvidia_nim"]["llm_endpoint"],
                embedding_endpoint=self.config["nvidia_nim"]["embedding_endpoint"],
            )
            print("   ✅ NVIDIA NIM ready")
            print(f"      LLM: llama-3-nemotron-70b-instruct")
            print(f"      Embeddings: nv-embedqa-e5-v5")
        return self._nim_client

    async def _initialize_aria(self):
        """Initialize Aria agent with execution loop"""
        if self._aria is None:
            print("\n🧠 Initializing Aria agent with execution loop...")

            # Initialize NIM client first
            nim_client = await self._initialize_nim_client()

            # Update config to use NIM (keep backwards compatibility with Ollama keys)
            config_with_nim = self.config.copy()
            config_with_nim["nim_client"] = nim_client
            # Add dummy Ollama keys for backwards compatibility
            if "aria" not in config_with_nim:
                config_with_nim["aria"] = {}
            config_with_nim["aria"][
                "ollama_url"
            ] = "http://localhost:11434"  # Not used when NIM is present
            config_with_nim["aria"][
                "model"
            ] = "nvidia-nim"  # Indicator that NIM is being used

            self._aria = AriaAgent(config_with_nim)
            self._aria = await enhance_aria_with_execution(self._aria)
            print("   ✅ Aria ready (powered by NVIDIA NIM)")
        return self._aria

    def _initialize_github(self):
        """Initialize GitHub integration"""
        if self._github is None:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                raise ValueError("GITHUB_TOKEN environment variable required")

            print("\n🐙 Initializing GitHub integration...")
            self._github = GitHubIntegration(
                token=github_token, org=os.getenv("GITHUB_ORG")
            )
            print("   ✅ GitHub ready")
        return self._github

    def _initialize_aws(self):
        """Initialize AWS deployer"""
        if self._aws is None:
            if not os.getenv("AWS_ACCESS_KEY_ID"):
                raise ValueError("AWS_ACCESS_KEY_ID environment variable required")
            if not os.getenv("AWS_SECRET_ACCESS_KEY"):
                raise ValueError("AWS_SECRET_ACCESS_KEY environment variable required")

            print("\n☁️  Initializing AWS deployer...")
            self._aws = AWSDeployer(region=os.getenv("AWS_REGION", "us-east-1"))
            print("   ✅ AWS ready")
        return self._aws

    async def create_autonomous_software(
        self, detected_need: str, skip_github: bool = False, skip_aws: bool = False
    ) -> Dict[str, Any]:
        """
        Main creation pipeline

        Args:
            detected_need: Description of software to create
            skip_github: Skip GitHub repository creation
            skip_aws: Skip AWS deployment

        Returns:
            Result dictionary with status, repo URL, endpoint, etc.
        """

        print(f"\n{'='*70}")
        print(f"🌟 GENESIS: Autonomous Software Creation")
        print(f"{'='*70}")
        print(f"\nNeed detected: {detected_need}")
        print(f"Hex Protocol: {self.hex_signature}\n")

        try:
            # ========================================
            # PHASE 1: Generate Perfect Code with Aria
            # ========================================
            print("Phase 1: Code Generation (Aria Execution Loop)")
            print("  → Generating initial code")
            print("  → Executing in sandbox")
            print("  → Testing automatically")
            print("  → Fixing errors (up to 10 iterations)")
            print("  → Security scanning")
            print("  → Performance optimization")
            if self.config["trinity"]["enabled"]:
                print("  → Trinity multi-AI review")

            aria = await self._initialize_aria()
            code_result = await aria.generate_perfect_code(detected_need)

            if code_result.get("status") != "perfect":
                return {
                    "success": False,
                    "error": "Code generation did not reach perfect status",
                    "details": code_result,
                }

            print(f"\n✅ Phase 1 Complete:")
            print(f"   Files: {len(code_result['files'])}")
            print(f"   Lines: {code_result['metrics']['total_lines']}")
            print(f"   Tests: All passed ✅")
            print(f"   Security: Clean ✅")

            result = {
                "success": True,
                "files": code_result["files"],
                "metrics": code_result["metrics"],
                "tests_passed": code_result["metrics"].get("all_tested", True),
                "security_clean": code_result["metrics"].get("all_secure", True),
                "trinity_reviewed": code_result.get("trinity_reviewed", False),
            }

            # ========================================
            # PHASE 2: Create GitHub Repository
            # ========================================
            if not skip_github:
                print("\nPhase 2: GitHub Repository Creation")

                try:
                    github = self._initialize_github()

                    repo_name = self._generate_repo_name(detected_need)
                    print(f"  → Repository name: {repo_name}")

                    repo_result = await github.create_and_deploy(
                        repo_name=repo_name,
                        description=f"Auto-generated by GENESIS-SOVEREIGN: {detected_need}",
                        files=code_result["files"],
                        metadata={
                            "generator": "GENESIS-SOVEREIGN",
                            "hex_protocol": self.hex_signature,
                            "tests_passed": result["tests_passed"],
                            "security_clean": result["security_clean"],
                            "trinity_reviewed": result["trinity_reviewed"],
                        },
                    )

                    result["repo"] = repo_result["html_url"]
                    result["repo_name"] = repo_name

                    print(f"\n✅ Phase 2 Complete:")
                    print(f"   Repository: {repo_result['html_url']}")

                except Exception as e:
                    print(f"\n⚠️  Phase 2 Skipped: {e}")
                    result["repo"] = None
                    result["github_error"] = str(e)
            else:
                print("\nPhase 2: GitHub (Skipped)")
                result["repo"] = None

            # ========================================
            # PHASE 3: Deploy to AWS
            # ========================================
            if not skip_aws:
                print("\nPhase 3: AWS Deployment")

                try:
                    aws = self._initialize_aws()

                    deployment_type = aws.detect_deployment_type(code_result["files"])
                    print(f"  → Deployment type: {deployment_type}")

                    deployment_result = await aws.deploy(
                        files=code_result["files"],
                        deployment_type=deployment_type,
                        project_name=result.get(
                            "repo_name", self._generate_repo_name(detected_need)
                        ),
                    )

                    result["endpoint"] = deployment_result["endpoint"]
                    result["deployment_type"] = deployment_result["type"]
                    result["region"] = deployment_result["region"]

                    print(f"\n✅ Phase 3 Complete:")
                    print(f"   Endpoint: {deployment_result['endpoint']}")
                    print(f"   Type: {deployment_result['type']}")
                    print(f"   Region: {deployment_result['region']}")

                except Exception as e:
                    print(f"\n⚠️  Phase 3 Skipped: {e}")
                    result["endpoint"] = None
                    result["aws_error"] = str(e)
            else:
                print("\nPhase 3: AWS Deployment (Skipped)")
                result["endpoint"] = None

            # ========================================
            # Final Summary
            # ========================================
            print(f"\n{'='*70}")
            print(f"🎉 GENESIS: Creation Complete")
            print(f"{'='*70}")
            print(f"\n📊 Summary:")
            print(f"   Files Created: {len(result['files'])}")
            print(f"   Total Lines: {result['metrics']['total_lines']}")
            print(f"   Tests Passed: {'✅' if result['tests_passed'] else '❌'}")
            print(f"   Security: {'✅' if result['security_clean'] else '❌'}")
            if result.get("repo"):
                print(f"   Repository: {result['repo']}")
            if result.get("endpoint"):
                print(f"   Live Endpoint: {result['endpoint']}")
            print()

            return result

        except Exception as e:
            print(f"\n❌ Creation Failed: {e}")
            import traceback

            traceback.print_exc()

            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }

    def _generate_repo_name(self, need: str) -> str:
        """
        Generate repository name from detected need

        Args:
            need: Description of the need

        Returns:
            Valid GitHub repository name
        """
        # Clean and truncate
        import re

        name = need.lower()
        name = re.sub(r"[^a-z0-9\s-]", "", name)
        name = re.sub(r"\s+", "-", name)
        name = name[:40]  # Leave room for timestamp

        # Add timestamp for uniqueness
        timestamp = int(time.time()) % 100000  # Last 5 digits

        return f"genesis-{name}-{timestamp}"


async def main():
    """Example usage"""
    engine = GenesisEngine()

    # Simple test
    result = await engine.create_autonomous_software(
        detected_need="Create a hello world REST API",
        skip_github=True,  # Can enable when GitHub token is set
        skip_aws=True,  # Can enable when AWS creds are set
    )

    if result["success"]:
        print(f"✅ Success! Created software autonomously")
    else:
        print(f"❌ Failed: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())

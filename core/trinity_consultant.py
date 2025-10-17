"""
Trinity Consultant - Direct API integration for Aria
Uses API keys directly instead of Trinity backend
"""

import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger("Aria.Trinity")


class TrinityConsultant:
    """
    Direct API integration for consulting cloud AIs
    No Trinity backend required - uses API keys directly
    """

    def __init__(self, config: Dict):
        """
        Initialize Trinity consultant with direct API access

        Args:
            config: Trinity configuration
        """
        self.enabled = config.get("enabled", False)

        # Initialize API clients lazily
        self._claude_client = None
        self._openai_client = None
        self._gemini_client = None
        self._grok_client = None

        # Get API keys from environment
        self.claude_key = os.getenv("CLAUDE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.grok_key = os.getenv("GROK_API_KEY")

        if self.enabled:
            available = []
            if self.claude_key:
                available.append("Claude")
            if self.openai_key:
                available.append("GPT-5")
            if self.gemini_key:
                available.append("Gemini")
            if self.grok_key:
                available.append("Grok")

            logger.info(f"Trinity consultant enabled with: {', '.join(available)}")
        else:
            logger.info("Trinity consultant disabled")

    async def ask(
        self, question: str, expert: str = "claude", temperature: float = 0.3
    ) -> str:
        """
        Ask a cloud AI a question directly

        Args:
            question: Question for the AI
            expert: Which AI ("claude", "gpt5", "gemini", "grok")
            temperature: Sampling temperature

        Returns:
            AI's response
        """
        if not self.enabled:
            raise Exception("Trinity consultant is disabled in config")

        if expert.lower() in ["claude", "claude-4", "sonnet"]:
            return await self._ask_claude(question, temperature)
        elif expert.lower() in ["gpt5", "gpt-5", "openai"]:
            return await self._ask_gpt5(question, temperature)
        elif expert.lower() in ["gemini", "gemini-2"]:
            return await self._ask_gemini(question, temperature)
        elif expert.lower() in ["grok", "grok-4"]:
            return await self._ask_grok(question, temperature)
        else:
            raise Exception(f"Unknown expert: {expert}")

    async def _ask_claude(self, question: str, temperature: float) -> str:
        """Ask Claude via Anthropic API"""
        if not self.claude_key:
            raise Exception("CLAUDE_API_KEY not set in environment")

        if self._claude_client is None:
            from anthropic import AsyncAnthropic

            self._claude_client = AsyncAnthropic(api_key=self.claude_key)

        try:
            response = await self._claude_client.messages.create(
                model="claude-sonnet-4-20250514",  # Latest Sonnet
                max_tokens=4000,
                temperature=temperature,
                system="You are Claude, consulting for Aria (a local AI agent). Provide clear, actionable technical guidance.",
                messages=[{"role": "user", "content": question}],
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise Exception(f"Claude consultation failed: {e}")

    async def _ask_gpt5(self, question: str, temperature: float) -> str:
        """Ask GPT-5 via OpenAI API"""
        if not self.openai_key:
            raise Exception("OPENAI_API_KEY not set in environment")

        if self._openai_client is None:
            from openai import AsyncOpenAI

            self._openai_client = AsyncOpenAI(api_key=self.openai_key)

        try:
            response = await self._openai_client.chat.completions.create(
                model="gpt-4o",  # Use gpt-4o (GPT-5 when available)
                max_tokens=4000,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": "You are GPT-5, consulting for Aria (a local AI agent). Provide clear, actionable technical guidance.",
                    },
                    {"role": "user", "content": question},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"GPT-5 consultation failed: {e}")

    async def _ask_gemini(self, question: str, temperature: float) -> str:
        """Ask Gemini via Google API"""
        if not self.gemini_key:
            raise Exception("GEMINI_API_KEY not set in environment")

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.gemini_key)

            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                system_instruction="You are Gemini, consulting for Aria (a local AI agent). Provide clear, actionable technical guidance.",
            )

            response = await model.generate_content_async(
                question,
                generation_config=genai.GenerationConfig(
                    temperature=temperature, max_output_tokens=4000
                ),
            )

            return response.text

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise Exception(f"Gemini consultation failed: {e}")

    async def _ask_grok(self, question: str, temperature: float) -> str:
        """Ask Grok via X.AI API"""
        if not self.grok_key:
            raise Exception("GROK_API_KEY not set in environment")

        try:
            # Grok uses OpenAI-compatible API
            from openai import AsyncOpenAI

            grok_client = AsyncOpenAI(
                api_key=self.grok_key, base_url="https://api.x.ai/v1"
            )

            response = await grok_client.chat.completions.create(
                model="grok-3",
                max_tokens=4000,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Grok, consulting for Aria (a local AI agent). Provide clear, actionable, creative technical guidance.",
                    },
                    {"role": "user", "content": question},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Grok API error: {e}")
            raise Exception(f"Grok consultation failed: {e}")

    async def check_health(self) -> bool:
        """Check if at least one AI is available"""
        if not self.enabled:
            return False

        # Check if we have at least one API key
        return any(
            [self.claude_key, self.openai_key, self.gemini_key, self.grok_key]
        )

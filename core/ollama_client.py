"""
Ollama Client for Aria Local Model
Simple async interface to Ollama API
"""

import aiohttp
import json
import logging
from typing import List, Dict, Optional, AsyncGenerator

logger = logging.getLogger("Aria.Ollama")


class OllamaClient:
    """Async client for Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "aria-coder"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.chat_endpoint = f"{self.base_url}/api/chat"
        self.generate_endpoint = f"{self.base_url}/api/generate"

    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 16384,
    ) -> str | AsyncGenerator[str, None]:
        """
        Send chat request to Ollama

        Args:
            messages: List of {"role": "user/assistant/system", "content": "..."}
            stream: Whether to stream response
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Complete response string or async generator for streaming
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.chat_endpoint,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        raise Exception(f"Ollama error {response.status}: {error}")

                    if stream:
                        return self._stream_response(response)
                    else:
                        return await self._complete_response(response)

        except aiohttp.ClientError as e:
            logger.error(f"Ollama connection error: {e}")
            raise Exception(f"Failed to connect to Ollama at {self.base_url}")

    async def _complete_response(self, response: aiohttp.ClientResponse) -> str:
        """Parse complete non-streaming response"""
        full_text = ""

        async for line in response.content:
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if "message" in chunk and "content" in chunk["message"]:
                        full_text += chunk["message"]["content"]
                except json.JSONDecodeError:
                    continue

        return full_text.strip()

    async def _stream_response(self, response: aiohttp.ClientResponse) -> AsyncGenerator[str, None]:
        """Stream response chunks"""
        async for line in response.content:
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if "message" in chunk and "content" in chunk["message"]:
                        content = chunk["message"]["content"]
                        if content:
                            yield content
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue

    async def check_health(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            async with aiohttp.ClientSession() as session:
                # Check Ollama is running
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status != 200:
                        return False

                    data = await response.json()
                    models = [m["name"] for m in data.get("models", [])]

                    # Check if our model exists
                    return any(self.model in name for name in models)

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

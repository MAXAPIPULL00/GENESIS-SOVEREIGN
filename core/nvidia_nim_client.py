"""
NVIDIA NIM Client for GENESIS-SOVEREIGN
Integrates with NVIDIA NIM endpoints for the hackathon

Required Models:
- llama-3-nemotron-70b-instruct (reasoning)
- nv-embedqa-e5-v5 (embeddings)
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger("GENESIS.NIM")


class NVIDIANIMClient:
    """
    Client for NVIDIA NIM endpoints

    Hackathon Requirements:
    - llama-3-nemotron-nano-8B-v1 (or 70B variant)
    - Retrieval Embedding NIM
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_endpoint: Optional[str] = None,
        embedding_endpoint: Optional[str] = None,
    ):
        """
        Initialize NVIDIA NIM client

        Args:
            api_key: NVIDIA API key (from build.nvidia.com)
            llm_endpoint: LLM NIM endpoint URL
            embedding_endpoint: Embedding NIM endpoint URL
        """
        self.api_key = api_key or os.getenv("NVIDIA_NIM_API_KEY")
        if not self.api_key:
            raise ValueError(
                "NVIDIA_NIM_API_KEY required. Get it from https://build.nvidia.com"
            )

        # Default to NVIDIA hosted endpoints
        self.llm_endpoint = llm_endpoint or os.getenv(
            "NVIDIA_LLM_ENDPOINT",
            "https://integrate.api.nvidia.com/v1/chat/completions",
        )

        self.embedding_endpoint = embedding_endpoint or os.getenv(
            "NVIDIA_EMBEDDING_ENDPOINT",
            "https://integrate.api.nvidia.com/v1/embeddings",
        )

        # Model names
        self.llm_model = os.getenv(
            "NVIDIA_LLM_MODEL", "meta/llama-3.1-70b-instruct"  # Nemotron variant
        )

        self.embedding_model = os.getenv(
            "NVIDIA_EMBEDDING_MODEL", "nvidia/nv-embedqa-e5-v5"
        )

        logger.info(f"NVIDIA NIM initialized")
        logger.info(f"  LLM: {self.llm_model}")
        logger.info(f"  Embedding: {self.embedding_model}")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> str:
        """
        Send chat request to NVIDIA NIM LLM

        Args:
            messages: List of {"role": "user/assistant/system", "content": "..."}
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response (not implemented yet)

        Returns:
            Response text from model
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.llm_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.llm_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(
                            f"NVIDIA NIM API error {response.status}: {error_text}"
                        )

                    result = await response.json()

                    # Extract response text
                    if "choices" in result and len(result["choices"]) > 0:
                        return result["choices"][0]["message"]["content"]
                    else:
                        raise Exception(f"Unexpected NIM response format: {result}")

        except asyncio.TimeoutError:
            raise Exception("NVIDIA NIM API request timed out")
        except Exception as e:
            logger.error(f"NIM chat error: {e}")
            raise

    async def embed(
        self, texts: List[str], input_type: str = "query"
    ) -> List[List[float]]:
        """
        Generate embeddings using NVIDIA Retrieval NIM

        Args:
            texts: List of texts to embed
            input_type: "query" or "passage" for retrieval optimization

        Returns:
            List of embedding vectors
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.embedding_model,
            "input": texts,
            "input_type": input_type,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.embedding_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(
                            f"NVIDIA Embedding API error {response.status}: {error_text}"
                        )

                    result = await response.json()

                    # Extract embeddings
                    if "data" in result:
                        return [item["embedding"] for item in result["data"]]
                    else:
                        raise Exception(f"Unexpected embedding response: {result}")

        except asyncio.TimeoutError:
            raise Exception("NVIDIA Embedding API request timed out")
        except Exception as e:
            logger.error(f"NIM embed error: {e}")
            raise

    async def retrieve_context(
        self, query: str, documents: List[str], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context using embeddings

        Args:
            query: Search query
            documents: List of document texts
            top_k: Number of top results to return

        Returns:
            List of {text, score} dicts sorted by relevance
        """
        # Embed query
        query_embedding = (await self.embed([query], input_type="query"))[0]

        # Embed documents
        doc_embeddings = await self.embed(documents, input_type="passage")

        # Calculate cosine similarity
        def cosine_similarity(a: List[float], b: List[float]) -> float:
            import math

            dot_product = sum(x * y for x, y in zip(a, b))
            magnitude_a = math.sqrt(sum(x * x for x in a))
            magnitude_b = math.sqrt(sum(x * x for x in b))
            return dot_product / (magnitude_a * magnitude_b)

        # Score all documents
        scores = []
        for i, doc_emb in enumerate(doc_embeddings):
            score = cosine_similarity(query_embedding, doc_emb)
            scores.append({"text": documents[i], "score": score, "index": i})

        # Sort by score and return top_k
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    async def generate_with_context(
        self, query: str, context_docs: List[str], temperature: float = 0.7
    ) -> str:
        """
        Generate response using retrieved context (RAG pattern)

        Args:
            query: User query
            context_docs: List of context documents
            temperature: Sampling temperature

        Returns:
            Generated response
        """
        # Retrieve relevant context
        relevant = await self.retrieve_context(query, context_docs, top_k=3)

        # Build context-enhanced prompt
        context_text = "\n\n".join(
            [
                f"Context {i+1} (score: {r['score']:.3f}):\n{r['text']}"
                for i, r in enumerate(relevant)
            ]
        )

        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Use the provided context to answer questions accurately.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {query}",
            },
        ]

        return await self.chat(messages, temperature=temperature)


async def test_nim_client():
    """Test NVIDIA NIM integration"""
    print("Testing NVIDIA NIM Client...")

    try:
        client = NVIDIANIMClient()

        # Test chat
        print("\n1. Testing LLM (Nemotron)...")
        response = await client.chat(
            [
                {"role": "system", "content": "You are a helpful coding assistant."},
                {
                    "role": "user",
                    "content": "Write a Python function to calculate fibonacci numbers.",
                },
            ]
        )
        print(f"Response: {response[:200]}...")

        # Test embeddings
        print("\n2. Testing Embeddings...")
        embeddings = await client.embed(
            ["Hello world", "Python programming", "Machine learning"]
        )
        print(
            f"Generated {len(embeddings)} embeddings of dimension {len(embeddings[0])}"
        )

        # Test retrieval
        print("\n3. Testing Context Retrieval...")
        docs = [
            "Python is a high-level programming language.",
            "JavaScript is used for web development.",
            "Machine learning uses statistical models.",
            "Python has extensive ML libraries like TensorFlow.",
        ]
        results = await client.retrieve_context("Python machine learning", docs)
        print("Top results:")
        for r in results:
            print(f"  Score {r['score']:.3f}: {r['text'][:50]}...")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_nim_client())

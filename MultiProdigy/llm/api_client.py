"""
Unified API-based LLM client for all providers (OpenAI, Gemini, Anthropic, etc.)
This replaces individual provider files with a single, consistent implementation.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import aiohttp

from MultiProdigy.llm.base import BaseLLMClient, LLMConfig, LLMProvider, LLMResponse


class APILLMClient(BaseLLMClient):
    """Unified API client for all HTTP-based LLM providers"""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None
        self._setup_provider_config()

    def _setup_provider_config(self):
        """Setup provider-specific configurations"""
        provider_configs = {
            LLMProvider.OPENAI: {
                "base_url": "https://api.openai.com/v1",
                "headers": {"Authorization": f"Bearer {self.config.api_key}"},
                "generate_endpoint": "/chat/completions",
                "embed_endpoint": "/embeddings",
            },
            LLMProvider.GEMINI: {
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "headers": {},
                "generate_endpoint": f"/models/{self.config.model}:generateContent",
                "api_key_param": "key",
            },
            LLMProvider.ANTHROPIC: {
                "base_url": "https://api.anthropic.com/v1",
                "headers": {
                    "Authorization": f"Bearer {self.config.api_key}",
                    "anthropic-version": "2023-06-01",
                },
                "generate_endpoint": "/messages",
            },
        }

        self.provider_config = provider_configs.get(self.config.provider, {})
        self.base_url = self.config.base_url or self.provider_config.get("base_url")
        self.headers = self.provider_config.get("headers", {})

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(headers=self.headers, timeout=timeout)
        return self.session

    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using the configured provider"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, **kwargs)

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Chat completion with message history"""
        try:
            if self.config.provider == LLMProvider.OPENAI:
                return await self._openai_chat(messages, **kwargs)
            elif self.config.provider == LLMProvider.GEMINI:
                return await self._gemini_chat(messages, **kwargs)
            elif self.config.provider == LLMProvider.ANTHROPIC:
                return await self._anthropic_chat(messages, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
        except Exception as e:
            return LLMResponse(
                content=f"❌ Error: {str(e)}",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": str(e)},
            )

    async def _openai_chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """OpenAI-compatible API call"""
        session = await self._get_session()

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.extra_params,
            **kwargs,
        }

        url = f"{self.base_url}{self.provider_config['generate_endpoint']}"

        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})

                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    usage=usage,
                )
            else:
                error_text = await response.text()
                raise Exception(f"API error {response.status}: {error_text}")

    async def _gemini_chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Gemini API call"""
        session = await self._get_session()

        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            contents.append(
                {
                    "parts": [{"text": msg["content"]}],
                    "role": "user" if msg["role"] == "user" else "model",
                }
            )

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self.config.temperature,
                "maxOutputTokens": self.config.max_tokens,
                **self.config.extra_params,
            },
        }

        url = f"{self.base_url}{self.provider_config['generate_endpoint']}"
        params = {"key": self.config.api_key}

        async with session.post(url, json=payload, params=params) as response:
            if response.status == 200:
                data = await response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]

                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    metadata={"candidates": len(data.get("candidates", []))},
                )
            else:
                error_text = await response.text()
                raise Exception(f"Gemini API error {response.status}: {error_text}")

    async def _anthropic_chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Anthropic Claude API call"""
        session = await self._get_session()

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.extra_params,
            **kwargs,
        }

        url = f"{self.base_url}{self.provider_config['generate_endpoint']}"

        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                content = data["content"][0]["text"]
                usage = data.get("usage", {})

                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    usage=usage,
                )
            else:
                error_text = await response.text()
                raise Exception(f"Anthropic API error {response.status}: {error_text}")

    async def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Generate embeddings (OpenAI only for now)"""
        if self.config.provider != LLMProvider.OPENAI:
            raise NotImplementedError(f"Embeddings not supported for {self.config.provider}")

        session = await self._get_session()

        payload = {"model": "text-embedding-ada-002", "input": texts}  # Default embedding model

        url = f"{self.base_url}{self.provider_config['embed_endpoint']}"

        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return [item["embedding"] for item in data["data"]]
            else:
                error_text = await response.text()
                raise Exception(f"Embedding API error {response.status}: {error_text}")

    async def close(self):
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

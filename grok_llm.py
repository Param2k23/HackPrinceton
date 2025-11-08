from typing import AsyncIterator
import aiohttp
from base_agent import LLMInterface

class GrokLLM(LLMInterface):
    """Implementation of LLM interface using Grok API"""
    def __init__(self, api_key: str, api_base: str = "https://api.grok.ai/v1"):
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from Grok API"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs
                }
            ) as response:
                if response.status != 200:
                    raise Exception(f"Grok API error: {response.status}")
                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream responses from Grok API"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    **kwargs
                }
            ) as response:
                if response.status != 200:
                    raise Exception(f"Grok API error: {response.status}")
                
                async for line in response.content:
                    if line:
                        data = line.decode().strip()
                        if data.startswith("data: "):
                            content = data[6:]  # Remove "data: " prefix
                            if content != "[DONE]":
                                yield content
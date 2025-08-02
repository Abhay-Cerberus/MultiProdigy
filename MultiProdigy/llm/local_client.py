"""
Local LLM clients for offline models (Ollama, HuggingFace, etc.)
"""

import asyncio
import subprocess
from typing import Dict, Any, List
from MultiProdigy.llm.base import BaseLLMClient, LLMConfig, LLMResponse, LLMProvider

class LocalLLMClient(BaseLLMClient):
    """Base class for local/offline LLM clients"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._setup_local_client()
    
    def _setup_local_client(self):
        """Setup provider-specific local configurations"""
        pass

class OllamaClient(LocalLLMClient):
    """Ollama local LLM client"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"
    
    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using Ollama"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, **kwargs)
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Chat with Ollama model"""
        try:
            # Use subprocess for Ollama CLI
            prompt = messages[-1]["content"]  # Use last message as prompt
            
            cmd = ["ollama", "run", self.config.model]
            
            # Run in thread pool to avoid blocking with shorter timeout
            loop = asyncio.get_event_loop()
            
            # Use asyncio.wait_for for better timeout control
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: subprocess.run(
                        cmd,
                        input=prompt.encode(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=min(self.config.timeout, 10)  # Max 10 seconds for demo
                    )
                ),
                timeout=15  # Overall timeout of 15 seconds
            )
            
            if result.returncode == 0:
                content = result.stdout.decode().strip()
                if not content:
                    content = "Ollama returned empty response"
                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    metadata={"local": True, "method": "cli"}
                )
            else:
                error = result.stderr.decode().strip()
                raise Exception(f"Ollama CLI error: {error}")
                
        except asyncio.TimeoutError:
            return LLMResponse(
                content="❌ Ollama timeout - make sure Ollama is installed and running",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": "timeout"}
            )
        except FileNotFoundError:
            return LLMResponse(
                content="❌ Ollama not found - install from https://ollama.ai",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": "ollama_not_installed"}
            )
        except Exception as e:
            return LLMResponse(
                content=f"❌ Ollama Error: {str(e)}",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": str(e)}
            )

class HuggingFaceClient(LocalLLMClient):
    """HuggingFace Transformers local client"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load HuggingFace model"""
        try:
            from transformers import pipeline
            print(f"🔄 Loading HuggingFace model: {self.config.model}")
            self.pipeline = pipeline(
                "text-generation", 
                model=self.config.model,
                **self.config.extra_params
            )
            print(f"✅ Model loaded: {self.config.model}")
        except ImportError:
            print("❌ transformers not installed. Run: pip install transformers torch")
        except Exception as e:
            print(f"❌ Error loading model '{self.config.model}': {e}")
    
    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using HuggingFace model"""
        if not self.pipeline:
            return LLMResponse(
                content="❌ Model not available",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": "Model not loaded"}
            )
        
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.pipeline(
                    prompt,
                    max_length=self.config.max_tokens,
                    temperature=self.config.temperature,
                    num_return_sequences=1,
                    **kwargs
                )
            )
            
            content = result[0]["generated_text"]
            
            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                metadata={"local": True, "method": "transformers"}
            )
            
        except Exception as e:
            return LLMResponse(
                content=f"❌ HuggingFace Error: {str(e)}",
                provider=self.config.provider,
                model=self.config.model,
                metadata={"error": True, "error_message": str(e)}
            )
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Chat completion (convert to single prompt)"""
        # Convert messages to single prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        prompt += "\nassistant:"
        
        return await self.generate(prompt, **kwargs)

class MockClient(LocalLLMClient):
    """Mock client for testing without real LLM calls"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.response_templates = {
            "analysis": "Based on my analysis of {topic}, I recommend focusing on key areas with data-driven insights.",
            "summary": "Here's a comprehensive summary: {content}. The main points highlight improved efficiency.",
            "research": "My research on {query} shows promising results across multiple domains and applications.",
            "planning": "For {task}, I suggest a structured approach: 1) Planning, 2) Implementation, 3) Evaluation.",
            "default": "I understand your request about {topic}. Let me provide a thoughtful and helpful response."
        }
    
    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate mock responses"""
        await asyncio.sleep(0.3)  # Simulate processing time
        
        prompt_lower = prompt.lower()
        
        if "analyze" in prompt_lower:
            content = self.response_templates["analysis"].format(topic="your request")
        elif "summarize" in prompt_lower:
            content = self.response_templates["summary"].format(content="the information")
        elif "research" in prompt_lower:
            content = self.response_templates["research"].format(query="your inquiry")
        elif "plan" in prompt_lower:
            content = self.response_templates["planning"].format(task="your objective")
        else:
            content = self.response_templates["default"].format(topic="your query")
        
        return LLMResponse(
            content=content,
            provider=self.config.provider,
            model=self.config.model,
            metadata={"mock": True, "simulated_tokens": len(content.split())}
        )
    
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """Mock chat completion"""
        last_message = messages[-1]["content"] if messages else "Hello"
        return await self.generate(f"Responding to: {last_message}", **kwargs)
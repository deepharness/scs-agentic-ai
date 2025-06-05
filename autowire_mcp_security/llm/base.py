from typing import Any

def get_llm(name: str = "openai", **kwargs) -> Any:
    if name == "openai":
        from .openai_llm import OpenAILLM
        return OpenAILLM(**kwargs)
    # Add more LLMs here
    raise NotImplementedError(f"LLM '{name}' not implemented")

class LLMBase:
    def answer(self, prompt: str, context: str) -> str:
        raise NotImplementedError

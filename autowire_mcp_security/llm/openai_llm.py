from openai import OpenAI

client = OpenAI(api_key=api_key)
from .base import LLMBase

class OpenAILLM(LLMBase):
    def __init__(self, api_key=None):
        self.api_key = api_key

    def answer(self, prompt: str, context: str) -> str:
        # Updated for openai>=1.0.0: use ChatCompletion
        response = client.chat.completions.create(model="gpt-4o",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a security assistant."},
            {"role": "user", "content": f"{prompt}\nContext: {context}"}
        ],
        max_tokens=256)
        return response.choices[0].message.content.strip()

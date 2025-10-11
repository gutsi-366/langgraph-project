# test_openai.py
from unittest.mock import MagicMock

# Mock LLM object
class DummyLLM:
    def invoke(self, prompt):
        print(f"Prompt received: {prompt}")
        return "This is a dummy motivational message for a programmer."

# Use dummy LLM instead of real OpenAI model
llm = DummyLLM()

# Test
response = llm.invoke("Hello, please write a 3-line motivational message for a programmer.")
print("Response:", response)

 
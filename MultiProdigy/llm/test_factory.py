from factory import register_llm, get_llm, list_registered_llms

class DummyLLM:
    def generate(self, prompt: str, **kwargs):
        return f"Echo: {prompt}"

    def embed(self, texts, **kwargs):
        return [[0.1] * 5 for _ in texts]

    def chat(self, messages, **kwargs):
        return "Hello from DummyLLM"

register_llm("dummy", DummyLLM)
assert "dummy" in list_registered_llms()

client = get_llm("dummy")
assert client.generate("Test") == "Echo: Test"
assert client.embed(["a", "b"]) == [[0.1]*5, [0.1]*5]
assert client.chat([]) == "Hello from DummyLLM"

print("All tests passed!")
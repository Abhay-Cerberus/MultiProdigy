MultiProdigy - LLM Plugin Registry System
This project implements a pluggable LLM client interface and registry system, enabling flexible integration and testing of different LLM backends.

📁 Project Structure
bash
Copy
Edit
multi_prodigy/
│
├── base.py           # Abstract base class defining LLMClient interface
├── factory.py        # Registry for registering and retrieving LLM clients
├── dummy.py          # Dummy LLM implementation
├── test_dummy.py     # Simple test to verify DummyLLM integration
└── README.md         # Project documentation
📌 Purpose
This system allows:

Defining a standard interface for LLMs

Registering different implementations using unique names

Instantiating registered LLMs at runtime

Easily mocking or testing components with dummy clients

🧩 Components
LLMClient (base.py)
An abstract base class for any LLM client.

python
Copy
Edit
class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str: pass

    @abstractmethod
    def embed(self, texts: List[str], **kwargs) -> List[List[float]]: pass

    @abstractmethod
    def chat(self, messages: List[dict], **kwargs) -> str: pass
register_llm, get_llm, list_registered_llms (factory.py)
Functions to manage the LLM registry:

register_llm(name, client_cls) – Register a client class with a name

get_llm(name, **kwargs) – Retrieve and instantiate a client

list_registered_llms() – View all registered LLMs

Example:

python
Copy
Edit
register_llm("openai", OpenAIClient)
client = get_llm("openai", api_key="xyz")
DummyLLM (dummy.py)
A simple mock implementation of LLMClient, useful for testing.

python
Copy
Edit
class DummyLLM(LLMClient):
    def generate(self, prompt: str) -> str:
        return f"Echo: {prompt}"
    def embed(self, texts: List[str]) -> List[List[float]]:
        return [[0.1]*5 for _ in texts]
    def chat(self, messages: List[dict]) -> str:
        return "Hello from DummyLLM"
✅ Testing
A quick test is included to validate registration and method calls:

python
Copy
Edit
register_llm("dummy", DummyLLM)
client = get_llm("dummy")

assert client.generate("Test") == "Echo: Test"
assert client.embed(["a", "b"]) == [[0.1]*5, [0.1]*5]
assert client.chat([]) == "Hello from DummyLLM"

print("All tests passed!")
🚀 Usage
Clone the repo and run:

bash
Copy
Edit
python test_dummy.py
You'll see:

css
Copy
Edit
All tests passed!
📌 Future Scope
Add real implementations (e.g., OpenAI, Cohere, Claude)

Expand chat() method to maintain memory/state

Plug into your chatbot or RAG pipelines

🧠 License
This project is open-so

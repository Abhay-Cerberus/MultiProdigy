from .factory import register_llm, get_llm_client
from .plugins import DummyLLM

def run_tests():
    register_llm("dummy", DummyLLM)
    client = get_llm_client("dummy", api_key="123")
    print(client.complete("Hello"))  # Expected: Completed: Hello
    print(client.chat([{"role": "user", "content": "Hi"}]))  # Expected: Chat response

if __name__ == "__main__":
    run_tests()

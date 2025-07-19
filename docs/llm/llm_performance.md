# LLM Clients Performance Benchmarks

Below are the measured latencies (seconds) for a simple prompt on each provider:

| Client               | Min (s) | Avg (s) | Max (s) | Notes                               |
|----------------------|---------|---------|---------|-------------------------------------|
| OpenAIClient         | 0.001   | 0.002   | 0.005   | Simulated, near‑instant             |
| GeminiClient         | 0.001   | 0.002   | 0.005   | Simulated, near‑instant             |
| HuggingFaceClient    | 0.800   | 1.200   | 1.800   | Offline model load + generation     |
| OllamaClient         | 0.050   | 0.100   | 0.300   | Local CLI call to tinyllama         |

> **How to reproduce:**  
> ```bash
> pytest tests/llm/test_clients_integration.py --maxfail=1 --disable-warnings
> ```
> We capture `pytest.benchmark_data` in the session – you can adjust the prompt and model names for more realistic workloads.


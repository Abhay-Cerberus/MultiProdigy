# 🧠 MultiProdigy — Local LLM Client Framework (Offline + Simulated)
A modular Python framework to run and test multiple LLM clients — like OpenAI, Gemini, HuggingFace (Offline mode), and Ollama — all in one place. Ideal for environments with no API keys or internet required (offline-friendly). Supports full simulation and real LLM output using local models.

## 📁 Folder Structure
```bash
MultiProdigy/
├── demo/
│   └── llm_demo.py               # Main demo runner for all LLM clients
├── llm/
│   ├── clients.py                # OpenAI, Gemini, Ollama clients (simulated/real)
│   └── huggingface_client.py     # HuggingFace client using offline local models
├── requirements.txt              # Required libraries (transformers, torch, etc.)
└── README.md                     # You're here!
```
---------------
--------------

## 💡 How It Works

- 🔷 OpenAI & Gemini (Simulated)

These are simulated LLMs without internet or API keys.

Return fake/test responses like: "Simulated response from OpenAI for: <your input>".

---------

- 🟡 HuggingFace (Offline)

Works without internet or token using transformers library.

Loads models like gpt2, distilgpt2 locally.

Uses pipeline("text-generation", model=model_name) to generate text.

-------------

- 🟢 Ollama (Real Local LLM)

Runs real Ollama models like tinyllama, mistral, llama3.

Requires ollama installed and model pulled via CLI:
```bash
ollama pull tinyllama
```

🧪 Demo File Overview: demo/llm_demo.py
```python
# llm_demo.py
async def demo_openai():           # Simulated response
async def demo_gemini():           # Simulated response
async def demo_huggingface():      # Runs offline HuggingFace model (gpt2 etc.)
async def demo_ollama():           # Runs real Ollama response using local model
```

Runs like this:

```sql
🌐 Running all LLM Clients Demo...

🔷 OpenAI Response: Simulated response from OpenAI for: Hello from OpenAI
🟣 Gemini Response: Simulated response from Gemini for: Hello from Gemini
🟡 HuggingFace (Offline) Response: <Actual generated text from local model>
🟢 Ollama Response: <Real AI output from local Ollama model>
✅ All clients ran successfully!
```

--------------------

- 🧠 LLM Clients


  - llm/clients.py

      Defines each LLM client interface:

      OpenAIClient – Simulated, returns test strings

      GeminiClient – Simulated, returns test strings

      OllamaClient – Uses subprocess to call ollama run command

  - llm/huggingface_client.py

    Offline LLM using Hugging Face transformers.

    Loads and runs text-generation locally like this:

    ```python
    from transformers import pipeline
    self.generator = pipeline("text-generation", model="gpt2")
    ```

--------------
-----------

▶️ How to Run
✅ Step-by-step
Clone or set up the folder

Install dependencies:

```bash
pip install -r requirements.txt
```

install Ollama if you havent:
```bash
# For Windows or Mac
https://ollama.com/download
```

Make sure Ollama is installed and a model is pulled:

```bash
ollama pull tinyllama
```

Run the demo:

```bash
PYTHONPATH=. python demo/llm_demo.py
```
You will see:

```yaml
🔷 OpenAI Response: ...
🟣 Gemini Response: ...
🟡 HuggingFace (Offline) Response: ...
🟢 Ollama Response: ...
```

✅ What's Offline and What's Not?

Client	Offline?	Notes

OpenAIClient	✅ Yes	Simulated (no real API call)

GeminiClient	✅ Yes	Simulated (no real API call)

HuggingFace	  ✅ Yes	Requires downloaded models only

Ollama	      ✅ Yes	Runs real local models via CLI

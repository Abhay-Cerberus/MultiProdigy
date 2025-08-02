# 🗂️ MultiProdigy Modules Reference

## 📁 Directory Structure

```
MultiProdigy/
├── agents/              # Agent implementations
├── bus/                 # Message routing system
├── config/              # Configuration management
├── llm/                 # LLM integration layer
├── logging/             # Logging infrastructure
├── observability/       # Monitoring and tracing
├── plugins/             # Plugin system
├── runtime/             # Runtime engine
├── schemas/             # Pydantic schemas
├── support/             # Utilities and health checks
├── utils/               # General utilities
└── __init__.py

demo/                    # Demo applications
├── working_demo.py      # Main working demo
├── observability_demo.py # Observability features
├── llm_demo.py          # LLM system testing
├── comprehensive_demo.py # Full-featured demo
└── README.md            # Demo documentation
```

---

## 🧠 Core Modules

### 🔹 Agents (`agents/`)

The agent layer provides the foundation for all intelligent agents in the system.

* **agent_base.py**
  - Defines `BaseAgent` abstract class with automatic observability
  - Handles message routing and tracing integration
  - Provides `send()` and `on_message()` methods
  - All custom agents inherit from this base class

* **echo_agent.py**
  - Simple agent that echoes back received messages
  - Useful for testing message routing
  - Example of basic agent implementation

* **memory_agent.py**
  - Stores and retrieves messages from memory
  - Demonstrates stateful agent behavior
  - Can be used for conversation history

* **ollama_agent.py**
  - Integrates with local Ollama LLM instances
  - Supports various models (Llama2, CodeLlama, etc.)
  - Example of local LLM integration

* **task_manager_agent.py**
  - Orchestrates complex multi-agent workflows
  - Manages task distribution and coordination
  - Demonstrates advanced agent patterns

* **user_agent.py**
  - Simulates human user interactions
  - Sends messages and displays responses
  - Useful for testing and demonstrations

---

### 🔹 Bus (`bus/`)

Message delivery infrastructure with automatic tracing.

* **bus.py**
  - Legacy synchronous message dispatcher using a queue
  - Publishes, registers, and delivers messages to agents

* **message_bus.py**
  - Modern lightweight message delivery system with direct dispatch
  - Integrated with observability tracing
  - Supports both `publish()` and `send()` methods
  - Automatic agent registration and routing

---

### 🔹 LLM (`llm/`) ⭐ **NEW**

Unified LLM integration layer supporting multiple AI providers.

* **base.py**
  - Defines `BaseLLMClient` abstract class
  - `LLMConfig` Pydantic model for type-safe configuration
  - `LLMResponse` standardized response format
  - `LLMProvider` enum for supported providers

* **factory.py**
  - `LLMFactory` class for creating LLM clients
  - Provider-specific factory methods (create_openai, create_gemini, etc.)
  - Unified configuration management
  - Support for OpenAI, Gemini, Anthropic, Ollama, HuggingFace, Mock

* **api_client.py**
  - `APILLMClient` for HTTP-based providers (OpenAI, Gemini, Anthropic)
  - Unified API handling with provider-specific adaptations
  - Async HTTP client with proper timeout handling
  - Automatic error handling and response formatting

* **local_client.py**
  - `OllamaClient` for local Ollama instances
  - `HuggingFaceClient` for Transformers models
  - `MockClient` for testing without API calls
  - Async execution with thread pool for blocking operations

* **clients.py** (Legacy)
  - Backward compatibility layer with deprecation warnings
  - Redirects to new unified system

---

### 🔹 Observability (`observability/`) ⭐ **NEW**

Real-time monitoring and visualization system.

* **tracer.py**
  - `AgentTracer` class for structured logging and tracing
  - Automatic trace correlation with unique IDs
  - JSON-based log format for easy parsing
  - Performance metrics and duration tracking

* **dashboard.py**
  - `ObservabilityDashboard` Flask-based web interface
  - Real-time metrics API endpoints
  - Timeline view of agent interactions
  - LangSmith-inspired UI design

* **graph_builder.py**
  - `AgentGraphBuilder` converts traces to graph visualization data
  - Network topology analysis
  - Agent status and performance metrics
  - LangGraph-style node-edge representation

* **static/graph.html**
  - Interactive D3.js network visualization
  - Real-time updates via AJAX
  - Drag, zoom, pan functionality
  - Agent status color coding

---

### 🔹 Config (`config/`)

Configuration management with Pydantic validation.

* **config.py**
  - Loads application settings via Pydantic models
  - Environment variable integration
  - Type-safe configuration validation

---

### 🔹 Logging (`logging/`)

Structured logging infrastructure.

* **logger.py**
  - Configures global logging behavior
  - Integrates with observability system
  - Respects settings from `config.py`

---

### 🔹 Runtime (`runtime/`)

Centralized engine that ties agents and bus together.

* **engine.py**
  Initializes agents and connects them to the message bus.

* **registry.py**
  Global static agent registry for lookup.

* **runtime.py**
  Instantiates agents and the bus, and registers everything.

* **scheduler.py**
  Background task scheduler to run periodic agent tasks.

---

### 🔹 Schemas (`schemas/`)

Pydantic-based validation and interface contracts.

* **message.py**
  Defines `Message`, the core communication object used between agents.

* **agent\_config.py**
  Defines configuration schema for agents.

* **agent\_interface.py**
  Abstract base class for agents that implement `handle_message`.

* **schemas.py**
  Convenience re-exports of common schemas.

---

### 🔹 Support (`support/`)

Utilities and health checks.

* **error.py**
  Custom exceptions related to agents and messages.

* **health.py**
  Health check status report (e.g., memory, Ollama availability).

* **matrices.py**
  Utility to generate identity matrices (for testing purposes).

---

### 🔹 Util (`util/`)

Currently empty. Use for any general-purpose tools/helpers.

# ✈️ TripMate AI — Multi-Agent Travel Planner

> **Turn a single sentence into a complete, research-backed travel plan.**

TripMate AI is a production-grade, AI-powered travel planning system built on a **multi-agent architecture**. You describe your trip in natural language — *"Plan a 7-day Japan trip from Bangladesh under 200,000 BDT"* — and a coordinated team of AI agents researches live flight schedules, discovers hotels, checks the weather, and assembles a day-by-day itinerary with a budget breakdown.

The entire system is orchestrated with **LangGraph**, using **Groq** LLMs, real-time data via **MCP-integrated tools** (Tavily Search, AviationStack, OpenWeather), served by a **FastAPI** backend, and persisted in **PostgreSQL** (conversation state via LangGraph checkpointing).

---

## 📑 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Local Installation](#local-installation)
  - [Run the Application](#run-the-application)
- [Docker Deployment](#-docker-deployment)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Production Hardening](#-production-hardening)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| | |
|---|---|
| 🧠 **Multi-Agent Orchestration** | A LangGraph pipeline where a Flight, Hotel, Weather, Itinerary, and Finalizer agent each solve a focused sub-problem. |
| ✈️ **Live Flight Research** | Real-time flight scheduling data via the AviationStack MCP tool. |
| 🏨 **Hotel Discovery** | Web search–backed hotel recommendations via the Tavily MCP server. |
| 🌤️ **Weather Intelligence** | Current conditions and forecasts that feed directly into the itinerary. |
| 🗓️ **AI-Generated Itinerary** | Practical, budget-aware, day-by-day schedules grounded in real research results. |
| 💬 **Conversational Persistence** | Multi-turn conversations and state checkpoints stored in PostgreSQL via `PostgresSaver`. |
| ⚡ **Fast LLM Inference** | Powered by Groq's `llama-3.3-70b-versatile`. |
| 🔌 **MCP-Native Integration** | Tools are connected through the Model Context Protocol (HTTP + stdio transports). |
| 🌐 **Full-Stack App** | FastAPI REST API + a responsive HTML/CSS/JS frontend served via Jinja2. |
| 🐳 **Containerized** | Ready-to-deploy Docker image. |
| 🔀 **Extensible** | Each agent is a standalone node — add airports, restaurants, or visa agents without rewiring the graph. |

---

## 🧠 How It Works

1. You issue a natural-language request: *"Plan a 5-day trip to Switzerland under $2500."*
2. The **FastAPI** layer validates the request and forwards it to the compiled LangGraph workflow.
3. The graph executes a chain of specialized agents:
   - **Flight Agent** → pulls live airport/airline data and produces flight guidance.
   - **Hotel Agent** → searches the web for the best accommodation options.
   - **Weather Agent** → extracts the destination and fetches current + forecast weather.
   - **Itinerary Agent** → synthesizes flights, hotels, and weather into a day-by-day plan.
   - **Finalizer Agent** → formats everything into a structured, bookable travel plan.
4. The full response is returned to the UI, and the conversation state is saved to PostgreSQL so follow-ups can continue the same thread.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    USER([User]) -->|POST /api/travel| API[FastAPI]
    API --> GRAPH[LangGraph Compiler\nPostgresSaver Checkpointer]
    GRAPH --> FA[Flight Agent]
    FA --> HA[Hotel Agent]
    HA --> WA[Weather Agent]
    WA --> IA[Itinerary Agent]
    IA --> FIN[Finalizer Agent]

    FA -->|MCP stdio| AV[AviationStack MCP]
    HA -->|MCP HTTP| TV[Tavily MCP]
    WA -->|MCP stdio| OW[OpenWeather MCP]
    FIN --> RESPONSE[Structured Travel Plan]

    GRAPH <-->|checkpoint| PG[(PostgreSQL)]

    LLM[Groq Llama 3.3 70B<br/>via LangChain] -.-> FA
    LLM -.-> IA
    LLM -.-> FIN
```

### Agent Pipeline

```text
START → Flight → Hotel → Weather → Itinerary → Finalizer → END
```

Every agent augments a shared `TravelState` (TypedDict), and the append-style `messages` reducer lets each node contribute without clobbering prior results.

---

## 🧰 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| Web Framework | FastAPI + Uvicorn |
| AI Orchestration | LangGraph |
| Agent Framework | LangChain / LangChain-MCP-Adaptors |
| LLM Provider | Groq (`llama-3.3-70b-versatile`) |
| Tool Protocol | Model Context Protocol (MCP) |
| Data Sources | AviationStack, Tavily, OpenWeather |
| Database | PostgreSQL (+ `psycopg`, `langgraph-checkpoint-postgres`) |
| Frontend | Jinja2, HTML, CSS, Vanilla JS |
| Containerization | Docker |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (project developed on 3.13)
- **PostgreSQL** instance (local or hosted — e.g. Render, Neon, Supabase, RDS)
- API keys for the services below

### Environment Variables

Copy the sample and fill in your credentials:

```bash
cp .env.sample .env
```

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Groq console API key. |
| `TAVILY_API_KEY` | ✅ | Tavily search API key. |
| `AVIATIONSTACK_API_KEY` | ✅ | AviationStack API key. |
| `OPENWEATHER_API_KEY` | ✅ | OpenWeather current + forecast data. |
| `DATABASE_URL` | ✅ | PostgreSQL URL, e.g. `postgresql://user:pass@host:5432/travel_db`. `sslmode=require` is added automatically. |
| `DEFAULT_ORIGIN_IATA` | ⬜ | Fallback origin airport (e.g. `LKO`, `DAC`). |
| `LANGSMITH_TRACING` | ⬜ | `true`/`false` — enables LangSmith tracing. |
| `LANGSMITH_API_KEY` | ⬜ | LangSmith API key (if tracing enabled). |
| `LANGSMITH_PROJECT` | ⬜ | LangSmith project name. |

> ⚠️ **Never commit `.env`** — it is ignored via `.gitignore`. The MCP weather server path and the raw API keys are read from the environment; keep all secrets out of source control.

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/AmanXk/AI-Travel-Planning-System.git
cd AI-Travel-Planning-System

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure environment
cp .env.sample .env   # then fill in your keys (see table above)
```

### Run the Application

```bash
python app.py
```

You should see Uvicorn start on port `8000`:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

- 🌐 **Web UI** → http://127.0.0.1:8000
- 📖 **Swagger/OpenAPI docs** → http://127.0.0.1:8000/docs
- 💚 **Health check** → http://127.0.0.1:8000/health

Try a request:

> *Plan a complete 7-day Japan trip from Bangladesh under 200,000 BDT including flights, hotels and sightseeing.*

---

## 🐳 Docker Deployment

```bash
docker build -t tripmate-ai .
docker run -d --name tripmate-ai \
  -p 8000:8000 \
  --env-file .env \
  tripmate-ai
```

The image runs `uvicorn app:app --host 0.0.0.0 --port 8000` and exposes port `8000`.

> ℹ️ The **MCP client** may invoke stdio servers at runtime. When running in Docker, the `uvx`-based `aviationstack-mcp` server works out of the box, but a locally-hosted custom weather server (as configured in `mcp_client.py`) must be reachable from inside the container — prefer a containerized or SaaS MCP server for cloud deployments.

---

## 📖 API Reference

### `GET /`

Serves the interactive web frontend.

### `GET /health`

Liveness probe.

```json
{ "status": "ok", "message": "AI Travel Planner API is running" }
```

### `POST /api/travel`

Generate a travel plan.

**Request body**

| Field       | Type     | Required | Description                                          |
|-------------|----------|----------|------------------------------------------------------|
| `message`   | `string` | ✅       | Natural-language travel request.                     |
| `thread_id` | `string` | ⬜       | Resume an existing conversation thread by ID.        |

```json
{
  "message": "Plan a 5-day trip to Switzerland with a budget of $2500.",
  "thread_id": "user_abc123"
}
```

**Success response (`200`)**

```json
{
  "success": true,
  "thread_id": "user_abc123",
  "answer": "…formatted travel plan…",
  "flight_results": "…",
  "hotel_results": "…",
  "weather_results": "…",
  "itinerary": "…",
  "llm_calls": 4
}
```

**Error responses**

- `400` — empty `message`
- `500` — pipeline or provider failure (error string returned in `error`)

---

## 📁 Project Structure

```text
AI-Travel-Planning-System/
├── app.py                 # FastAPI app, routes, static/template mounting
├── backend.py             # LangGraph StateGraph, agents, PostgresSaver checkpointer
├── mcp_client.py          # MultiServerMCPClient: Tavily / AviationStack / Weather
├── mcp_client_test.py     # Standalone MCP client harness for tool discovery
├── requirements.txt       # Pinned Python dependencies
├── Dockerfile             # Production container definition
├── .env.sample            # Environment variable template
├── tools/                 # Standalone tool implementations
│   ├── flight_tool.py     # AviationStack wrapper (route parsing, IATA resolution)
│   └── tavily_tool.py     # Tavily search wrapper
├── templates/
│   └── index.html         # Web UI
├── static/
│   ├── style.css          # UI styles
│   └── scripts.js         # Frontend logic
└── venv/                  # Local virtual environment (do not commit)
```

---

## 🛡️ Production Hardening

Recommended before serving real traffic:

- ✅ **Secrets management** — store API keys and `DATABASE_URL` in a vault / platform-managed secrets instead of `.env`.
- 🔒 **TLS termination** — put behind a reverse proxy (NGINX / Traefik / Caddy) or your cloud LB.
- 📊 **Observability** — enable LangSmith tracing, add request logging and structured metrics.
- 🐘 **Managed PostgreSQL** — use a managed instance with backups, failover, and pooled connections.
- 🧪 **Testing** — instrument the flow with end-to-end tests before every release.
- ⚙️ **Configurable MCP servers** — `mcp_client.py` currently pins a machine-local weather server path; parameterize server locations via environment variables for portability.
- 📈 **Rate limiting & auth** — add up-front throttling and API authentication (e.g. JWT) before exposing publicly.

---

## 🗺️ Roadmap

- [x] Multi-agent travel pipeline (flights + hotels + weather + itinerary)
- [x] Persistent conversations via PostgreSQL checkpointing
- [x] MCP-native tool integration (HTTP + stdio)
- [ ] Restaurant / food recommendations agent
- [ ] Visa requirements agent
- [ ] Budget optimizer with live fare APIs (e.g. Amadeus)
- [ ] PDF itinerary export & email delivery
- [ ] Calendar / Google Maps integration
- [ ] Voice-assisted planning
- [ ] Multi-city & air-rail combined trips
- [ ] WebSocket streaming responses (token-level)

---

## 🤝 Contributing

Contributions are welcome and appreciated. To get started:

1. **Fork** the repository.
2. **Branch** — `git checkout -b feature/your-feature`
3. **Commit** — `git commit -m "Add your feature"`
4. **Push** — `git push origin feature/your-feature`
5. **Open a pull request** describing the change and how it was tested.

Please ensure existing functionality is covered before submitting.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE`

---

Made with ☕ and a fleet of AI agents. Star the repo if TripMate AI saved you an hour of trip planning!

# ✈️ TripMate AI — Multi-Agent Travel Planner with LangGraph

> **Plan complete trips using AI-powered multi-agent workflows.**
>
> TripMate AI transforms a natural language travel request into a complete travel plan by coordinating multiple AI agents for flight research, hotel discovery, and itinerary generation. Built with **LangGraph**, **LangChain**, **FastAPI**, **Groq LLMs**, and **PostgreSQL**.

---

## 🚀 Overview

Planning a trip often requires switching between multiple websites to compare flights, search for hotels, and organize an itinerary.

TripMate AI simplifies this process by using a **multi-agent architecture**, where each AI agent is responsible for a specific task. The agents collaborate through **LangGraph** to generate a structured and personalized travel plan from a single user request.

This project demonstrates how modern AI agents can work together to solve real-world planning problems in a modular and scalable way.

---

## ✨ Features

- ✈️ Flight research using AviationStack API
- 🏨 Hotel recommendations using Tavily Search
- 🗓️ AI-generated day-by-day travel itinerary
- 🤖 Multi-agent orchestration with LangGraph
- 💬 Natural language travel planning
- ⚡ Fast responses powered by Groq LLMs
- 💾 Persistent conversation history with PostgreSQL
- 🌐 FastAPI backend with REST API
- 🎨 Simple web interface using HTML, CSS, JavaScript, and Jinja2
- 📦 Modular architecture for easy extension

---

## 🧠 Multi-Agent Architecture

```text
                    User Request
                          │
                          ▼
                 LangGraph Supervisor
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  Flight Agent      Hotel Agent     Itinerary Agent
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                  Response Agent
                          │
                          ▼
                 Structured Travel Plan
```

---

## ⚙️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| Backend | FastAPI |
| AI Framework | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| Database | PostgreSQL |
| Flight API | AviationStack |
| Search API | Tavily |
| Frontend | HTML, CSS, JavaScript, Jinja2 |

---

## 📁 Project Structure

```text
TripMate-AI/
│
├── app.py                  # FastAPI application
├── backend.py              # LangGraph workflow
├── requirements.txt
├── .env
│
├── tools/
│   ├── aviation.py
│   ├── tavily.py
│   └── utils.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

---

## 🔄 Workflow

```text
User Request
      │
      ▼
FastAPI API
      │
      ▼
LangGraph Supervisor
      │
      ├────────► Flight Agent
      │
      ├────────► Hotel Agent
      │
      ├────────► Itinerary Agent
      │
      ▼
Response Agent
      │
      ▼
Final Travel Plan
```

---

## 📸 Demo

> Add screenshots or GIFs of your application here.

```markdown
![Home Page](docs/home.png)

![Workflow Demo](docs/demo.gif)
```

---

## 🔑 Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- PostgreSQL
- Groq API Key
- Tavily API Key
- AviationStack API Key

---

## 🌱 Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db

GROQ_API_KEY=your_groq_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

TAVILY_API_KEY=your_tavily_api_key

DEFAULT_ORIGIN_IATA=DAC
```

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/your-username/tripmate-ai.git

cd tripmate-ai
```

Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

### Health Check

```http
GET /health
```

---

### Generate Travel Plan

```http
POST /api/travel
```

Example Request

```json
{
    "message": "Plan a 5-day trip to Switzerland with a budget of $2500."
}
```

---

## 📝 Example Output

```text
Destination: Switzerland
Duration: 5 Days
Budget: $2500

✈ Flights
Delhi → Zurich

🏨 Hotel
Hotel Alexander Zurich

📅 Day 1
• Explore Zurich Old Town
• Visit Bahnhofstrasse

📅 Day 2
• Rhine Falls
• Boat Cruise

📅 Day 3
• Lucerne
• Chapel Bridge

📅 Day 4
• Mount Titlis

📅 Day 5
• Local Shopping
• Return Flight
```

---

## 💡 Why Multi-Agent Architecture?

Instead of relying on a single LLM prompt, TripMate AI divides the planning process into specialized AI agents.

- **Flight Agent** → Finds flight information
- **Hotel Agent** → Searches accommodation options
- **Itinerary Agent** → Creates a day-by-day schedule
- **Response Agent** → Combines everything into a structured travel plan

This modular design makes the system easier to maintain, extend, and improve.

---

## 🚀 Future Improvements

- [ ] Google Maps integration
- [ ] Weather forecasting
- [ ] Budget optimization
- [ ] Restaurant recommendation agent
- [ ] Visa information agent
- [ ] PDF itinerary export
- [ ] Calendar integration
- [ ] Email itinerary
- [ ] Voice assistant
- [ ] Multi-city trip planning

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## ⭐ Support

If you found this project helpful, please consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future development.

---

## 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and contribute

thank you!!
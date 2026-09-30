# LinkedIn Post Options

---

## 🔥 Option 1 — Story-driven (best for engagement)

---

🏥 **I built an AI system that monitors hospital patients in real-time and consults with nurses using a local LLM.**

Here's what Sentinel Health Agent does — end to end:

**The problem it solves:**
Nurses drown in alerts. Not every high heart rate needs the same response — it depends on the patient's allergies, medications, and history. Generic alarms don't know that. Mine does.

**How it works:**
1. A Kafka stream delivers live patient vitals every 2 seconds
2. A background consumer picks up CRITICAL / WARNING readings
3. It fetches that patient's full medical history from PostgreSQL
4. It runs a RAG search over clinical guidelines (PDFs embedded into pgvector)
5. An Ollama LLM generates a personalised 1–2 sentence clinical recommendation
6. A nurse can then open the chatbot and ask follow-up questions — the LangGraph agent autonomously decides which tools to call (patient profile, history, recent alerts, knowledge base)

**The tech stack:**
→ FastAPI + async SQLAlchemy 2.x (production-grade, fully async)
→ Apache Kafka (KRaft, no Zookeeper) for real-time vitals streaming
→ LangGraph StateGraph with MemorySaver — persistent multi-turn conversation per session
→ MCP-style tools via LangChain StructuredTool — the LLM decides what to call
→ RAG pipeline: nomic-embed-text embeddings → pgvector similarity search → llama3.2
→ Streamlit multi-page dashboard (Live Alerts, Patient Onboarding, Alert History, Nurse Chatbot)
→ Docker Compose — PostgreSQL with pgvector, Kafka, Kafka UI

**What I'm proud of:**
- `main.py` is ~90 lines. All it does is wire services together.
- The Kafka consumer, RAG service, alert processor, and chatbot agent are all independent, testable classes
- The LangGraph agent uses class-based graph building — `ChatbotGraphBuilder(tools).build()` — no nested functions
- MCP tools use `StructuredTool.from_function` with Pydantic schemas so the LLM gets precise JSON schemas for every tool

This is the kind of system I want to keep building — production GenAI engineering at the intersection of real-time data and clinical decision support.

**GitHub:** [link]

Open to **GenAI / Backend / ML Engineering** roles. If your team is building something like this, let's talk. 👇

#GenAI #LangGraph #RAG #FastAPI #Kafka #Python #AIEngineering #LLM #OpenToWork

---

## ⚡ Option 2 — Short & punchy (better for reach)

---

🏥 Just shipped **Sentinel Health Agent** — an AI clinical alert system I built from scratch.

**What it does:**
- Streams patient vitals through Kafka in real time
- Enriches every CRITICAL alert with RAG-retrieved clinical guidelines + the patient's allergy/medication history
- Lets nurses consult a LangGraph chatbot that autonomously calls patient data tools (MCP pattern)
- All running on a local Ollama LLM — no OpenAI dependency

**Stack:** FastAPI · LangGraph · LangChain · Kafka · pgvector · PostgreSQL · Streamlit · Docker

This was a deep dive into production GenAI architecture — async SQLAlchemy 2.x, LangGraph StateGraph with persistent memory, class-based MCP tools with Pydantic schemas, and a RAG pipeline backed by pgvector.

GitHub: [link]

Actively looking for **GenAI / Backend Engineering** roles. DMs open 🚀

#Python #GenAI #RAG #LangGraph #Kafka #FastAPI #OpenToWork

---

## 💼 Option 3 — "What I learned" angle (great for technical recruiters)

---

🧠 **6 things I learned building a production GenAI system this week:**

**1. LangGraph is not just a chatbot framework.**
It's a proper state machine. Once you model your agent as a graph — START → llm_node → tool_executor → llm_node → END — reasoning loops become predictable and debuggable.

**2. MCP tools on class methods need StructuredTool, not @tool.**
`@tool` leaks `self` into the JSON schema the LLM sees. Use `StructuredTool.from_function(coroutine=self._method, args_schema=PydanticModel)` instead.

**3. `main.py` should be boring.**
Mine is ~90 lines. It starts services, exposes them on `app.state`, and registers routers. That's it. Every bug I found was in a file main.py didn't know about.

**4. Kafka message keys matter for ordering.**
Using `patient_id` as the Kafka key guarantees all readings for the same patient land on the same partition — critical if you're building per-patient alert logic.

**5. `async_sessionmaker` replaces `sessionmaker` for async SQLAlchemy 2.x.**
The old pattern causes type warnings and is officially deprecated. Small change, correct code.

**6. RAG without patient context is half the answer.**
The same 120 BPM reading means something completely different for a 25-year-old athlete vs. a 70-year-old on beta-blockers. Enriching the LLM prompt with medical history before the RAG call is what makes the advice actually useful.

Project: **Sentinel Health Agent** — real-time clinical alert monitoring with RAG + LangGraph nurse chatbot.

Stack: FastAPI · LangGraph · LangChain · Kafka · pgvector · Ollama · Streamlit

GitHub: [link] · Open to GenAI / Backend Engineering roles 👇

#GenAI #LangGraph #RAG #Python #FastAPI #Kafka #MLEngineering #OpenToWork

---

## 📌 Tips for maximum LinkedIn reach

| Do | Don't |
|----|-------|
| Post Tuesday–Thursday, 8–10am | Post on weekends |
| Add a screenshot of the dashboard | Leave it text-only |
| Reply to every comment in the first hour | Post and disappear |
| Tag 2–3 relevant people (LangChain team, etc.) | Tag 10+ random people |
| Pin it to your profile | Let it get buried |
| Add a Loom walkthrough video in the comments | Just link GitHub |

---

## 🏷️ Best hashtags for this project

`#GenAI` `#LangGraph` `#RAG` `#LLM` `#FastAPI` `#Kafka` `#Python` `#AIEngineering`
`#MachineLearning` `#BackendEngineering` `#OpenToWork` `#LangChain` `#PostgreSQL`

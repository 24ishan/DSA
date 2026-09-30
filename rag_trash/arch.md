# 🏗️ SYSTEM ARCHITECTURE & QUICK REFERENCE

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SENTINEL HEALTH AGENT                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐                                                      │
│  │  Simulator   │────┐                                                 │
│  │ (simulator.py)    │                                                 │
│  └──────────────┘    │ Vitals Data                                     │
│                      │ (HR, SpO2)                                      │
│                      ├────────────────────────────────────────┐        │
│                      │                                        │        │
│                      ▼                                        ▼        │
│           ┌────────────────────┐              ┌─────────────────┐    │
│           │   Kafka Broker     │──────────────│  Kafka UI       │    │
│           │ (vitals_stream)    │              │ (Port 8080)     │    │
│           └────────────────────┘              └─────────────────┘    │
│                      │                                                 │
│                      │ Message Stream                                  │
│                      ▼                                                 │
│           ┌────────────────────────────────────────────┐             │
│           │     FastAPI Backend                         │             │
│           │     (app/backend/main.py)                   │             │
│           │                                            │             │
│           │  ┌────────────────────────────────────┐   │             │
│           │  │  Kafka Consumer Loop                │   │             │
│           │  │  blocking_kafka_loop()             │   │             │
│           │  │  - Poll messages                   │   │             │
│           │  │  - Filter CRITICAL status          │   │             │
│           │  │  - Call ProcessAlerts              │   │             │
│           │  └────────────────────────────────────┘   │             │
│           │                  │                        │             │
│           │                  ▼                        │             │
│           │  ┌────────────────────────────────────┐   │             │
│           │  │  ProcessAlerts                      │   │             │
│           │  │  - Validate inputs                 │   │             │
│           │  │  - Get RAG advice                  │   │             │
│           │  │  - Save to database                │   │             │
│           │  └────────────────────────────────────┘   │             │
│           │                  │                        │             │
│           │                  ▼                        │             │
│           │  ┌────────────────────────────────────┐   │             │
│           │  │  MedicalRAG                        │   │             │
│           │  │  - Query vector store              │   │             │
│           │  │  - Get context                     │   │             │
│           │  │  - Call Ollama LLM                 │   │             │
│           │  │  - Generate advice                 │   │             │
│           │  └────────────────────────────────────┘   │             │
│           │                  │                        │             │
│           │                  ├─────────────────────┐  │             │
│           │                  ▼                    ▼  │             │
│           │  ┌────────────┐          ┌────────────────────┐        │
│           │  │ PostgreSQL │◄────────►│ Ollama LLM         │        │
│           │  │ + pgvector │          │ (llama2)           │        │
│           │  │            │          │ + Embeddings       │        │
│           │  └────────────┘          │ (mxbai-embed-large)│        │
│           │  - clinical_alerts       └────────────────────┘        │
│           │  - medical_vectors                                      │
│           │                                                        │
│           └────────────────────────────────────────────┘            │
│                                                                    │
│           ┌──────────────────────┐   ┌──────────────────────┐     │
│           │  API Endpoints       │   │  Health Endpoints    │     │
│           │  - POST /upload      │   │  - GET /health       │     │
│           │  - GET /history      │   │  - GET /health/rag   │     │
│           │  - GET /             │   │                      │     │
│           └──────────────────────┘   └──────────────────────┘     │
│                      │                                             │
│                      │ JSON Responses                              │
│                      ▼                                             │
│           ┌────────────────────────┐                              │
│           │ Streamlit Dashboard    │                              │
│           │ (app/dashboard/home.py)│                              │
│           │ - Real-time alerts     │                              │
│           │ - Alert history        │                              │
│           │ - AI advice display    │                              │
│           └────────────────────────┘                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Interaction Matrix

| Component | Interacts With | Type | Purpose |
|-----------|----------------|------|---------|
| Simulator | Kafka | Produces | Sends vital signs |
| Kafka | Backend | Queues | Message broker |
| Backend Main | Kafka | Consumes | Polls critical alerts |
| Backend Main | ProcessAlerts | Calls | Processes alerts |
| ProcessAlerts | MedicalRAG | Calls | Gets clinical advice |
| ProcessAlerts | PostgreSQL | Writes | Saves alerts |
| MedicalRAG | PostgreSQL | Reads | Vector search |
| MedicalRAG | Ollama | Calls | LLM + Embeddings |
| Dashboard | Backend | HTTP GET | Fetches history |
| PDF Upload | PostgresRAGManager | Calls | Indexes documents |
| PostgresRAGManager | PostgreSQL | Reads/Writes | Vector store |
| PostgresRAGManager | Ollama | Calls | Embeddings |

---

## File Dependencies Graph

```
simulator.py
  ├─ kafka
  └─ .env

app/backend/main.py
  ├─ fastapi
  ├─ sqlalchemy
  ├─ app/__init__.py (setup_logging)
  ├─ app/utils/config.py
  ├─ app/backend/models.py
  ├─ app/backend/schemas.py
  ├─ app/backend/services/process_alerts.py
  ├─ app/backend/services/rag_service.py
  ├─ app/backend/services/history.py
  ├─ app/vector_db/ingest_pdf.py
  └─ kafka

app/backend/services/process_alerts.py
  ├─ app/backend/models.py
  ├─ app/backend/services/rag_service.py
  └─ app/__init__.py

app/backend/services/rag_service.py
  ├─ app/utils/config.py
  ├─ app/utils/retry.py
  ├─ app/backend/services/prompts.py
  ├─ langchain_ollama
  ├─ langchain_postgres
  └─ app/__init__.py

app/vector_db/ingest_pdf.py
  ├─ app/utils/config.py
  ├─ langchain_postgres
  ├─ langchain_ollama
  ├─ pypdf
  └─ app/__init__.py

app/dashboard/home.py
  ├─ streamlit
  ├─ pandas
  └─ requests

app/backend/services/history.py
  ├─ app/backend/models.py
  └─ sqlalchemy

app/backend/store/*
  └─ (Currently empty, ready for implementation)
```

---

## Configuration Flow

```
.env file (local)
  ├─→ POSTGRES_* → DATABASE_URL
  ├─→ KAFKA_*
  ├─→ OLLAMA_*
  ├─→ LOG_LEVEL
  └─→ TABLE NAMES

app/utils/config.py
  ├─→ All modules import config
  └─→ Single source of truth

Environment Validation (main.py:validate_env_vars)
  ├─→ Runs on app startup
  └─→ Fails fast if missing
```

---

## Data Models Relationships

```
                   ┌─────────────────────┐
                   │  ClinicalAlert      │
                   │  (SQLAlchemy Model) │
                   │                     │
                   │  - id (PK)          │
                   │  - patient_id (FK)  │
                   │  - heart_rate       │
                   │  - status           │
                   │  - ai_advice        │
                   │  - timestamp        │
                   └─────────────────────┘
                          ▲
                          │ Serialized by
                          │
                   ┌─────────────────────┐
                   │ClinicalAlertResponse│
                   │  (Pydantic Schema)  │
                   │                     │
                   │ Used in /history API│
                   └─────────────────────┘

                   ┌──────────────────────┐
                   │  Vector Documents    │
                   │  (pgvector table)    │
                   │                      │
                   │  - langchain_id (PK) │
                   │  - content           │
                   │  - embedding(768)    │
                   │  - metadata.json     │
                   └──────────────────────┘
                          ▲
                   Used by MedicalRAG
                   for semantic search
```

---

## State Management & Lifecycle

### Application Startup Sequence
```
1. Validate environment variables
2. Create async engine (SQLAlchemy)
3. Create session factory
4. Create FastAPI app with lifespan
5. [Lifespan → STARTUP]
   └─ Initialize RAG service
      ├─ Create embeddings model
      ├─ Create LLM model
      ├─ Create PGEngine
      └─ Initialize vector store
   └─ Initialize ProcessAlerts
   └─ Start Kafka consumer task
6. Server ready to accept requests
```

### Request Processing for Critical Alert
```
1. Kafka message arrives (vitals_stream)
2. blocking_kafka_loop() polls it
3. Filter: status == "CRITICAL"
4. ProcessAlerts.process_critical_alert()
   └─ Get RAG agent (lazy init)
   └─ Validate inputs
   └─ Call MedicalRAG.get_clinical_advice()
      ├─ Validate heart rate (30-200)
      ├─ Query vector store
      ├─ Get relevant documents
      ├─ Format prompt
      ├─ Call Ollama LLM (with retries)
      └─ Return advice
   └─ Save ClinicalAlert to DB
   └─ Return status
5. Continue polling
```

### Application Shutdown Sequence
```
1. Lifespan → SHUTDOWN
2. Cancel Kafka consumer task
3. Wait up to 10 seconds
4. Close Kafka consumer
5. Close RAG service
6. Dispose database engine
7. Exit
```

---

## Error Handling Strategy

```
Input Validation Errors
  └─ ValueError → Logged + returned as error response

Database Errors
  └─ SQLAlchemy exceptions → Caught + logged with traceback

Network/Connection Errors
  └─ ConnectionError → Retry with exponential backoff

Timeout Errors
  └─ TimeoutError → Retry with exponential backoff

Unknown Errors
  └─ Exception → Logged with full traceback + re-raised
```

---

## Performance Characteristics

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| Embeddings Generation | 100-500ms | Depends on Ollama |
| Vector Search (k=2) | 50-200ms | Index on langchain_id |
| LLM Inference | 1-3 seconds | WiFi dependent |
| DB Roundtrip | 10-50ms | Connection pooled |
| Alert Processing | 2-4s | Total end-to-end |

---

## Testing Considerations for Future Development

### Unit Tests Needed:
- `test_rag_service.py` - MedicalRAG methods
- `test_process_alerts.py` - Alert processing logic
- `test_prompts.py` - Prompt formatting
- `test_retry.py` - Retry decorator

### Integration Tests Needed:
- Test Kafka → Backend → DB flow
- Test PDF upload → indexing → search
- Test health checks

### Load Tests Needed:
- Kafka message throughput
- Concurrent alert processing
- Vector store search performance

---

## Common Development Tasks

### Add a New Alert Type
1. Update `simulator.py` to generate it
2. Update `ProcessAlerts` to handle it
3. Add to `ClinicalAlert` model if different fields
4. Update dashboard if needed

### Add a New LLM Model
1. Update `.env` with new model name
2. Download model: `ollama pull model_name`
3. MedicalRAG will use it automatically

### Add a New Embedding Model
1. Update `.env` with new embedding model
2. Update `CONTEXT_MAX_LENGTH` if embedding dimensions change
3. MedicalRAG will use it automatically

### Add Authentication
1. Implement OAuth 2.0 in `main.py`
2. Add auth middleware
3. Protect endpoints with `Depends(get_current_user)`

### Scale Horizontally
1. Use multiple FastAPI instances
2. Load balance with nginx/haproxy
3. Kafka handles multiple consumers automatically
4. PostgreSQL connection pooling scales well

---

## Debugging Quick Tips

### Check Logs
```bash
# Watch backend logs
docker logs -f [backend_container]

# Check log level
echo $LOG_LEVEL
```

### Monitor Kafka
```bash
# Visit Kafka UI
http://localhost:8080

# Check topic
kafka-console-consumer --bootstrap-servers localhost:9092 --topic vitals_stream --from-beginning
```

### Test Database
```bash
# Connect to PostgreSQL
psql postgresql://user:pass@localhost:5432/health_agent

# Check tables
\dt

# Query alerts
SELECT * FROM clinical_alerts ORDER BY timestamp DESC LIMIT 5;
```

### Test Ollama
```bash
# Check running models
curl http://localhost:11434/api/tags

# Test embeddings
curl -X POST http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Hello world"
}'
```

### Test Backend Health
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/rag
```

---

This reference covers the complete system architecture and is ready for your future development!


# Monitoring Flow & Data Contract

```mermaid
flowchart TD
    A[Chatbot App] -->|JSONL logs| B[Monitoring Script]
    B --> C{Detectors}
    C --> C1[PII Regex]
    C --> C2[Latency Threshold]
    C --> C3[Error Classifier]
    C1 --> D[Flags JSONL]
    C2 --> D
    C3 --> D
    B --> E[Metrics CSV]
    B --> F[Operator Log (.log)]
    D --> G[Alerting Hook (future)]
```

## Data Contract (per log record)
```json
{
  "timestamp": "2025-08-22T12:34:56Z",
  "request_id": "uuid-...",
  "user_id": "u123",
  "prompt": "How do I reset my password?",
  "response": "Click…",
  "latency_ms": 842,
  "error_type": null,
  "model_version": "chatbot-1.1.0"
}
```

- **PII Regex**: emails and phone numbers (US-style + basic international pattern) for demo purposes.
- **Latency**: default alert threshold `>= 1500 ms` (configurable).
- **Errors**: any non-null `error_type` or `error`==true is counted.
# Project: LLMOps Foundations

This repository contains the foundational LLMOps framework for a customer-facing chatbot. It provides the essential tools and workflows for monitoring, versioning, and improving our AI application, moving it from a prototype to a robust, safe, and scalable product.

## 🎯 Objective

To implement core LLMOps concepts including deployment, monitoring, evaluation, versioning, and feedback loops to ensure the reliability and continuous improvement of our chatbot.

---

## 🏛️ System Architecture & Lifecycle

Our LLMOps lifecycle is designed to be a continuous loop, ensuring that insights from production actively inform development.

![LLMOps Lifecycle Diagram](docs/lifecycle_map.md)

*For a detailed explanation of each phase, please see the [Lifecycle Map Document](./docs/lifecycle_map.md).*

---

## 📂 Folder Structure

```
/
├── docs/
│   └── lifecycle_map.md      # Mermaid diagram and explanation of the LLMOps cycle.
├── src/
│   ├── monitoring.py         # Python script for real-time monitoring of chatbot responses.
│   └── feedback_collector.py # CLI tool for collecting stakeholder feedback.
├── .gitignore                # Standard Python .gitignore.
├── README.md                 # This file.
└── requirements.txt          # (Currently empty as only standard libraries are used).
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git

### Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/llmops-foundations-bootcamp.git
    cd llmops-foundations-bootcamp
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies (if any):**
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Code Usage

### 1. Monitoring Chatbot Interactions

The `monitoring.py` script simulates chatbot activity and checks each response for high latency, errors, and PII leaks.

**To run the simulation:**
```bash
python src/monitoring.py
```
- **Output:** Logs will be printed to the console and saved to `chatbot_monitoring.log`.
- **What it does:**
    - **Latency:** Flags responses that take longer than 5 seconds.
    - **PII:** Uses regex to detect emails and phone numbers in bot responses.
    - **Errors:** Identifies and logs explicit error messages from the bot.
    - **Structured Logging:** All interactions are logged as JSON for easy parsing by downstream systems.

### 2. Collecting Feedback

The `feedback_collector.py` script provides a simple CLI to gather and store structured feedback from users or internal teams (like Product Managers).

**To submit feedback:**
```bash
python src/feedback_collector.py
```
- The script will prompt you for a User ID, feedback type, and a description.
- Feedback is stored in `feedback.jsonl`, a JSON Lines file where each line is a valid JSON object.

---

## 🔄 Versioning and Rollback Strategy

We use a Git-based branching model to manage our releases and enable rapid rollbacks.

- **`main` branch:** This is the primary development branch. All new features and improvements are merged here. It is expected to be potentially unstable.
- **`stable` branch:** This branch represents the last known-good version of the application that is safe for production deployment.

### Disaster Recovery: Rollback Scenario

**Scenario:** A new deployment from `main` introduces a critical bug (e.g., the chatbot frequently crashes or leaks sensitive data).

**Rollback Steps:**

1.  **Halt Deployments:** The on-call engineer immediately pauses any further deployments from the `main` branch.
2.  **Identify Last Good Version:** The `stable` branch points to the last validated commit.
3.  **Execute Rollback:** The `stable` branch is merged back into `main` and deployed, effectively overwriting the faulty changes.
    ```bash
    # Get on the main branch
    git checkout main

    # Merge the 'stable' version back into 'main'
    git merge stable

    # Push the reverted code to trigger a new deployment
    git push origin main
    ```
4.  **Post-Mortem:** The team conducts a post-mortem to understand the root cause and improve testing and validation processes.

---

## 📝 Design Decisions & Rationale

- **PII Detection with Regex:** We use regular expressions for PII detection as a simple, fast, and dependency-free first line of defense. It's not foolproof but catches the most common formats effectively. In a more mature system, this would be augmented with a more sophisticated NER (Named Entity Recognition) model.
- **JSON Lines for Logs/Feedback (`.jsonl`):** We chose the JSON Lines format because it's easy to append to. Unlike a single large JSON array, you can add new records to the file without parsing the entire content, which is ideal for logging and streaming data.
- **Standard Libraries Only:** The core scripts use only Python's standard libraries (`re`, `logging`, `time`, `json`). This makes the tools highly portable and removes dependency management overhead for these foundational tasks.

## 🔒 Privacy & Compliance Notes

- **PII Monitoring is Critical:** The `monitoring.py` script's primary security function is to act as a safety net, detecting and alerting on accidental PII exposure by the LLM.
- **Data Minimization:** All collected feedback and logs should be subject to data retention policies. The `user_id` should be a non-identifiable internal ID, not a real user name or email.
- **Next Steps:** For compliance with regulations like GDPR, we would need to add mechanisms for data access, rectification, and erasure, as well as more robust anonymization of logs.
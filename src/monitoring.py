import re
import time
import logging
import json
import random
from datetime import datetime

# --- Configuration ---
LOG_FILE = "chatbot_monitoring.log"
PII_PATTERNS = {
    "EMAIL": r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    "PHONE": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
}

# --- Logging Setup ---
# Configure logger to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def detect_pii(text):
    """
    Detects Personal Identifiable Information (PII) in a given text.
    Returns a dictionary with found PII types and their matches.
    """
    found_pii = {}
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            found_pii[pii_type] = matches
    return found_pii

def monitor_conversation(user_id, request, response, latency):
    """
    Monitors a single chatbot conversation for performance, errors, and PII.
    """
    # 1. Latency Check
    if latency > 5.0:
        logging.warning(f"HighLatency: Response time was {latency:.2f}s for user {user_id}")

    # 2. Error Detection (based on response content)
    if response.get("status") == "error":
        logging.error(f"ChatbotError: User {user_id} encountered an error: {response.get('content')}")
        return

    response_text = response.get("content", "")

    # 3. PII Detection
    pii_found = detect_pii(response_text)
    if pii_found:
        logging.warning(f"PIIDetection: PII detected for user {user_id}. Details: {pii_found}")

    # 4. Standard Logging
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "request": request,
        "response": response_text,
        "latency_seconds": latency,
        "pii_detected": bool(pii_found),
        "status": response.get("status")
    }
    logging.info(f"InteractionLog: {json.dumps(log_entry)}")

def simulate_chatbot_response(query):
    """
    A mock function to simulate getting a response from the LLM-powered chatbot.
    """
    start_time = time.time()
    
    # Simulate different scenarios
    rand_val = random.random()
    if rand_val < 0.7: # Happy path
        response = {
            "status": "success",
            "content": "Thank you for your query about your order. It is scheduled to arrive tomorrow."
        }
        time.sleep(random.uniform(0.5, 2.0))
    elif rand_val < 0.85: # PII leak scenario
        response = {
            "status": "success",
            "content": "Your account details are tied to user@example.com. For help, call 555-123-4567."
        }
        time.sleep(random.uniform(1.0, 3.0))
    elif rand_val < 0.95: # High latency scenario
        response = {
            "status": "success",
            "content": "Searching through our extensive knowledge base for your complex query..."
        }
        time.sleep(random.uniform(5.5, 7.0))
    else: # Error scenario
        response = {
            "status": "error",
            "content": "I am sorry, but I encountered an internal error. Please try again later."
        }
        time.sleep(random.uniform(0.5, 1.0))

    end_time = time.time()
    latency = end_time - start_time
    return response, latency

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting chatbot monitoring simulation...")
    
    sample_queries = [
        "What's the status of my order?",
        "How do I reset my password?",
        "Can you find my account details?",
        "Tell me about your refund policy.",
        "Why is my bill so high?"
    ]

    for i in range(10):
        user_id = f"user_{random.randint(100, 999)}"
        query = random.choice(sample_queries)
        print(f"\n--- Simulating interaction for {user_id} ---")
        response, latency = simulate_chatbot_response(query)
        monitor_conversation(user_id, query, response, latency)
        time.sleep(1)

    print("\nSimulation finished. Check 'chatbot_monitoring.log' for detailed logs.")
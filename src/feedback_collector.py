import json
from datetime import datetime

FEEDBACK_FILE = "feedback.jsonl"

def collect_feedback():
    """
    Collects structured feedback from a user via the command line
    and saves it to a JSON Lines file.
    """
    print("--- Chatbot Feedback Collector ---")
    
    # 1. Get User Input
    user_id = input("Enter your User ID (e.g., 12345): ").strip()
    
    print("Select Feedback Type:")
    print("  1: Bug Report")
    print("  2: Suggestion")
    print("  3: Incorrect Answer")
    print("  4: Other")
    
    feedback_type_map = {
        "1": "bug_report",
        "2": "suggestion",
        "3": "incorrect_answer",
        "4": "other"
    }
    type_choice = input("Enter the number for the feedback type: ").strip()
    feedback_type = feedback_type_map.get(type_choice, "other")
    
    description = input("Please provide a detailed description of your feedback:\n").strip()

    # Basic validation
    if not user_id or not description:
        print("\nError: User ID and description cannot be empty. Aborting.")
        return

    # 2. Structure the Feedback Record
    feedback_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "feedback_type": feedback_type,
        "description": description
    }
    
    # 3. Save the Record
    try:
        with open(FEEDBACK_FILE, 'a') as f:
            f.write(json.dumps(feedback_record) + '\n')
        print("\nThank you! Your feedback has been successfully recorded.")
        print("Record saved:", json.dumps(feedback_record, indent=2))
    except IOError as e:
        print(f"\nError: Could not write to feedback file '{FEEDBACK_FILE}'. {e}")

if __name__ == "__main__":
    collect_feedback()
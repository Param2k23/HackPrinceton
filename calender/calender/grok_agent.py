import os
import json
import requests
from xai_sdk import Client
from xai_sdk.chat import user, system
from datetime import datetime, timedelta

# ---- CONFIG ----
GROK_API_KEY = "xai-my_api_key"
CAL_API_URL = "http://localhost:8000"

# List ALL calendars to check (shared calendar + personal calendars)
CALENDARS_TO_CHECK = [
    "247dea3b49ee02b600bb816406bf949dd6a5cd8e4ed0bfc4d3b3599f2fca5359@group.calendar.google.com",
    "neel.modi4@gmail.com",
]

# Default calendar for adding events
DEFAULT_CALENDAR = "247dea3b49ee02b600bb816406bf949dd6a5cd8e4ed0bfc4d3b3599f2fca5359@group.calendar.google.com"

# ---- Initialize Grok Client ----
client = Client(
    api_key=GROK_API_KEY,
    timeout=180,
)

# ---- Helper Functions ----
def extract_text(response):
    """Extract text from Grok response"""
    if not response:
        return ""
    content = response.content
    if isinstance(content, str):
        return content
    elif isinstance(content, list) and len(content) > 0:
        first = content[0]
        if isinstance(first, dict) and "text" in first:
            return first["text"]
        elif isinstance(first, str):
            return first
    return ""


def get_current_datetime():
    """Get current datetime in ISO format"""
    return datetime.now().isoformat()


def ask_grok_to_parse_intent(query: str) -> str:
    """Ask Grok to understand the user's intent and return structured JSON"""
    
    current_time = get_current_datetime()
    
    prompt = f"""Current date and time: {current_time}

User query: "{query}"

Analyze this query and return ONLY a JSON object (no other text) with one of these formats:

For finding free time slots:
{{
  "action": "find_free_slots",
  "calendars": {json.dumps(CALENDARS_TO_CHECK)},
  "start": "2025-11-10T00:00:00",
  "end": "2025-11-17T00:00:00",
  "duration_minutes": 60
}}

For adding an event:
{{
  "action": "add_event",
  "calendar_id": "{DEFAULT_CALENDAR}",
  "title": "Meeting Title",
  "start": "2025-11-12T14:00:00",
  "end": "2025-11-12T15:00:00",
  "description": "Optional description",
  "attendees": ["email1@example.com", "email2@example.com"]
}}

Guidelines:
- Parse relative dates like "next week", "tomorrow", "next Monday" into specific ISO datetime strings
- For "find time" queries, infer reasonable time ranges (e.g., "next week" = next 7 days from now)
- For duration, infer from context (e.g., "2-hour slot" = 120 minutes, "quick meeting" = 30 minutes)
- For events, extract title, start time, end time from the query
- If no duration specified for events, default to 60 minutes
- Use 24-hour format for times
- Include all emails from {json.dumps(CALENDARS_TO_CHECK)} as attendees for events
- Return ONLY the JSON, nothing else"""
    
    print("⏳ Asking Grok to parse intent... (this may take 30-90 seconds)")
    chat = client.chat.create(model="grok-4")
    chat.append(user(prompt))

    try:
        response = chat.sample()
        print("✅ Got response from Grok")
        return extract_text(response)
    except Exception as e:
        print(f"⚠️ Grok timed out or failed: {e}")
        return None


def call_find_free_slots(args: dict):
    """Call the find_free_slots API endpoint"""
    print(f"📅 Querying calendar for free slots...")
    r = requests.post(f"{CAL_API_URL}/find_free_slots", json=args)
    r.raise_for_status()
    return r.json()


def call_add_event(args: dict):
    """Call the add_event API endpoint"""
    print(f"📝 Adding event to calendar...")
    r = requests.post(f"{CAL_API_URL}/add_event", json=args)
    r.raise_for_status()
    return r.json()


def generate_response(query: str, action: str, result: dict):
    """Ask Grok to generate a natural language response"""
    
    if action == "find_free_slots":
        suggestions = result.get("suggestions", [])
        
        if not suggestions:
            context = "No free slots found in the specified time range."
        else:
            context = f"Found {len(suggestions)} free time slot(s):\n{json.dumps(suggestions, indent=2)}"
        
        response_prompt = f"""User asked: "{query}"

Result: {context}

Write a friendly, professional 2-3 sentence response summarizing when they're free. Format times in a readable way (e.g., "Monday, Nov 11 at 2:00 PM")."""
    
    else:  # add_event
        event_id = result.get("eventId", "")
        event_link = result.get("htmlLink", "")
        
        response_prompt = f"""User asked: "{query}"

The event was successfully added to the calendar.
Event ID: {event_id}
Link: {event_link}

Write a friendly 1-2 sentence confirmation message."""
    
    print("⏳ Generating response... (this may take 30-60 seconds)")
    chat = client.chat.create(model="grok-4")
    chat.append(user(response_prompt))
    
    try:
        response = chat.sample()
        print("✅ Got response from Grok")
        return extract_text(response)
    except Exception as e:
        print(f"⚠️ Grok timed out for response: {e}")
        if action == "find_free_slots":
            return f"Found {len(result.get('suggestions', []))} free time slot(s)."
        else:
            return "Event added successfully!"


def clean_json_response(text: str) -> str:
    """Clean up JSON response by removing markdown code blocks"""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line (```)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)
    return cleaned.strip()


# ---- MAIN ----

def process_query(user_query: str):
    """
    Process a user query and execute the appropriate action.
    Returns a dictionary with structured results instead of printing to console.
    """
    result_data = {
        "user_query": user_query,
        "parsed_intent": None,
        "api_result": None,
        "response": None,
        "error": None
    }

    try:
        # Step 1: Ask Grok to parse the intent
        llm_output = ask_grok_to_parse_intent(user_query)
        if not llm_output:
            result_data["error"] = "No response from Grok"
            return result_data

        result_data["parsed_intent_raw"] = llm_output

        # Step 2: Parse JSON response
        cleaned_output = clean_json_response(llm_output)
        try:
            parsed = json.loads(cleaned_output)
            result_data["parsed_intent"] = parsed

            action = parsed.get("action")
            if action == "find_free_slots":
                # Step 3a: Find free slots
                api_args = {
                    "calendars": parsed["calendars"],
                    "start": parsed["start"],
                    "end": parsed["end"],
                    "duration_minutes": parsed["duration_minutes"]
                }
                api_result = call_find_free_slots(api_args)
                result_data["api_result"] = api_result

                # Step 4: Generate response
                response = generate_response(user_query, action, api_result)
                result_data["response"] = response

            elif action == "add_event":
                # Step 3b: Add event
                api_args = {
                    "calendar_id": parsed["calendar_id"],
                    "title": parsed["title"],
                    "start": parsed["start"],
                    "end": parsed["end"],
                    "description": parsed.get("description", ""),
                    "attendees": parsed.get("attendees", [])
                }
                api_result = call_add_event(api_args)
                result_data["api_result"] = api_result

                response = generate_response(user_query, action, api_result)
                result_data["response"] = response

            else:
                result_data["error"] = f"Unknown action: {action}"

        except json.JSONDecodeError as e:
            result_data["error"] = f"Grok did not return valid JSON: {e}"
            result_data["parsed_intent_raw"] = cleaned_output

    except KeyboardInterrupt:
        result_data["error"] = "Interrupted by user"
    except Exception as e:
        result_data["error"] = f"{type(e).__name__}: {e}"

    return result_data


if __name__ == "__main__":
    print("🚀 Starting Enhanced Grok Calendar Agent\n")
    print("=" * 60)
    
    # Example queries - uncomment to test different scenarios
    
    # Finding free time
    # process_query("Find a 2-hour slot next week when everyone is free")
    # process_query("When am I free tomorrow afternoon?")
    # process_query("Show me available times for a quick 30-minute meeting next Monday")
    
    # Adding events
    # process_query("Schedule a team meeting next Tuesday at 2 PM for 1 hour")
    # process_query("Add 'Project Review' to the calendar on Nov 15th from 3-4 PM")
    # process_query("Book a 2-hour workshop on Friday at 10 AM")
    
    # Interactive mode
    while True:
        print("\n" + "=" * 60)
        user_query = input("🧩 Enter your query (or 'quit' to exit): ").strip()
        
        if user_query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_query:
            continue
            
        process_query(user_query)
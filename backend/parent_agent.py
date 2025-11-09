import json
import os
from xai_sdk import Client
from xai_sdk.chat import system, user
from tools import tools
from prompts import CHILD_FACING_PROMPT, PARENT_CLASSIFIER_PROMPT
import google.generativeai as genai
from datetime import datetime
# --- This is our REAL LLM Call Function ---
DASHBOARD_FILE = "C:\\HackPrinceton\\utils\\parent.json"

def parent_llm_call(input):
    """
    Makes a real API call to the Groq cloud.
    """
    print(f"\n--- [Parent LLM Call START] ---")
    print(f"USER: {input[:150]}...") # Print first 150 chars
    
    try:
        client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600, # Override default timeout with longer timeout for reasoning models
        )
        
        chat = client.chat.create(
            model="grok-3-mini",
            reasoning_effort="high",
            messages=[system(CHILD_FACING_PROMPT)],
        )
        chat.append(user(input))
        response = chat.sample()
        print(f"--- [Parent LLM Call END] ---\n")
        print(response.content)
        return response.content
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        if "No API key provided" in str(e):
            return "Error: XAI_API_KEY environment variable not set."
        return "Error: An unexpected error occurred."

def get_parent_alert(input_text):
    """
    Makes a private LLM call to classify the child's input
    and generate a parent-facing alert if needed.
    """
    print(f"\n--- [Classifier LLM Call START] ---")
    
    try:
        # Get the API key from your environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
            
        # Configure the genai module with your API key
        genai.configure(api_key=api_key)
        
        # --- Now you can create a model ---
        # Create a model instance for your classifier
        client_gemini = genai.GenerativeModel('gemini-2.5-flash')
        
        print("Gemini client initialized successfully.")

    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        client_gemini = None
        if not client_gemini:
            print(f"Error: GENAI_API_KEY environment variable not set.")
        return {"severity": "normal"} # Fail safe

    # Format the prompt with the child's input
    prompt = PARENT_CLASSIFIER_PROMPT.format(child_input=input_text)
    
    try:
        response = client_gemini.generate_content(prompt)
        
        content = response.text
        print(f"--- [Classifier LLM Call END] ---")
        
        # --- Parse the JSON response ---
        return json.loads(content)
        
    except json.JSONDecodeError:
        print(f"Error: Classifier LLM did not return valid JSON. Response: {content}")
        return {"severity": "normal"} # Fail safe
    except Exception as e:
        print(f"Error: Classifier LLM call failed - {e}")
        return {"severity": "normal"} # Fail safe

def append_to_dashboard(alert_data):
    """Appends a JSON object as a new line to the dashboard file."""
    try:
        # Add a timestamp to the data
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **alert_data
        }
        with open(DASHBOARD_FILE, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
        print(f"[Dashboard] Logged alert: {log_entry['privacy_safe_message']}")
    except Exception as e:
        print(f"[Dashboard] Error: Failed to write to dashboard file - {e}")
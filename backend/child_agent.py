import json
import os
from xai_sdk import Client
from xai_sdk.chat import system, user
from tools import tools
from prompts import PARENT_FACING_PROMPT

# --- This is our REAL LLM Call Function ---

def child_llm_call(input):
    """
    Makes a real API call to the Groq cloud.
    """
    print(f"\n--- [LLM Call START] ---")
    print(f"USER: {input[:150]}...") # Print first 150 chars
    
    try:
        client = Client(
        api_key=os.getenv("XAI_API_KEY"),
        timeout=3600, # Override default timeout with longer timeout for reasoning models
        )
        
        chat = client.chat.create(
            model="grok-3-mini",
            reasoning_effort="high",
            messages=[system(PARENT_FACING_PROMPT)],
        )
        print(f"--- [LLM Call END] ---\n")
        print(chat)
        return chat
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        if "No API key provided" in str(e):
            return "Error: XAI_API_KEY environment variable not set."
        return "Error: An unexpected error occurred."
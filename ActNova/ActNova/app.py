from nova_act import NovaAct
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_with_nova_act(user_prompt, starting_page=None):
    """
    Use Nova Act to perform web searches and interactions
    """
    try:
        # Default to Google search if no starting page specified
        if not starting_page:
            starting_page = "https://www.google.com"
        
        print(f"\n🔍 Starting Nova Act on: {starting_page}")
        print(f"📝 Task: {user_prompt}")
        print("\n⏳ Processing... (this may take a moment)\n")
        
        # Convert user prompt into an action for Nova Act
        action_prompt = f"{user_prompt}. Extract and return only the most concise and precise information."
        
        # Initialize NovaAct with API key
        with NovaAct(
            starting_page=starting_page, 
            headless=True # Pass the API key explicitly
        ) as nova:
            result = nova.act(action_prompt)
        
        # Extract response from ActResult object
        response_text = None
        if hasattr(result, 'response') and result.response:
            response_text = result.response
        elif hasattr(result, 'parsed_response') and result.parsed_response:
            response_text = result.parsed_response
        else:
            # Fallback: try to get any text from the result
            response_text = str(result)
        
        print("=" * 80)
        print("✅ RESULTS:")
        print("=" * 80)
        if response_text and response_text != "None":
            print(response_text)
        else:
            print("⚠️  No response received. Raw result:")
            print(result)
        print("=" * 80)
        
        # Print metadata for debugging
        if hasattr(result, 'metadata'):
            print(f"\n📊 Metadata:")
            print(f"   Steps executed: {result.metadata.num_steps_executed}")
            print(f"   Duration: {result.metadata.end_time - result.metadata.start_time}")
        
        return response_text
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full error for debugging
        return None

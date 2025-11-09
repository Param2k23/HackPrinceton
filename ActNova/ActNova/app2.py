from nova_act import NovaAct
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_with_nova_act(user_prompt, starting_page="https://www.google.com"):
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

def main():
    # Get API key from environment variable or hardcode it temporarily
    api_key = os.environ.get('NOVA_ACT_API_KEY') or "8d1dbd68-2516-4ca9-8006-91a4a603baec"
    
    if not api_key:
        print("\n" + "=" * 80)
        print("❌ ERROR: NOVA_ACT_API_KEY not found!")
        print("=" * 80)
        print("\nPlease set your API key using one of these methods:")
        print("\n1. Environment variable:")
        print("   export NOVA_ACT_API_KEY='your_api_key_here'")
        print("\n2. Create a .env file with:")
        print("   NOVA_ACT_API_KEY=your_api_key_here")
        print("\n3. Get your API key from: https://nova.amazon.com/act")
        print("=" * 80 + "\n")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("🤖 Amazon Nova Act - Terminal Demo")
    print("=" * 80)
    print(f"🔑 Using API Key: {api_key[:8]}...{api_key[-4:]}")
    print("\nExamples of queries you can try:")
    print("  • Are there any basketball games coming up next weekend?")
    print("  • What are some playing arenas in Princeton?")
    print("  • Find upcoming concerts in New York")
    print("  • Search for the latest tech news")
    print("\nType 'quit' or 'exit' to stop\n")
    print("=" * 80)
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 Enter your query: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            # Skip empty inputs
            if not user_input:
                print("⚠️  Please enter a query")
                continue
            
            # Check if user wants to specify a starting page
            print("\n🌐 Starting page (press Enter for Google, or enter a URL): ", end='')
            starting_page = input().strip()
            
            if not starting_page:
                starting_page = None
            elif not starting_page.startswith('http'):
                starting_page = f"https://{starting_page}"
            
            # Execute the search with API key
            search_with_nova_act(user_input, starting_page)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            continue

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
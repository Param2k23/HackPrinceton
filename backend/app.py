# app.py
import os
from flask import Flask, request, jsonify, Response
from child_agent import child_llm_call
from parent_agent import parent_llm_call, get_parent_alert, append_to_dashboard
from elevenlabs.client import ElevenLabs
from pathlib import Path
from dotenv import load_dotenv
# --- 2. BUILD A ROBUST PATH TO THE .env FILE ---
# This finds the directory where 'app.py' lives
script_dir = Path(__file__).parent
# This points directly to the '.env' file in that same directory
env_path = script_dir / ".env"
# -----------------------------------------------

# --- 3. LOAD THE .env FILE FROM THAT EXACT PATH ---
load_dotenv(dotenv_path=env_path)
# -------------------------------------------------

# --- 4. ADD THIS PRINT STATEMENT FOR DEBUGGING ---
print(f"Loaded ElevenLabs API Key: {os.getenv('ELEVENLABS_API_KEY')}")

# --- App Initialization ---
elevenlabs = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
# Create the Flask app instance
app = Flask(__name__)
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    This is the main API endpoint for Postman.
    """
    # 1. Get JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    if 'role' not in data or 'message' not in data:
        return jsonify({"error": "Missing 'role' or 'message' in request body"}), 400
    
    role = data['role']
    if role == 'child' or role == 'son' or role == 'daughter':
        try:
            alert_data = get_parent_alert(data['message'])
            if alert_data and alert_data.get("severity") == "severe":
                # Step 3: Append to the dashboard file
                append_to_dashboard(alert_data)
        except Exception as e:
            # Don't let classification failure stop the child's chat
            print(f"Error in alert/logging pipeline: {e}")
        response_text = parent_llm_call(data['message'])
    else:
        response_text = child_llm_call(data['message'])
    # 3. Return a clean JSON response
    return jsonify({
        "role": data.get('role'),
        "response": response_text
    })

@app.route('/api/tts', methods=['POST'])
def tts_endpoint():
    """
    This is the main API endpoint for Postman.
    """
    # 1. Get JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    if 'role' not in data or 'message' not in data:
        return jsonify({"error": "Missing 'role' or 'message' in request body"}), 400
    
    role = data['role']
    if role == 'child' or role == 'son' or role == 'daughter':
        try:
            alert_data = get_parent_alert(data['message'])
            if alert_data and alert_data.get("severity") == "severe":
                # Step 3: Append to the dashboard file
                append_to_dashboard(alert_data)
        except Exception as e:
            # Don't let classification failure stop the child's chat
            print(f"Error in alert/logging pipeline: {e}")
        response_text = parent_llm_call(data['message'])
    else:
        response_text = child_llm_call(data['message'])
# --- Audio Generation and Streaming ---
    try:
        audio_stream = elevenlabs.text_to_speech.stream(
            text=response_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2"
        )
        
        # --- THIS IS THE FIX ---
        # Instead of playing the stream, return it as the HTTP response.
        # The client (Postman, web browser) will play this.
        return Response(audio_stream, mimetype="audio/mpeg")

    except Exception as e:
        print(f"Error during audio generation: {e}")
        # If audio fails, fall back to sending the text response as JSON
        return jsonify({
            "error": "Audio generation failed.",
            "response_text": response_text
        }), 500

if __name__ == '__main__':
    app.run()
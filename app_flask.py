from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Ollama host from environment variable, default to localhost
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Call Ollama API
        response = requests.post(f"{OLLAMA_HOST}/api/generate", 
            json={
                "model": "llama2",
                "prompt": user_message
            })
        
        if response.status_code == 200:
            return jsonify({'response': response.json().get('response', '')})
        else:
            return jsonify({'error': 'Failed to get response from Ollama'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

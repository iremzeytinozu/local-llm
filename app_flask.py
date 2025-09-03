from flask import Flask, request, jsonify, render_template_string
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

# Ollama API endpoint
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# HTML template for the chatbot interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Chatbot - Ollama</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .chat-container {
            width: 90%;
            max-width: 800px;
            height: 600px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .chat-header h1 {
            margin: 0;
            font-size: 24px;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: #007bff;
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.assistant .message-content {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        
        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
        }
        
        .chat-input:focus {
            border-color: #007bff;
        }
        
        .send-button {
            padding: 12px 24px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        
        .send-button:hover {
            background: #0056b3;
        }
        
        .send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #666;
            padding: 10px;
        }
        
        .model-selector {
            margin-top: 10px;
        }
        
        .model-selector select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: white;
            color: #333;
        }
        
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background: #28a745;
        }
        
        .status-offline {
            background: #dc3545;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 AI Chatbot</h1>
            <p>Ollama ile güçlendirilmiş AI asistan</p>
            <div class="model-selector">
                <label for="model-select" style="margin-right: 10px;">Model:</label>
                <select id="model-select">
                    <option value="llama3">Llama 3</option>
                    <option value="llama2">Llama 2</option>
                    <option value="mistral">Mistral</option>
                    <option value="codellama">CodeLlama</option>
                </select>
                <span id="status-indicator" class="status-indicator status-offline"></span>
                <span id="status-text">Bağlantı kontrol ediliyor...</span>
            </div>
        </div>
        
        <div class="chat-messages" id="chat-messages">
            <div class="message assistant">
                <div class="message-content">
                    Merhaba! Ben AI asistanınızım. Size nasıl yardımcı olabilirim?
                </div>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div>AI düşünüyor...</div>
        </div>
        
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="chat-input" placeholder="Mesajınızı yazın..." />
            <button class="send-button" id="send-button">Gönder</button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chat-messages');
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');
        const loading = document.getElementById('loading');
        const modelSelect = document.getElementById('model-select');
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');

        // Check server status
        async function checkStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                if (data.status === 'online') {
                    statusIndicator.className = 'status-indicator status-online';
                    statusText.textContent = 'Çevrimiçi';
                } else {
                    statusIndicator.className = 'status-indicator status-offline';
                    statusText.textContent = 'Çevrimdışı';
                }
            } catch (error) {
                statusIndicator.className = 'status-indicator status-offline';
                statusText.textContent = 'Bağlantı hatası';
            }
        }

        // Add message to chat
        function addMessage(content, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Send message
        async function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;

            const selectedModel = modelSelect.value;
            
            // Add user message
            addMessage(message, true);
            chatInput.value = '';
            
            // Show loading
            loading.style.display = 'block';
            sendButton.disabled = true;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        model: selectedModel
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage(`Hata: ${data.error}`, false);
                } else {
                    addMessage(data.response, false);
                }
            } catch (error) {
                addMessage('Bağlantı hatası oluştu. Lütfen tekrar deneyin.', false);
            }
            
            // Hide loading
            loading.style.display = 'none';
            sendButton.disabled = false;
            chatInput.focus();
        }

        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Check status on load and periodically
        checkStatus();
        setInterval(checkStatus, 30000); // Check every 30 seconds
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Ana sayfa - Chatbot arayüzü"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint - Ollama ile konuşma"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        model = data.get('model', 'llama3')
        
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz'}), 400
        
        # Ollama API'ye istek gönder
        ollama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": user_message,
                "stream": False
            },
            timeout=60
        )
        
        if ollama_response.status_code == 200:
            response_data = ollama_response.json()
            ai_response = response_data.get('response', 'Yanıt alınamadı')
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': f'Ollama API hatası: {ollama_response.status_code}'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Bağlantı hatası: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Sunucu hatası: {str(e)}'}), 500

@app.route('/status')
def status():
    """Sunucu durumu kontrolü"""
    try:
        # Ollama'nın çalışıp çalışmadığını kontrol et
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'online', 'message': 'Ollama çalışıyor'})
        else:
            return jsonify({'status': 'offline', 'message': 'Ollama yanıt vermiyor'})
    except:
        return jsonify({'status': 'offline', 'message': 'Ollama bağlantısı yok'})

@app.route('/models')
def models():
    """Mevcut modelleri listele"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({'error': 'Modeller listelenemedi'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Sağlık kontrolü endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Debug mode sadece geliştirme için
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print(f"🚀 Chatbot başlatılıyor...")
    print(f"📡 Ollama Host: {OLLAMA_HOST}")
    print(f"🌐 Web arayüzü: http://localhost:5000")
    
    app.run(
        host='0.0.0.0', 
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )

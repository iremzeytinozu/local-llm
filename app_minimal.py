from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # React frontend için CORS enable

# Ollama API konfigürasyonu
OLLAMA_API = os.getenv('OLLAMA_HOST', 'http://localhost:11434') + '/api/generate'
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3')

# Basit HTML arayüzü (React alternatifi için)
HTML_INTERFACE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Ollama Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center;
        }
        .container { 
            width: 90%; 
            max-width: 600px; 
            background: white; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 20px; 
            text-align: center; 
        }
        .chat-area { 
            height: 400px; 
            overflow-y: auto; 
            padding: 20px; 
            background: #f8f9fa;
        }
        .message { 
            margin: 10px 0; 
            padding: 10px 15px; 
            border-radius: 18px; 
            max-width: 80%; 
        }
        .user { 
            background: #007bff; 
            color: white; 
            margin-left: auto; 
            text-align: right;
        }
        .bot { 
            background: white; 
            border: 1px solid #e0e0e0; 
        }
        .input-area { 
            display: flex; 
            padding: 20px; 
            gap: 10px;
        }
        .input-area input { 
            flex: 1; 
            padding: 12px; 
            border: 2px solid #e0e0e0; 
            border-radius: 25px; 
            outline: none;
        }
        .input-area input:focus { 
            border-color: #007bff; 
        }
        .input-area button { 
            padding: 12px 20px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer;
        }
        .input-area button:hover { 
            background: #0056b3; 
        }
        .loading { 
            text-align: center; 
            color: #666; 
            padding: 10px; 
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Ollama Chatbot</h1>
            <p>Model: {{ model_name }}</p>
        </div>
        <div class="chat-area" id="chatArea">
            <div class="message bot">Merhaba! Size nasıl yardımcı olabilirim?</div>
        </div>
        <div class="loading" id="loading">AI düşünüyor...</div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Mesajınızı yazın..." onkeypress="checkEnter(event)">
            <button onclick="sendMessage()">Gönder</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const chatArea = document.getElementById('chatArea');
            const loading = document.getElementById('loading');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Kullanıcı mesajını ekle
            chatArea.innerHTML += `<div class="message user">${message}</div>`;
            input.value = '';
            loading.style.display = 'block';
            chatArea.scrollTop = chatArea.scrollHeight;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Bot yanıtını ekle
                chatArea.innerHTML += `<div class="message bot">${data.response || 'Üzgünüm, bir hata oluştu.'}</div>`;
            } catch (error) {
                chatArea.innerHTML += `<div class="message bot">Bağlantı hatası: ${error.message}</div>`;
            }
            
            loading.style.display = 'none';
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function checkEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
'''

@app.route("/chat", methods=["POST"])
def chat():
    """Ana chat endpoint - Ollama ile konuşma"""
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Mesaj boş olamaz"}), 400

        print(f"🤖 Kullanıcı: {user_message}")
        
        # Ollama API'ye isteği gönder
        response = requests.post(OLLAMA_API, json={
            "model": MODEL_NAME,
            "prompt": user_message,
            "stream": False  # Stream kapalı - basit response
        }, timeout=60)

        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data.get("response", "Yanıt alınamadı")
            
            print(f"🤖 AI: {ai_response[:100]}...")
            return jsonify({"response": ai_response})
        else:
            print(f"❌ Ollama API hatası: {response.status_code}")
            return jsonify({"error": f"Ollama API hatası: {response.status_code}"}), 500

    except requests.exceptions.RequestException as e:
        print(f"❌ Bağlantı hatası: {str(e)}")
        return jsonify({"error": f"Ollama bağlantı hatası: {str(e)}"}), 500
    except Exception as e:
        print(f"❌ Genel hata: {str(e)}")
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    """Ana sayfa - Web arayüzü"""
    return render_template_string(HTML_INTERFACE, model_name=MODEL_NAME)

@app.route("/api", methods=["GET"])
def api_info():
    """API bilgileri"""
    return jsonify({
        "message": "Ollama Chatbot API çalışıyor 🚀",
        "model": MODEL_NAME,
        "ollama_host": OLLAMA_API,
        "endpoints": {
            "/": "Web arayüzü",
            "/chat": "POST - Chat endpoint",
            "/health": "Sağlık kontrolü",
            "/models": "Mevcut modeller"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Sağlık kontrolü"""
    try:
        # Ollama'nın çalışıp çalışmadığını kontrol et
        test_response = requests.get(
            OLLAMA_API.replace('/api/generate', '/api/tags'), 
            timeout=5
        )
        
        if test_response.status_code == 200:
            return jsonify({
                "status": "healthy", 
                "ollama": "connected",
                "model": MODEL_NAME
            })
        else:
            return jsonify({
                "status": "unhealthy", 
                "ollama": "disconnected"
            }), 503
            
    except Exception as e:
        return jsonify({
            "status": "unhealthy", 
            "error": str(e)
        }), 503

@app.route("/models", methods=["GET"])
def models():
    """Mevcut modelleri listele"""
    try:
        response = requests.get(
            OLLAMA_API.replace('/api/generate', '/api/tags'), 
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "Modeller listelenemedi"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Ollama Chatbot başlatılıyor...")
    print(f"📡 Ollama Host: {OLLAMA_API}")
    print(f"🤖 Model: {MODEL_NAME}")
    print(f"🌐 Web arayüzü: http://localhost:5000")
    print(f"📋 API: http://localhost:5000/api")
    
    # Debug mode sadece geliştirme için
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    
    app.run(
        host="0.0.0.0", 
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )

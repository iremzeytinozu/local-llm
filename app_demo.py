from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

# Mock Ollama API için test responses
MOCK_RESPONSES = {
    "hello": "Merhaba! Ben bir AI asistanıyım. Size nasıl yardımcı olabilirim?",
    "test": "Test başarılı! Sistem çalışıyor.",
    "default": "Bu bir demo versiyondur. Gerçek Ollama API'si bağlandığında daha gelişmiş yanıtlar alacaksınız."
}

# Basit HTML arayüzü
HTML_INTERFACE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Ollama Chatbot - Demo</title>
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
        .demo-notice {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            text-align: center;
            font-size: 14px;
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
            <p>Railway Demo Versiyonu</p>
        </div>
        <div class="demo-notice">
            🚧 Bu demo versiyondur. Gerçek Ollama API'si için sunucu kurulumu gereklidir.
        </div>
        <div class="chat-area" id="chatArea">
            <div class="message bot">Merhaba! Bu Railway demo versiyonudur. Basit test yanıtları verebilirim.</div>
        </div>
        <div class="loading" id="loading">AI düşünüyor...</div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Mesajınızı yazın... (test, hello gibi)" onkeypress="checkEnter(event)">
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
                chatArea.innerHTML += `<div class="message bot">${data.response || 'Bir hata oluştu.'}</div>`;
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
    """Demo chat endpoint - Mock responses"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").lower()
        
        if not user_message:
            return jsonify({"error": "Mesaj boş olamaz"}), 400

        # Mock delay for realistic experience
        time.sleep(1)
        
        # Simple response logic
        if "hello" in user_message or "merhaba" in user_message:
            response = MOCK_RESPONSES["hello"]
        elif "test" in user_message:
            response = MOCK_RESPONSES["test"]
        elif any(word in user_message for word in ["nasılsın", "how are you", "naber"]):
            response = "Ben bir AI'yım, her zaman iyiyim! Siz nasılsınız?"
        elif any(word in user_message for word in ["teşekkür", "thanks", "thank you"]):
            response = "Rica ederim! Başka bir konuda yardım edebilirim."
        else:
            response = f"'{user_message}' hakkında: {MOCK_RESPONSES['default']}"
        
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    """Ana sayfa - Demo web arayüzü"""
    return render_template_string(HTML_INTERFACE)

@app.route("/api", methods=["GET"])
def api_info():
    """API bilgileri"""
    return jsonify({
        "message": "Ollama Chatbot Demo API 🚀",
        "version": "Demo v1.0",
        "mode": "railway-demo",
        "endpoints": {
            "/": "Web arayüzü",
            "/chat": "POST - Chat endpoint (demo)",
            "/health": "Sağlık kontrolü",
            "/api": "Bu bilgi sayfası"
        },
        "notice": "Bu demo versiyondur. Gerçek Ollama API'si için sunucu kurulumu gereklidir."
    })

@app.route("/health", methods=["GET"])
def health():
    """Sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "mode": "demo",
        "message": "Railway demo version running"
    })

if __name__ == "__main__":
    print("🚀 Ollama Chatbot Demo başlatılıyor...")
    print("🌐 Railway Demo Mode")
    print("💡 Bu demo versiyondur - gerçek Ollama API'si için sunucu gereklidir")
    
    app.run(
        host="0.0.0.0", 
        port=int(os.getenv('PORT', 5000)),
        debug=False
    )

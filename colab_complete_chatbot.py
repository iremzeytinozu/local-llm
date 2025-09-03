# 🤖 Ollama Chatbot - Google Colab Edition
# Bu hücreyi çalıştırarak gerçek AI chatbot'unuzu başlatın!

print("🚀 Ollama Chatbot kurulumu başlıyor...")

# 1. Gerekli kütüphaneleri yükle
!pip install pyngrok requests flask

# 2. Ollama kurulumu
!curl -fsSL https://ollama.com/install.sh | sh

# 3. Python kodlarını hazırla
import os
import threading
import time
import subprocess
from pyngrok import ngrok

# Flask uygulaması kodunu oluştur
flask_app_code = '''
from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434/api/generate"

# Modern HTML arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI Chatbot - Google Colab</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            padding: 20px;
        }
        .container { 
            width: 100%; 
            max-width: 600px; 
            background: white; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 20px; 
            text-align: center; 
        }
        .status {
            background: #d4edda;
            color: #155724;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            border-bottom: 1px solid #c3e6cb;
        }
        .chat-area { 
            height: 400px; 
            overflow-y: auto; 
            padding: 20px; 
            background: #f8f9fa;
        }
        .message { 
            margin: 10px 0; 
            padding: 12px 16px; 
            border-radius: 18px; 
            max-width: 80%; 
            word-wrap: break-word;
            line-height: 1.4;
        }
        .user { 
            background: #007bff; 
            color: white; 
            margin-left: auto; 
            text-align: right;
            border-bottom-right-radius: 4px;
        }
        .bot { 
            background: white; 
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        .loading {
            opacity: 0.6;
            font-style: italic;
        }
        .input-area { 
            display: flex; 
            padding: 20px; 
            gap: 10px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        .input-area input { 
            flex: 1; 
            padding: 12px 16px; 
            border: 2px solid #e0e0e0; 
            border-radius: 25px; 
            outline: none;
            font-size: 16px;
        }
        .input-area input:focus { 
            border-color: #007bff; 
        }
        .input-area button { 
            padding: 12px 24px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        .input-area button:hover { 
            background: #0056b3; 
        }
        .input-area button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        @media (max-width: 768px) {
            .container { margin: 10px; }
            .message { max-width: 90%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Chatbot</h1>
            <p>Google Colab + Ollama ile çalışıyor</p>
        </div>
        <div class="status">
            ✅ Gerçek AI modeli (Llama 3.2) çalışıyor!
        </div>
        <div class="chat-area" id="chatArea">
            <div class="message bot">
                Merhaba! Ben gerçek bir AI asistanıyım. Size nasıl yardımcı olabilirim? 
                Herhangi bir konu hakkında soru sorabilir, kod yazmasını isteyebilir 
                veya genel konularda sohbet edebilirsiniz!
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Mesajınızı yazın..." onkeypress="checkEnter(event)">
            <button id="sendButton" onclick="sendMessage()">Gönder</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const chatArea = document.getElementById('chatArea');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Kullanıcı mesajını ekle
            chatArea.innerHTML += `<div class="message user">${message}</div>`;
            input.value = '';
            
            // Loading mesajı ekle
            chatArea.innerHTML += `<div class="message bot loading" id="loadingMsg">🤔 AI düşünüyor...</div>`;
            chatArea.scrollTop = chatArea.scrollHeight;
            
            // Button'u disable et
            sendButton.disabled = true;
            sendButton.textContent = 'Bekleyin...';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Loading mesajını kaldır
                document.getElementById('loadingMsg').remove();
                
                // AI yanıtını ekle
                chatArea.innerHTML += `<div class="message bot">${data.response || 'Bir hata oluştu.'}</div>`;
                
            } catch (error) {
                document.getElementById('loadingMsg').innerHTML = '❌ Bağlantı hatası oluştu.';
            }
            
            // Button'u aktif et
            sendButton.disabled = false;
            sendButton.textContent = 'Gönder';
            
            chatArea.scrollTop = chatArea.scrollHeight;
            input.focus();
        }
        
        function checkEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Sayfa yüklendiğinde input'a odaklan
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('messageInput').focus();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Mesaj boş olamaz"}), 400
        
        # Ollama API'ye istek gönder
        response = requests.post(OLLAMA_API, json={
            "model": "llama3.2:1b",
            "prompt": user_message,
            "stream": False
        }, timeout=60)
        
        if response.status_code == 200:
            ai_response = response.json().get("response", "Yanıt alınamadı")
            return jsonify({"response": ai_response})
        else:
            return jsonify({"response": "AI şu anda meşgul, lütfen bir dakika bekleyip tekrar deneyin."})
            
    except requests.exceptions.Timeout:
        return jsonify({"response": "AI yanıt vermekte gecikiyor, lütfen tekrar deneyin."})
    except Exception as e:
        return jsonify({"response": f"Bir hata oluştu: {str(e)}"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "message": "Colab chatbot çalışıyor!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# Flask dosyasını yaz
with open('chatbot_app.py', 'w') as f:
    f.write(flask_app_code)

print("✅ Flask uygulaması hazırlandı!")

# 4. Ollama'yı arka planda başlat
def start_ollama():
    os.system("ollama serve")

print("🔧 Ollama servisi başlatılıyor...")
ollama_thread = threading.Thread(target=start_ollama, daemon=True)
ollama_thread.start()

# Ollama'nın başlamasını bekle
time.sleep(15)

# 5. Küçük ve hızlı model indir
print("📦 AI modeli indiriliyor... (Bu biraz zaman alabilir)")
os.system("ollama pull llama3.2:1b")

print("✅ AI modeli hazır!")

# 6. Flask uygulamasını arka planda başlat
def start_flask():
    os.system("python chatbot_app.py")

print("🌐 Web uygulaması başlatılıyor...")
flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()

# Flask'ın başlamasını bekle
time.sleep(10)

# 7. Ngrok ile public URL oluştur
print("🔗 Public URL oluşturuluyor...")
public_url = ngrok.connect(5000)

print("\n" + "="*60)
print("🎉 CHATBOT HAZIR! 🎉")
print("="*60)
print(f"🔗 Chatbot URL: {public_url}")
print("\n📋 Kullanım:")
print("1. Yukarıdaki URL'yi tarayıcıda açın")
print("2. Gerçek AI ile sohbet edin!")
print("3. Colab oturumu açık olduğu sürece çalışır")
print("\n💡 İpucu: Colab'ı arka planda bırakabilirsiniz")
print("="*60)

# URL'yi sürekli göster
try:
    while True:
        print(f"🔗 Aktif URL: {public_url}")
        time.sleep(300)  # Her 5 dakikada bir hatırlat
except KeyboardInterrupt:
    print("\n👋 Chatbot durduruldu!")

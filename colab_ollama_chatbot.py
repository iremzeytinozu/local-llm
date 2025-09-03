# Google Colab + Ngrok ile Ollama Chatbot
# Bu notebook'u Google Colab'da çalıştırın

# 1. Ollama kurulumu
!curl -fsSL https://ollama.com/install.sh | sh

# 2. Ollama'yı arka planda başlat
import subprocess
import time
import threading

def start_ollama():
    subprocess.run(["ollama", "serve"], capture_output=False)

# Ollama'yı arka planda başlat
ollama_thread = threading.Thread(target=start_ollama, daemon=True)
ollama_thread.start()

# Birkaç saniye bekle
time.sleep(10)

# 3. Model indir
!ollama pull llama3.2:1b  # Küçük model, hızlı indirme

# 4. Flask uygulaması
flask_code = '''
from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434/api/generate"

# HTML arayüzü
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Ollama Chatbot - Colab</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f2f6; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; }
        .header { text-align: center; color: #333; margin-bottom: 20px; }
        .chat-area { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; background: #fafafa; }
        .message { margin: 10px 0; padding: 8px 12px; border-radius: 15px; max-width: 80%; }
        .user { background: #007bff; color: white; margin-left: auto; text-align: right; }
        .bot { background: #e9ecef; color: #333; }
        .input-area { display: flex; gap: 10px; }
        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px; }
        .input-area button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Ollama Chatbot</h1>
            <p>Google Colab + Ngrok ile çalışıyor!</p>
        </div>
        <div class="chat-area" id="chatArea">
            <div class="message bot">Merhaba! Ben gerçek bir AI'yım. Size nasıl yardımcı olabilirim?</div>
        </div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Mesajınızı yazın..." onkeypress="checkEnter(event)">
            <button onclick="sendMessage()">Gönder</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const chatArea = document.getElementById('chatArea');
            const message = input.value.trim();
            
            if (!message) return;
            
            chatArea.innerHTML += `<div class="message user">${message}</div>`;
            input.value = '';
            chatArea.innerHTML += `<div class="message bot" style="opacity: 0.6;">AI düşünüyor...</div>`;
            chatArea.scrollTop = chatArea.scrollHeight;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Son "düşünüyor" mesajını kaldır
                const messages = chatArea.getElementsByClassName('message');
                messages[messages.length - 1].remove();
                
                chatArea.innerHTML += `<div class="message bot">${data.response || 'Bir hata oluştu.'}</div>`;
            } catch (error) {
                const messages = chatArea.getElementsByClassName('message');
                messages[messages.length - 1].innerHTML = 'Bağlantı hatası oluştu.';
            }
            
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
"""

@app.route("/")
def home():
    return render_template_string(HTML_INTERFACE)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        response = requests.post(OLLAMA_API, json={
            "model": "llama3.2:1b",
            "prompt": user_message,
            "stream": False
        }, timeout=30)
        
        if response.status_code == 200:
            ai_response = response.json().get("response", "Yanıt alınamadı")
            return jsonify({"response": ai_response})
        else:
            return jsonify({"response": "AI şu anda meşgul, lütfen tekrar deneyin."})
            
    except Exception as e:
        return jsonify({"response": f"Hata: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''

# Flask dosyasını yaz
with open('app_colab.py', 'w') as f:
    f.write(flask_code)

# 5. Ngrok kurulumu (public URL için)
!pip install pyngrok

from pyngrok import ngrok
import threading

# Flask'ı arka planda başlat
def run_flask():
    import subprocess
    subprocess.run(["python", "app_colab.py"])

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Birkaç saniye bekle
time.sleep(5)

# Ngrok tunnel oluştur
public_url = ngrok.connect(5000)
print(f"🌐 CHATBOT HAZIR! 🌐")
print(f"🔗 Public URL: {public_url}")
print(f"🤖 Bu URL'yi tarayıcıda açın ve chatbot'unuzu kullanın!")
print(f"💡 Colab oturumu açık olduğu sürece çalışacak.")

# URL'yi sürekli göster
import time
while True:
    print(f"🔗 Chatbot URL: {public_url}")
    time.sleep(60)  # Her dakika URL'yi göster

# Google Colab + Ngrok ile Ollama Chatbot
# Bu notebook'u Google Colab'da çalıştırın

# 1. Ollama kurulumu
# Aşağıdaki komutu terminalde çalıştırmalısınız:
# curl -fsSL https://ollama.com/install.sh | sh

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
subprocess.run(["ollama", "pull", "llama3.2:1b"])  # Küçük model, hızlı indirme

# 4. Flask uygulaması
flask_code = '''
from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434/api/generate"

# HTML arayüzü - Modern ve güzel tasarım
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Ollama AI Chatbot</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container { 
            max-width: 800px; 
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px; 
            padding: 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }
        
        .header { 
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white; 
            padding: 30px 20px;
            text-align: center;
            position: relative;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="20" cy="80" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="80" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="50" r="3" fill="rgba(255,255,255,0.1)"/></svg>');
        }
        
        .header h1 { 
            font-size: 2.5rem; 
            font-weight: 700;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        
        .header p { 
            opacity: 0.9; 
            font-size: 1.1rem;
            position: relative;
            z-index: 1;
        }
        
        .status-badge {
            display: inline-block;
            background: rgba(34, 197, 94, 0.2);
            color: #16a34a;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-top: 10px;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .chat-container {
            padding: 20px;
        }
        
        .chat-area { 
            height: 450px; 
            overflow-y: auto; 
            padding: 20px;
            margin-bottom: 20px; 
            background: #f8fafc;
            border-radius: 15px;
            border: 1px solid #e2e8f0;
            scroll-behavior: smooth;
        }
        
        .chat-area::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-area::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }
        
        .chat-area::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        
        .message { 
            margin: 15px 0; 
            padding: 15px 20px; 
            border-radius: 20px; 
            max-width: 80%; 
            position: relative;
            animation: fadeIn 0.3s ease-in;
            word-wrap: break-word;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user { 
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white; 
            margin-left: auto; 
            text-align: right;
            border-bottom-right-radius: 5px;
        }
        
        .bot { 
            background: white;
            color: #1f2937;
            border: 1px solid #e5e7eb;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .bot::before {
            content: '🤖';
            position: absolute;
            left: -10px;
            top: -5px;
            background: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            border: 2px solid #e5e7eb;
        }
        
        .typing-indicator {
            display: inline-block;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            padding: 15px 20px;
            position: relative;
        }
        
        .typing-dots {
            display: inline-flex;
            gap: 4px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #9ca3af;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        .input-area { 
            display: flex; 
            gap: 15px; 
            align-items: flex-end;
            background: white;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        .input-area input { 
            flex: 1; 
            padding: 15px 20px; 
            border: 1px solid #d1d5db; 
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
            background: #f9fafb;
        }
        
        .input-area input:focus {
            border-color: #4f46e5;
            background: white;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        
        .input-area button { 
            padding: 15px 25px; 
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 120px;
            justify-content: center;
        }
        
        .input-area button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
        }
        
        .input-area button:active {
            transform: translateY(0);
        }
        
        .input-area button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .welcome-message {
            text-align: center;
            color: #6b7280;
            font-style: italic;
            margin: 20px 0;
            padding: 20px;
            background: rgba(79, 70, 229, 0.05);
            border-radius: 15px;
            border: 1px dashed rgba(79, 70, 229, 0.2);
        }
        
        @media (max-width: 768px) {
            .container { margin: 10px; border-radius: 15px; }
            .header h1 { font-size: 2rem; }
            .chat-area { height: 350px; }
            .message { max-width: 90%; }
            .input-area { flex-direction: column; gap: 10px; }
            .input-area button { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> Ollama AI Chatbot</h1>
            <p>Google Colab + Ngrok ile gerçek AI deneyimi!</p>
            <span class="status-badge">
                <i class="fas fa-circle" style="color: #16a34a;"></i> Çevrimiçi
            </span>
        </div>
        
        <div class="chat-container">
            <div class="chat-area" id="chatArea">
                <div class="welcome-message">
                    <i class="fas fa-sparkles" style="color: #4f46e5; margin-right: 8px;"></i>
                    Merhaba! Ben gerçek bir AI'yım. Size nasıl yardımcı olabilirim?
                    <br><small style="margin-top: 8px; display: block; opacity: 0.7;">
                        İstediğiniz herhangi bir konuda soru sorabilir, kod yazabilirim, yaratıcı içerik üretebilirim!
                    </small>
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Mesajınızı buraya yazın..." onkeypress="checkEnter(event)" maxlength="1000">
                <button onclick="sendMessage()" id="sendBtn">
                    <i class="fas fa-paper-plane"></i>
                    Gönder
                </button>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        async function sendMessage() {
            if (isLoading) return;
            
            const input = document.getElementById('messageInput');
            const chatArea = document.getElementById('chatArea');
            const sendBtn = document.getElementById('sendBtn');
            const message = input.value.trim();
            
            if (!message) {
                input.focus();
                return;
            }
            
            // UI güncellemeleri
            isLoading = true;
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gönderiliyor...';
            
            // Kullanıcı mesajını ekle
            chatArea.innerHTML += `
                <div class="message user">
                    <i class="fas fa-user" style="margin-right: 8px;"></i>
                    ${escapeHtml(message)}
                </div>
            `;
            input.value = '';
            
            // Yazıyor göstergesi ekle
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message';
            typingDiv.innerHTML = `
                <div class="typing-indicator">
                    <i class="fas fa-robot" style="margin-right: 8px; color: #4f46e5;"></i>
                    AI düşünüyor
                    <div class="typing-dots" style="display: inline-block; margin-left: 8px;">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            `;
            chatArea.appendChild(typingDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                // Yazıyor göstergesini kaldır
                typingDiv.remove();
                
                // AI yanıtını ekle
                const botResponse = data.response || 'Yanıt alınamadı, lütfen tekrar deneyin.';
                chatArea.innerHTML += `
                    <div class="message bot">
                        ${escapeHtml(botResponse).replace(/\\n/g, '<br>')}
                    </div>
                `;
                
            } catch (error) {
                console.error('Chat error:', error);
                typingDiv.remove();
                
                chatArea.innerHTML += `
                    <div class="message bot" style="border-color: #ef4444; background: #fef2f2;">
                        <i class="fas fa-exclamation-triangle" style="color: #ef4444; margin-right: 8px;"></i>
                        Bağlantı hatası oluştu. Lütfen birkaç saniye bekleyip tekrar deneyin.
                        <br><small style="opacity: 0.7; margin-top: 5px; display: block;">
                            Hata: ${error.message}
                        </small>
                    </div>
                `;
            } finally {
                // UI'yi sıfırla
                isLoading = false;
                sendBtn.disabled = false;
                sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Gönder';
                input.focus();
                chatArea.scrollTop = chatArea.scrollHeight;
            }
        }
        
        function checkEnter(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Sayfa yüklendiğinde input'a odaklan
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('messageInput').focus();
            
            // Giriş animasyonu
            setTimeout(() => {
                document.querySelector('.container').style.transform = 'scale(1)';
                document.querySelector('.container').style.opacity = '1';
            }, 100);
        });
        
        // Container başlangıç animasyonu için CSS
        document.querySelector('.container').style.transform = 'scale(0.95)';
        document.querySelector('.container').style.opacity = '0';
        document.querySelector('.container').style.transition = 'all 0.3s ease';
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
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"response": "Lütfen bir mesaj yazın."})
        
        # Ollama API'ye istek gönder
        response = requests.post(OLLAMA_API, json={
            "model": "llama3.2:1b",
            "prompt": f"Sen yardımsever bir AI asistanısın. Türkçe yanıt ver. Kullanıcı sorusu: {user_message}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 512
            }
        }, timeout=45)
        
        if response.status_code == 200:
            ai_response = response.json().get("response", "").strip()
            if ai_response:
                return jsonify({"response": ai_response})
            else:
                return jsonify({"response": "AI şu anda yanıt veremiyor, lütfen tekrar deneyin."})
        else:
            return jsonify({
                "response": f"AI servisi geçici olarak kullanılamıyor (HTTP {response.status_code}). Lütfen birkaç saniye bekleyip tekrar deneyin."
            })
            
    except requests.exceptions.Timeout:
        return jsonify({"response": "AI yanıt verme süresi aşıldı. Lütfen daha kısa bir soru sorun veya tekrar deneyin."})
    except requests.exceptions.ConnectionError:
        return jsonify({"response": "AI servisiyle bağlantı kurulamadı. Ollama servisinin çalıştığından emin olun."})
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Server logları için
        return jsonify({"response": "Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin."})

@app.route("/health")
def health():
    """Sistem durumu kontrolü"""
    try:
        # Ollama servisini test et
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return jsonify({
                "status": "healthy",
                "ollama": "running",
                "models": [model.get("name", "") for model in models]
            })
        else:
            return jsonify({"status": "unhealthy", "ollama": "not responding"})
    except:
        return jsonify({"status": "unhealthy", "ollama": "not available"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'''

# Flask dosyasını yaz
with open('app_colab.py', 'w') as f:
    f.write(flask_code)

# 5. Ngrok kurulumu ve Flask başlatma
import subprocess
import sys

# Ngrok'u kur
subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok"], check=True)

from pyngrok import ngrok
import threading

print("🚀 Flask uygulaması başlatılıyor...")

# Flask'ı arka planda başlat
def run_flask():
    subprocess.run([sys.executable, "app_colab.py"])

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Flask'ın başlamasını bekle
print("⏳ Flask başlatılıyor...")
time.sleep(8)

print("🌐 Ngrok tunnel oluşturuluyor...")

# Ngrok tunnel oluştur
try:
    public_url = ngrok.connect(5000)
    
    print("\n" + "="*60)
    print("� CHATBOT BAŞARIYLA HAZIR! �")
    print("="*60)
    print(f"🔗 Public URL: {public_url}")
    print(f"🤖 Bu URL'yi tarayıcıda açarak chatbot'unuzu kullanın!")
    print(f"💡 Google Colab oturumu açık olduğu sürece çalışacak.")
    print(f"🔄 URL değişmeyecek, bu sekmede bırakabilirsiniz.")
    print("="*60)
    
    # Her 2 dakikada bir URL'yi göster ve durumu kontrol et
    import time
    counter = 0
    while True:
        counter += 1
        print(f"\n🟢 Aktif - {counter*2} dakika | URL: {public_url}")
        print("   � Chatbot çalışıyor, kullanıcılar bağlanabilir!")
        
        # Her 10 dakikada bir detaylı durum
        if counter % 5 == 0:
            try:
                import requests
                health_check = requests.get(f"{public_url}/health", timeout=5)
                if health_check.status_code == 200:
                    print("   ✅ Sistem sağlıklı çalışıyor")
                else:
                    print("   ⚠️  Sistem yanıt veriyor ama sorun olabilir")
            except:
                print("   ❌ Sistem kontrolü yapılamadı")
        
        time.sleep(120)  # 2 dakikada bir
        
except Exception as e:
    print(f"❌ Ngrok hatası: {e}")
    print("🔧 Çözüm önerileri:")
    print("   1. Ngrok hesabı oluşturun: https://ngrok.com")
    print("   2. Auth token'ı ayarlayın: ngrok authtoken YOUR_TOKEN")
    print("   3. Bu kodu tekrar çalıştırın")

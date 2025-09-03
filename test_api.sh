#!/bin/bash
# Hızlı test scripti

echo "🧪 Ollama Chatbot Test Başlıyor..."

# Ollama durumu kontrol
echo "1️⃣ Ollama durumu kontrol ediliyor..."
curl -s http://localhost:11434/api/tags > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Ollama çalışıyor"
else
    echo "❌ Ollama çalışmıyor! 'ollama serve' ile başlatın"
    exit 1
fi

# Flask uygulaması test
echo "2️⃣ Flask API test ediliyor..."
response=$(curl -s -w "%{http_code}" -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}' \
  -o /tmp/chat_response.json)

if [ "$response" = "200" ]; then
    echo "✅ Flask API çalışıyor"
    echo "📄 API Yanıtı:"
    cat /tmp/chat_response.json | python -m json.tool
else
    echo "❌ Flask API hatası (HTTP: $response)"
    exit 1
fi

# Health check
echo "3️⃣ Health check..."
health_status=$(curl -s http://localhost:5000/health | python -c "import sys, json; print(json.load(sys.stdin)['status'])")

if [ "$health_status" = "healthy" ]; then
    echo "✅ Sistem sağlıklı"
else
    echo "⚠️ Sistem durumu: $health_status"
fi

echo ""
echo "🎉 Test tamamlandı!"
echo "🌐 Web arayüzü: http://localhost:5000"
echo "📋 API endpoint: http://localhost:5000/chat"

# Cleanup
rm -f /tmp/chat_response.json

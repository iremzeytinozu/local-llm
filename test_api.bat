@echo off
REM Windows test scripti

echo 🧪 Ollama Chatbot Test Basliyor...

REM Ollama durumu kontrol
echo 1️⃣ Ollama durumu kontrol ediliyor...
curl -s http://localhost:11434/api/tags > nul 2>&1
if %errorlevel%==0 (
    echo ✅ Ollama calisiyir
) else (
    echo ❌ Ollama calisimiyor! 'ollama serve' ile baslatin
    exit /b 1
)

REM Flask API test
echo 2️⃣ Flask API test ediliyor...
curl -X POST http://localhost:5000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Test\"}" ^
  -o chat_response.json

if %errorlevel%==0 (
    echo ✅ Flask API calisiyor
    echo 📄 API Yaniti:
    type chat_response.json
) else (
    echo ❌ Flask API hatasi
    exit /b 1
)

REM Health check
echo 3️⃣ Health check...
curl -s http://localhost:5000/health

echo.
echo 🎉 Test tamamlandi!
echo 🌐 Web arayuzu: http://localhost:5000
echo 📋 API endpoint: http://localhost:5000/chat

REM Cleanup
del chat_response.json 2>nul

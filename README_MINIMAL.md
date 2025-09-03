# 🤖 Ollama Chatbot - Minimal Deployment Ready

Tamamen ücretsiz, production-ready Ollama chatbot sistemi.

## 📂 Proje Yapısı

```
ollama-chatbot/
├── app_minimal.py          # Flask API (Backend)
├── requirements_minimal.txt # Python dependencies
├── Dockerfile_minimal      # Docker container
└── frontend/               # React frontend (opsiyonel)
    ├── package.json
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    └── public/
        └── index.html
```

## 🚀 Hızlı Başlangıç

### 1. Yerel Test

#### Backend (Flask API):
```bash
# 1. Ollama'yı başlat
ollama serve
ollama pull llama3

# 2. Python dependencies
pip install -r requirements_minimal.txt

# 3. Flask API'yi çalıştır
python app_minimal.py
```

**Web arayüzü:** http://localhost:5000

#### API Test:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Merhaba, nasılsın?"}'
```

#### React Frontend (Opsiyonel):
```bash
cd frontend
npm install
npm start
```

**React arayüzü:** http://localhost:3000

### 2. Docker ile Çalıştırma

```bash
# Backend container
docker build -f Dockerfile_minimal -t ollama-chatbot .
docker run -p 5000:5000 -e OLLAMA_HOST=http://host.docker.internal:11434 ollama-chatbot

# Test
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Docker test"}'
```

## 🌐 Ücretsiz Deployment Seçenekleri

### Option 1: Railway (Önerilen)
1. https://railway.app → GitHub ile giriş
2. "New Project" → "Deploy from GitHub repo"
3. Environment Variables:
   ```
   OLLAMA_HOST=http://YOUR_SERVER_IP:11434
   PORT=5000
   ```
4. Deploy!

### Option 2: Render
1. https://render.com → GitHub connect
2. "New Web Service" → Bu repo
3. Build Command: `pip install -r requirements_minimal.txt`
4. Start Command: `gunicorn --bind 0.0.0.0:$PORT app_minimal:app`

### Option 3: Oracle Cloud Free Tier
```bash
# Oracle VM'de (Ubuntu)
sudo apt update
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

# Flask uygulamasını kur
git clone https://github.com/iremzeytinozu/local-llm.git
cd local-llm
pip install -r requirements_minimal.txt

# Gunicorn ile çalıştır
gunicorn --bind 0.0.0.0:5000 app_minimal:app
```

## 🔧 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/` | GET | Web arayüzü |
| `/chat` | POST | Ana chat endpoint |
| `/api` | GET | API bilgileri |
| `/health` | GET | Sağlık kontrolü |
| `/models` | GET | Mevcut modeller |

### Chat API Kullanımı:

**Request:**
```json
POST /chat
{
  "message": "Merhaba, nasılsın?"
}
```

**Response:**
```json
{
  "response": "Merhaba! Ben bir AI asistanıyım ve çok iyiyim, teşekkürler..."
}
```

## 🎯 Environment Variables

| Variable | Default | Açıklama |
|----------|---------|----------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server adresi |
| `MODEL_NAME` | `llama3` | Kullanılacak model |
| `PORT` | `5000` | Flask app portu |
| `FLASK_ENV` | `production` | Flask environment |

## 🔒 Production Optimizasyonları

### 1. Gunicorn Configuration:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app_minimal:app
```

### 2. Nginx Reverse Proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Rate Limiting:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat():
    # ...
```

## 📊 Monitoring

### Health Check:
```bash
curl http://your-app.com/health
```

### Logs:
```bash
# Railway
railway logs

# Docker
docker logs container_name

# Systemd
journalctl -u your-app
```

## 🚨 Troubleshooting

### Common Issues:

1. **Ollama Connection Error:**
   ```bash
   # Ollama durumu kontrol
   ollama list
   curl http://localhost:11434/api/tags
   ```

2. **CORS Hatası:**
   - Flask-CORS yüklü olduğundan emin olun
   - Frontend'in proxy ayarlarını kontrol edin

3. **Port Hatası:**
   - `PORT` environment variable'ını kontrol edin
   - Başka servislerin portu kullanmadığından emin olun

### Debug Mode:
```bash
FLASK_ENV=development python app_minimal.py
```

## 💰 Maliyet Analizi

### Tamamen Ücretsiz Seçenek:
- **Oracle Cloud:** Always Free (VM)
- **Railway:** $5/ay kredi (yeterli)
- **Domain:** Railway subdomain (ücretsiz)
- **SSL:** Otomatik (ücretsiz)

**Toplam: 0 TL/ay**

### Profesyonel Seçenek:
- **DigitalOcean Droplet:** $6/ay
- **Custom Domain:** $10-15/yıl
- **Cloudflare:** Ücretsiz plan

**Toplam: ~$8/ay**

## 🔄 CI/CD Pipeline

### GitHub Actions (Opsiyonel):
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          npx @railway/cli deploy
```

## 📚 Next Steps

1. **Model Optimization:** Daha küçük modeller için quantization
2. **Caching:** Redis ile response cache
3. **Authentication:** JWT token sistemi
4. **Analytics:** Conversation tracking
5. **Multi-model:** Model switching API

---

**🎉 Congratulations!** 

Artık tamamen ücretsiz, production-ready bir AI chatbot sisteminiz var!

**Demo:** https://your-app.railway.app
**API Docs:** https://your-app.railway.app/api

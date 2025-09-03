# 🤖 Ollama Chatbot

Streamlit ve Google Colab ile çalışan AI chatbot projesi.

## 📂 Proje Yapısı

```
local-llm/
├── app.py                          # Ana Streamlit uygulaması (Demo)
├── app_minimal.py                  # Flask API versiyonu
├── colab_complete_chatbot.py       # Google Colab için tam kod
├── colab_ollama_chatbot.py         # Google Colab basit versiyon
├── oracle_cloud_init.sh           # Oracle Cloud otomatik kurulum
├── requirements.txt               # Python gereksinimler
├── railway.toml                   # Railway deployment
└── Dockerfile                     # Docker container
```

## 🚀 Kullanım Seçenekleri

### 1. Streamlit Cloud Demo (Aktif)
**URL:** https://local-llm-y7mqmbxt9rlz6qfncyxvch.streamlit.app/

- ✅ Demo versiyonu çalışıyor
- 🎯 Mock responses ile test
- 📱 Web tabanlı arayüz

### 2. Google Colab (Gerçek AI)
**Dosya:** `colab_complete_chatbot.py`

```python
# Colab'da bu kodu çalıştırın
# 1. Yeni notebook oluşturun
# 2. colab_complete_chatbot.py içeriğini kopyalayın
# 3. Çalıştırın
```

- ✅ Gerçek Llama 3.2 AI modeli
- 🌐 Public URL (ngrok/localtunnel)
- 💰 Tamamen ücretsiz

### 3. Yerel Geliştirme
```bash
# Flask API
pip install -r requirements.txt
python app_minimal.py

# Streamlit
streamlit run app.py
```

## 🔧 Deployment

### Railway
```bash
# Otomatik deployment
git push origin main
# railway.toml konfigürasyonu mevcut
```

### Docker
```bash
docker build -t ollama-chatbot .
docker run -p 5000:5000 ollama-chatbot
```

### Oracle Cloud Free Tier
```bash
# VM'de çalıştırın
curl -sSL https://raw.githubusercontent.com/iremzeytinozu/local-llm/main/oracle_cloud_init.sh | bash
```

## 📋 Özellikler

- 🤖 **AI Chat:** Gerçek AI modeli desteği
- 🌐 **Web Interface:** Modern, responsive tasarım
- 📱 **Mobile Ready:** Mobil uyumlu arayüz
- 🔄 **Real-time:** Canlı sohbet deneyimi
- 💰 **Free Deployment:** Tamamen ücretsiz seçenekler

## 🛠️ Teknik Detaylar

- **Backend:** Flask / Streamlit
- **AI Model:** Ollama (Llama 3.2)
- **Frontend:** HTML/CSS/JavaScript
- **Deployment:** Railway, Streamlit Cloud, Google Colab

## 📞 Destek

- **Demo:** Streamlit Cloud üzerinde aktif
- **Gerçek AI:** Google Colab ile 5 dakikada kurulum
- **Production:** Oracle Cloud Free Tier önerilir

---
**💡 Tavsiye:** Demo'yu test edin, beğenirseniz Google Colab ile gerçek AI'yi deneyin!

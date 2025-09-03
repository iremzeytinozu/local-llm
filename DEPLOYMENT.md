# Chatbot Deployment Guide

## Sunucuya Atma Seçenekleri

### 1. Railway (En Kolay) 🚂
1. GitHub'a projeyi push edin
2. [railway.app](https://railway.app) 'e gidin
3. GitHub ile giriş yapın
4. "New Project" > "Deploy from GitHub repo"
5. Reponuzu seçin
6. Otomatik deploy olur!

**Avantajlar:**
- Ücretsiz $5/ay kredit
- Otomatik HTTPS
- Kolay setup

### 2. Streamlit Cloud (Streamlit için ideal) ☁️
1. [share.streamlit.io](https://share.streamlit.io) 'ya gidin
2. GitHub ile giriş yapın
3. Reponuzu seçin
4. `app.py` dosyasını belirtin
5. Deploy!

**Avantajlar:**
- Streamlit için optimize
- Tamamen ücretsiz
- Kolay kullanım

### 3. Heroku 🌐
```bash
# Heroku CLI kurulumu sonrası
heroku create your-app-name
git push heroku main
```

### 4. DigitalOcean App Platform 🐙
1. DigitalOcean hesabı oluşturun
2. Apps > Create App
3. GitHub reponuzu bağlayın
4. Deploy!

### 5. Render 🎨
1. [render.com](https://render.com) 'a gidin
2. GitHub ile giriş yapın
3. Web Service oluşturun
4. Reponuzu seçin

## Deployment için Gerekli Dosyalar ✅

Projenizde şu dosyalar hazır:
- `requirements.txt` - Python paketleri
- `railway.toml` - Railway konfigürasyonu
- `app_cloud.py` - Cloud-ready versiyon

## Önerilen Adımlar:

1. **GitHub'a push edin:**
```bash
git add .
git commit -m "Add deployment files"
git push origin main
```

2. **Streamlit Cloud kullanın** (en basit):
   - Ücretsiz
   - Streamlit için optimize
   - 1 dakikada deploy

3. **Railway alternatifi** (daha güçlü):
   - $5/ay ücretsiz kredit
   - Veritabanı desteği
   - Daha fazla kontrol

Hangi platformu tercih edersiniz?

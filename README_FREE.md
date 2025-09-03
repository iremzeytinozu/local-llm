# 🤖 AI Chatbot - Ollama ile Tamamen Ücretsiz Deployment

Bu proje, Ollama kullanarak tamamen ücretsiz bir AI chatbot sistemi kurar.

## 🏗️ Mimari

1. **Flask API** - Chatbot web arayüzü ve API
2. **Oracle Cloud** - Ücretsiz VM'de Ollama sunucusu
3. **Railway** - Ücretsiz web app hosting

## 🚀 Hızlı Başlangıç

### 1. Yerel Test

```bash
# Gereksinimler
pip install -r requirements_flask.txt

# Ollama'yı yerel olarak çalıştır
ollama serve
ollama pull llama3

# Flask uygulamasını başlat
python app_flask.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

### 2. Ücretsiz Oracle Cloud VM Kurulumu

#### Oracle Cloud Free Tier Hesap Oluşturma:
1. https://www.oracle.com/cloud/free/ adresine gidin
2. "Start for free" tıklayın
3. Hesap oluşturun (kredi kartı gerekir ama ücret kesilmez)

#### VM Oluşturma:
1. Oracle Cloud Console'a girin
2. "Compute" > "Instances" > "Create Instance"
3. Şu ayarları seçin:
   - **Name**: ollama-server
   - **Image**: Ubuntu 22.04
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **Network**: Public IP oluştur
   - **SSH Keys**: SSH key yükleyin veya oluşturun

#### Ollama Kurulumu:
```bash
# VM'e SSH ile bağlanın
ssh ubuntu@YOUR_VM_IP

# Kurulum scriptini çalıştırın
wget https://raw.githubusercontent.com/iremzeytinozu/local-llm/main/oracle_setup.sh
chmod +x oracle_setup.sh
./oracle_setup.sh
```

### 3. Railway'de Web App Deployment

#### Railway Hesap Oluşturma:
1. https://railway.app adresine gidin
2. GitHub hesabınızla giriş yapın

#### Deployment:
1. "New Project" > "Deploy from GitHub repo"
2. Bu repoyu seçin
3. Environment Variables ekleyin:
   ```
   OLLAMA_HOST=http://YOUR_ORACLE_VM_IP:11434
   PORT=5000
   ```
4. Deploy butonuna tıklayın

## 🔧 Yapılandırma

### Environment Variables

- `OLLAMA_HOST`: Ollama sunucu adresi
- `PORT`: Web uygulaması portu (Railway otomatik ayarlar)
- `FLASK_ENV`: development/production

### Desteklenen Modeller

- **llama3**: En güncel, güçlü model
- **llama2**: Hızlı ve efficient
- **mistral**: Kod ve matematik için iyi
- **codellama**: Programlama odaklı

## 📊 Ücretsiz Limitler

### Oracle Cloud (Always Free):
- 2x VM (ARM Ampere A1 cores)
- 1 GB RAM per VM
- 47 GB Boot Volume
- **Süresiz ücretsiz!**

### Railway (Free Plan):
- $5 kredi/ay
- 500 execution hours/ay
- Custom domain
- Auto-deploy from GitHub

## 🔒 Güvenlik

### Oracle Cloud VM:
```bash
# Güvenlik duvarı ayarları
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 11434/tcp # Ollama API

# Fail2ban kurulumu (DDoS koruması)
sudo apt install fail2ban
```

### API Rate Limiting:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 🚀 Gelişmiş Özellikler

### Custom Domain (Railway):
1. Railway dashboard'da Domains sekmesi
2. Custom domain ekle
3. DNS ayarlarını yap

### HTTPS (Otomatik):
- Railway otomatik SSL sertifikası sağlar
- Let's Encrypt kullanır

### Model Yönetimi:
```bash
# Yeni model indirme
ollama pull mistral

# Model listesi
ollama list

# Model silme
ollama rm model_name
```

## 🔍 Troubleshooting

### Oracle VM Bağlantı Problemi:
```bash
# Ollama servis durumu
sudo systemctl status ollama

# Logları kontrol et
sudo journalctl -u ollama -f

# Port kontrolü
sudo netstat -tulpn | grep 11434
```

### Railway Deployment Hatası:
```bash
# Logları kontrol et
railway logs

# Environment variables kontrol
railway variables
```

## 💡 Performans Optimizasyonu

### Oracle VM:
- Swap file oluşturun (düşük RAM için)
- Model cache'ini optimize edin
- Gereksiz servisleri kapatın

### Railway:
- Gunicorn worker sayısını ayarlayın
- Request timeout'larını optimize edin
- Health check endpoint kullanın

## 📈 Monitoring

### Basit Monitoring:
```bash
# VM kaynak kullanımı
htop

# Ollama API test
curl http://YOUR_VM_IP:11434/api/tags

# Web app health check
curl https://your-app.railway.app/health
```

## 🆘 Destek

- Issues: GitHub Issues kullanın
- Dokümantasyon: README.md
- Discord: [Ollama Community](https://discord.gg/ollama)

## 📝 Lisans

MIT License - Özgürce kullanabilirsiniz!

---

**💰 Toplam Maliyet: 0 TL/ay** (Free tier limitler dahilinde)

**⚡ Setup Süresi: ~30 dakika**

**🌟 Özellikler:**
- ✅ Tamamen ücretsiz
- ✅ Custom domain support
- ✅ HTTPS otomatik
- ✅ Auto-deploy from Git
- ✅ Professional web interface
- ✅ Multiple AI models
- ✅ Real-time chat
- ✅ Mobile responsive

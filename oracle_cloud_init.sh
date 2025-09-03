#!/bin/bash
# Oracle Cloud Free Tier - Ollama Kurulum Scripti

echo "🚀 Oracle Cloud VM - Ollama Kurulumu Başlıyor..."

# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Gerekli paketler
sudo apt install -y curl wget unzip htop git python3 python3-pip

# Ollama kurulumu
echo "📦 Ollama kuruluyor..."
curl -fsSL https://ollama.com/install.sh | sh

# Ollama'yı tüm IP'lere aç
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo '[Service]
Environment="OLLAMA_HOST=0.0.0.0"' | sudo tee /etc/systemd/system/ollama.service.d/override.conf

# Ollama servisini başlat
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Güvenlik duvarı ayarları
echo "🔒 Güvenlik duvarı yapılandırılıyor..."
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 11434/tcp # Ollama API
sudo ufw allow 5000/tcp  # Flask App
sudo ufw --force enable

# Python Flask uygulaması için gereksinimler
pip3 install flask flask-cors requests gunicorn

# Ollama modeli indir (arka planda)
echo "🤖 AI Modeli indiriliyor (bu birkaç dakika sürebilir)..."
nohup ollama pull llama3 > /tmp/ollama-pull.log 2>&1 &

# Git repo clone
cd /home/ubuntu
git clone https://github.com/iremzeytinozu/local-llm.git
cd local-llm

# Flask uygulamasını başlat
echo "🌐 Flask uygulaması başlatılıyor..."
nohup python3 app_minimal.py > /tmp/flask.log 2>&1 &

echo "✅ Kurulum tamamlandı!"
echo "📍 VM IP adresi alınıyor..."
curl -s https://ipinfo.io/ip > /tmp/vm_ip.txt

echo "🎉 Sistem hazır!"
echo "📋 Kontrol komutları:"
echo "  - Ollama durumu: systemctl status ollama"
echo "  - Flask durumu: ps aux | grep python"
echo "  - IP adresi: cat /tmp/vm_ip.txt"

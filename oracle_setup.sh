#!/bin/bash
# Oracle Cloud Free Tier VM için Ollama kurulum scripti

echo "🔧 Oracle Cloud VM'de Ollama Kurulumu Başlıyor..."

# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Gerekli paketleri kur
sudo apt install -y curl wget unzip

# Ollama kurulumu
echo "📦 Ollama kuruluyor..."
curl -fsSL https://ollama.com/install.sh | sh

# Ollama servisini başlat
sudo systemctl enable ollama
sudo systemctl start ollama

# Güvenlik duvarı ayarları
echo "🔒 Güvenlik duvarı yapılandırılıyor..."
sudo ufw allow 22/tcp
sudo ufw allow 11434/tcp
sudo ufw --force enable

# Ollama modeli indir
echo "🤖 Llama3 modeli indiriliyor..."
ollama pull llama3

# Ollama'yı harici bağlantılara aç
echo "🌐 Ollama harici erişim için yapılandırılıyor..."
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo '[Service]
Environment="OLLAMA_HOST=0.0.0.0"' | sudo tee /etc/systemd/system/ollama.service.d/override.conf

# Servisı yeniden başlat
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Durum kontrolü
echo "✅ Kurulum tamamlandı!"
echo "🔍 Ollama durumu:"
sudo systemctl status ollama --no-pager

echo ""
echo "📋 Önemli Bilgiler:"
echo "- Ollama API: http://YOUR_VM_IP:11434"
echo "- Test etmek için: curl http://YOUR_VM_IP:11434/api/tags"
echo "- Logları görmek için: sudo journalctl -u ollama -f"

# IP adresini göster
echo "🌐 VM IP Adresi:"
curl -s https://ipinfo.io/ip

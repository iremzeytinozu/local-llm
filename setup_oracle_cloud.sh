#!/bin/bash
# Oracle Cloud Free Tier - Ollama Kurulum Scripti

echo "🚀 Oracle Cloud Free Tier'da Ollama Kurulumu Başlıyor..."

# Sistem güncellemesi
echo "📦 Sistem güncelleniyor..."
sudo apt update && sudo apt upgrade -y

# Gerekli paketleri kur
sudo apt install -y curl wget git htop

# Ollama kurulumu
echo "🦙 Ollama kuruluyor..."
curl -fsSL https://ollama.com/install.sh | sh

# Systemd servis dosyası oluştur
echo "⚙️ Systemd servisi yapılandırılıyor..."
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=0.0.0.0"

[Install]
WantedBy=default.target
EOF

# Ollama kullanıcısı oluştur
sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama

# Servis başlat
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Güvenlik duvarı ayarları
echo "🔥 Güvenlik duvarı yapılandırılıyor..."
sudo ufw allow 22/tcp
sudo ufw allow 11434/tcp
sudo ufw --force enable

# Model indirme scripti oluştur
echo "📥 Model indirme scripti oluşturuluyor..."
cat > /home/ubuntu/install_models.sh << 'EOF'
#!/bin/bash
echo "Temel modeller indiriliyor..."
ollama pull llama3:8b
ollama pull llama2:7b
ollama pull mistral:7b
echo "✅ Modeller başarıyla indirildi!"
EOF

chmod +x /home/ubuntu/install_models.sh

# Otomatik başlatma scripti
echo "🔄 Otomatik başlatma yapılandırılıyor..."
cat > /home/ubuntu/start_ollama.sh << 'EOF'
#!/bin/bash
sudo systemctl start ollama
sleep 5
echo "Ollama durumu:"
sudo systemctl status ollama --no-pager
echo ""
echo "Mevcut modeller:"
ollama list
EOF

chmod +x /home/ubuntu/start_ollama.sh

echo ""
echo "✅ Kurulum tamamlandı!"
echo "📋 Sıradaki adımlar:"
echo "1. Sunucuyu yeniden başlatın: sudo reboot"
echo "2. Modelleri indirin: ./install_models.sh"
echo "3. Test edin: curl http://localhost:11434/api/tags"
echo ""
echo "🌐 Sunucu IP adresinizi not almayı unutmayın!"
echo "🔗 Railway'de OLLAMA_HOST=http://[IP-ADRES]:11434 olarak ayarlayın"

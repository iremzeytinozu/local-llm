# 🚀 Tamamen Ücretsiz Ollama Chatbot Yol Haritası

## 📋 Genel Bakış
- **Frontend**: Railway.app (Streamlit UI) - Ücretsiz
- **Backend**: Oracle Cloud Free Tier (Ollama Server) - Ücretsiz
- **Maliyet**: 0₺ / ay

## 🎯 Adım 1: Oracle Cloud Hesap Açma
1. https://cloud.oracle.com adresine git
2. "Start for free" tıkla
3. Hesap oluştur (kredi kartı gerekli ama ücret kesilmez)
4. Email doğrulama yap

## 🖥️ Adım 2: Ücretsiz VM Oluşturma
1. Oracle Cloud Console'a gir
2. **Compute** → **Instances** → **Create Instance**
3. **Ayarlar:**
   - Name: `ollama-server`
   - Image: `Ubuntu 22.04`
   - Shape: `VM.Standard.E2.1.Micro` (Always Free eligible)
   - Boot Volume: 47GB (Always Free eligible)
   - Network: Default VCN oluştur
   - SSH Keys: Generate a key pair (İndir ve sakla!)

## 🔧 Adım 3: Sunucu Kurulumu
1. SSH ile bağlan:
   ```bash
   ssh -i private_key ubuntu@[VM-IP-ADDRESS]
   ```
2. Setup scriptini çalıştır:
   ```bash
   wget https://raw.githubusercontent.com/[YOUR-USERNAME]/local-llm/main/setup_oracle_cloud.sh
   chmod +x setup_oracle_cloud.sh
   sudo ./setup_oracle_cloud.sh
   ```
3. Sunucuyu yeniden başlat:
   ```bash
   sudo reboot
   ```

## 🦙 Adım 4: Modelleri İndir
1. SSH ile tekrar bağlan
2. Modelleri indir:
   ```bash
   ./install_models.sh
   ```
3. Test et:
   ```bash
   curl http://localhost:11434/api/tags
   ```

## 🌐 Adım 5: Railway Deployment
1. https://railway.app adresine git
2. GitHub ile giriş yap
3. "Deploy from GitHub repo" seç
4. `local-llm` reposunu seç
5. **Environment Variables** ekle:
   ```
   OLLAMA_HOST=http://[ORACLE-VM-IP]:11434
   ```
6. Deploy et!

## 🔒 Adım 6: Güvenlik Ayarları
1. Oracle Cloud Console → Networking → Security Lists
2. Ingress Rules ekle:
   - Source: 0.0.0.0/0
   - Protocol: TCP
   - Port: 11434
3. SSH portunu güvenli tut (sadece gerektiğinde aç)

## ✅ Test ve Doğrulama
1. Railway URL'ini aç
2. Chatbot arayüzünü kontrol et
3. Bir mesaj gönder ve yanıt al
4. Farklı modelleri test et

## 💡 İpuçları
- **VM'yi kapat**: Kullanmadığın zaman Oracle Console'dan "Stop" et
- **Monitoring**: Oracle Cloud'da Always Free kullanım limitlerini takip et
- **Backup**: Önemli veriler için snapshots al
- **Updates**: Düzenli olarak `sudo apt update && sudo apt upgrade` çalıştır

## 🚨 Limitler (Always Free)
- **VM**: 2 OCPU, 12GB RAM (E2.1.Micro = 1 OCPU, 1GB RAM)
- **Storage**: 200GB Block Volume
- **Network**: 10TB çıkış trafiği/ay
- **Public IP**: 2 adet

## 🔗 Yararlı Linkler
- Oracle Cloud Free Tier: https://www.oracle.com/cloud/free/
- Railway Docs: https://docs.railway.app/
- Ollama Docs: https://ollama.ai/docs/

## 🎉 Sonuç
Bu kurulumla tamamen ücretsiz, kendi LLM sunucunuzla çalışan bir chatbot'a sahip olacaksınız!

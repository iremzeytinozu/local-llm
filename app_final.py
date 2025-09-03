import streamlit as st
import requests
import json
import os
from typing import Dict, Any

# Sayfa yapılandırması
st.set_page_config(
    page_title="🤖 Ücretsiz AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# CSS stil
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #007ACC;
        color: white;
        flex-direction: row-reverse;
    }
    .bot-message {
        background-color: #f1f3f4;
        color: #333;
    }
    .message-content {
        max-width: 80%;
        margin: 0 1rem;
    }
    .stAlert > div {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class OllamaAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        
    def is_connected(self) -> bool:
        """Ollama sunucusuna bağlantıyı kontrol et"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_models(self) -> list:
        """Mevcut modelleri getir"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def chat(self, model: str, message: str, context: list = None) -> str:
        """Ollama ile sohbet et"""
        try:
            # Mesaj geçmişini oluştur
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": message})
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['message']['content']
            else:
                return f"❌ Hata: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Zaman aşımı! Lütfen tekrar deneyin."
        except Exception as e:
            return f"❌ Bağlantı hatası: {str(e)}"

def main():
    st.title("🤖 Ücretsiz AI Chatbot")
    st.markdown("*Ollama ile çalışan tamamen ücretsiz chatbot*")
    
    # Sidebar - Ayarlar
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        
        # Ollama sunucu URL'si
        ollama_url = st.text_input(
            "🌐 Ollama Sunucu URL:",
            value=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            help="Ollama sunucunuzun IP adresi ve portu"
        )
        
        # Bağlantı testi
        if st.button("🔍 Bağlantı Testi"):
            with st.spinner("Bağlantı kontrol ediliyor..."):
                api = OllamaAPI(ollama_url)
                if api.is_connected():
                    st.success("✅ Bağlantı başarılı!")
                else:
                    st.error("❌ Bağlantı başarısız!")
        
        st.divider()
        
        # Model seçimi
        api = OllamaAPI(ollama_url)
        models = api.get_models()
        
        if models:
            selected_model = st.selectbox(
                "🧠 Model Seçin:",
                models,
                index=0
            )
            st.success(f"✅ {len(models)} model bulundu")
        else:
            st.warning("⚠️ Model bulunamadı!")
            selected_model = st.text_input("Model adını manuel girin:", "llama3.2")
        
        st.divider()
        
        # Geçmişi temizle
        if st.button("🧹 Sohbet Geçmişini Temizle"):
            st.session_state.messages = []
            st.rerun()
    
    # Ana alan - Sohbet
    st.header("💬 Sohbet")
    
    # Bağlantı durumu kontrolü
    api = OllamaAPI(ollama_url)
    if not api.is_connected():
        st.error("❌ Ollama sunucusuna bağlanılamıyor! Lütfen ayarları kontrol edin.")
        st.info("""
        **Ollama sunucusu nasıl kurulur?**
        1. Oracle Cloud'da ücretsiz VPS oluşturun
        2. Sunucuya bağlanın ve şu komutları çalıştırın:
        ```bash
        curl -fsSL https://ollama.com/install.sh | sh
        ollama pull llama3.2
        ollama serve --host 0.0.0.0
        ```
        3. Güvenlik duvarını açın: `sudo ufw allow 11434`
        4. Sunucu IP'nizi yukarıya girin
        """)
        return
    
    # Mesaj geçmişini başlat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <strong>Siz:</strong><br>
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-content">
                    <strong>🤖 Bot:</strong><br>
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Kullanıcı girişi
    user_input = st.chat_input("Mesajınızı buraya yazın...")
    
    if user_input:
        # Kullanıcı mesajını kaydet
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Bot yanıtını al
        with st.spinner("🤖 AI düşünüyor..."):
            # Sohbet geçmişini hazırla
            context = []
            for msg in st.session_state.messages[-10:]:  # Son 10 mesaj
                context.append({
                    "role": msg["role"] if msg["role"] != "assistant" else "assistant",
                    "content": msg["content"]
                })
            
            response = api.chat(selected_model, user_input, context[:-1])  # Son mesaj hariç
        
        # Bot yanıtını kaydet
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Sayfayı yenile
        st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        🚀 Tamamen ücretsiz AI chatbot | 
        🔧 Ollama + Streamlit ile yapılmıştır | 
        💚 Açık kaynak
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

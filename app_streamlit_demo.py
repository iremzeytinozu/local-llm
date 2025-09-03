import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="🤖 Ollama Chatbot Demo",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Ollama Chatbot - Demo Versiyonu")

# Demo notice
st.warning("🚧 Bu demo versiyondur. Gerçek Ollama API'si için sunucu kurulumu gereklidir.")

# Mock responses
MOCK_RESPONSES = {
    "hello": "Merhaba! Ben bir AI asistanıyım. Size nasıl yardımcı olabilirim?",
    "test": "Test başarılı! Sistem çalışıyor.",
    "default": "Bu bir demo versiyondur. Gerçek Ollama API'si bağlandığında daha gelişmiş yanıtlar alacaksınız."
}

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Bu demo versiyonudur. Basit test yanıtları verebilirim."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Mesajınızı yazın... (test, hello gibi)"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate mock response
    with st.chat_message("assistant"):
        with st.spinner("AI düşünüyor..."):
            time.sleep(1)  # Simulate thinking
            
            user_message = prompt.lower()
            
            if "hello" in user_message or "merhaba" in user_message:
                response = MOCK_RESPONSES["hello"]
            elif "test" in user_message:
                response = MOCK_RESPONSES["test"]
            elif any(word in user_message for word in ["nasılsın", "how are you", "naber"]):
                response = "Ben bir AI'yım, her zaman iyiyim! Siz nasılsınız?"
            elif any(word in user_message for word in ["teşekkür", "thanks", "thank you"]):
                response = "Rica ederim! Başka bir konuda yardım edebilirim."
            else:
                response = f"'{prompt}' hakkında: {MOCK_RESPONSES['default']}"
            
            st.markdown(response)
            
            # Add AI response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar info
with st.sidebar:
    st.header("ℹ️ Demo Bilgisi")
    st.info("""
    **Bu demo versiyondur!**
    
    Gerçek Ollama API'si için:
    1. Sunucu kurulumu gereklidir
    2. Oracle Cloud Free Tier kullanılabilir
    3. Docker container çalıştırılmalıdır
    
    **Test komutları:**
    - hello, merhaba
    - test
    - nasılsın
    - teşekkür
    """)
    
    st.header("🚀 Deployment")
    st.success("Streamlit Cloud: ✅ Çalışıyor")
    
    if st.button("🔄 Chat Geçmişini Temizle"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Merhaba! Bu demo versiyonudur. Basit test yanıtları verebilirim."}
        ]
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Demo Versiyonu** - Gerçek Ollama API'si için sunucu kurulumu gereklidir.")

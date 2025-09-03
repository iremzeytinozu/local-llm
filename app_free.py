import streamlit as st
import requests
import json
import os
from typing import Dict, List

# Set page config
st.set_page_config(
    page_title="Free LLM Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Get Ollama server URL from environment
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def test_ollama_connection() -> bool:
    """Test connection to Ollama server"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models() -> List[str]:
    """Get list of available models from Ollama server"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"].split(":")[0] for model in models]
        return ["llama3", "llama2"]  # fallback
    except:
        return ["llama3", "llama2"]  # fallback

def chat_with_ollama(model: str, prompt: str, context: str = "") -> str:
    """Send chat request to Ollama server"""
    try:
        full_prompt = f"""
        Context: {context}
        
        Human: {prompt}
        
        Assistant: """
        
        payload = {
            "model": model,
            "prompt": full_prompt.strip(),
            "stream": False
        }
        
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get("response", "Sorry, I couldn't generate a response.")
        else:
            return f"Error: Server returned status {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model might be too slow."
    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to Ollama server at {OLLAMA_HOST}"
    except Exception as e:
        return f"Error: {str(e)}"

# Main UI
st.title("🤖 Free LLM Chatbot")
st.markdown("**Powered by Ollama + Oracle Cloud Free Tier**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Connection status
    if test_ollama_connection():
        st.success("🟢 Connected to Ollama Server")
        available_models = get_available_models()
    else:
        st.error("🔴 Ollama Server Disconnected")
        st.warning(f"Trying to connect to: {OLLAMA_HOST}")
        available_models = ["llama3", "llama2"]
    
    model_name = st.selectbox(
        "Select Model:",
        available_models,
        index=0
    )
    
    st.markdown("---")
    st.subheader("📊 Server Info")
    st.code(f"Server: {OLLAMA_HOST}")
    
    if st.button("🔄 Test Connection"):
        if test_ollama_connection():
            st.success("✅ Connection successful!")
        else:
            st.error("❌ Connection failed!")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            # Prepare context from recent messages
            context = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in st.session_state.messages[-6:-1]  # Last 5 messages (excluding current)
            ])
            
            # Get response from Ollama
            response = chat_with_ollama(model_name, prompt, context)
            st.markdown(response)
            
            # Add to session state
            st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Messages", len(st.session_state.messages))

with col2:
    st.metric("Model", model_name)

with col3:
    connection_status = "🟢 Online" if test_ollama_connection() else "🔴 Offline"
    st.metric("Status", connection_status)

st.markdown("""
### 💡 About This Chatbot
- **100% Free** - Powered by Oracle Cloud Free Tier
- **Privacy First** - Your data stays on our servers
- **Open Source** - Built with Streamlit + Ollama
- **No API Keys** - No need for OpenAI or other paid services

**Models Available:** Llama3, Llama2, Mistral, CodeLlama and more!
""")

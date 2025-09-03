import streamlit as st
import requests
import json
import os

# Set page title and description
st.set_page_config(
    page_title="Local LLM Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Local LLM Chatbot")
st.markdown("Chat with AI models!")

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Selection
    api_type = st.selectbox(
        "Select API:",
        ["Local Ollama", "OpenAI", "Hugging Face"],
        index=0
    )
    
    if api_type == "Local Ollama":
        ollama_url = st.text_input("Ollama URL:", value="http://localhost:11434")
        model_name = st.selectbox(
            "Select Model:",
            ["llama3", "llama2", "mistral", "codellama"],
            index=0
        )
    elif api_type == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key:", type="password")
        model_name = st.selectbox(
            "Select Model:",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0
        )
    elif api_type == "Hugging Face":
        hf_api_key = st.text_input("Hugging Face API Key:", type="password")
        model_name = st.text_input("Model Name:", value="microsoft/DialoGPT-medium")
    
    temperature = st.slider(
        "Temperature (Creativity):",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    max_tokens = st.slider(
        "Maximum Tokens:",
        min_value=50,
        max_value=4096,
        value=1000,
        step=50
    )

def call_ollama(prompt, context, model, url, temperature, max_tokens):
    """Call local Ollama API"""
    try:
        full_prompt = f"""Answer the question below in a helpful and informative way.
        
Here is the conversation history: {context}

Question: {prompt}

Answer:"""
        
        response = requests.post(f"{url}/api/generate", 
                               json={
                                   "model": model,
                                   "prompt": full_prompt,
                                   "stream": False,
                                   "options": {
                                       "temperature": temperature,
                                       "num_predict": max_tokens
                                   }
                               },
                               timeout=60)
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection error: {str(e)}"

def call_openai(prompt, context, model, api_key, temperature, max_tokens):
    """Call OpenAI API"""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        
        # Add context from previous messages
        if context:
            messages.append({"role": "assistant", "content": f"Previous context: {context}"})
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"API error: {str(e)}"

def call_huggingface(prompt, context, model, api_key, temperature, max_tokens):
    """Call Hugging Face API"""
    try:
        full_prompt = f"Context: {context}\nQuestion: {prompt}\nAnswer:"
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "inputs": full_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_length": max_tokens
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "No response generated")
            return str(result)
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"API error: {str(e)}"

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Type your question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare previous messages as context
                    context = "\n".join([
                        f"{msg['role']}: {msg['content']}" 
                        for msg in st.session_state.messages[-5:]  # Last 5 messages
                    ])
                    
                    # Call appropriate API
                    if api_type == "Local Ollama":
                        response = call_ollama(prompt, context, model_name, ollama_url, temperature, max_tokens)
                    elif api_type == "OpenAI":
                        if not openai_api_key:
                            response = "Please enter your OpenAI API key in the sidebar."
                        else:
                            response = call_openai(prompt, context, model_name, openai_api_key, temperature, max_tokens)
                    elif api_type == "Hugging Face":
                        if not hf_api_key:
                            response = "Please enter your Hugging Face API key in the sidebar."
                        else:
                            response = call_huggingface(prompt, context, model_name, hf_api_key, temperature, max_tokens)
                    
                    st.markdown(response)
                    
                    # Add AI response to session state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")

with col2:
    st.subheader("📋 Usage Information")
    
    if api_type == "Local Ollama":
        st.info("""
        **Local Ollama:**
        - Make sure Ollama is running locally
        - Default URL: http://localhost:11434
        - Models need to be downloaded first
        """)
    elif api_type == "OpenAI":
        st.info("""
        **OpenAI API:**
        - Get API key from openai.com
        - Pay-per-use pricing
        - High quality responses
        """)
    elif api_type == "Hugging Face":
        st.info("""
        **Hugging Face:**
        - Free tier available
        - Many open-source models
        - Get API key from huggingface.co
        """)
    
    st.subheader("🔧 System Status")
    if st.button("Test Connection"):
        try:
            if api_type == "Local Ollama":
                response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Ollama connection successful!")
                else:
                    st.error("❌ Ollama connection failed!")
            elif api_type == "OpenAI":
                if openai_api_key:
                    st.success("✅ API key provided!")
                else:
                    st.warning("⚠️ Please enter API key")
            elif api_type == "Hugging Face":
                if hf_api_key:
                    st.success("✅ API key provided!")
                else:
                    st.warning("⚠️ Please enter API key")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Write your questions clearly and detailed for better results!")

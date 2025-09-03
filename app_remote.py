import streamlit as st
import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Set page title and description
st.set_page_config(
    page_title="Remote LLM Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Remote LLM Chatbot")
st.markdown("Chat with your Remote LLM using Ollama!")

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Server settings
    st.subheader("Server Settings")
    server_url = st.text_input(
        "Ollama Server URL:",
        value="http://your-server-ip:11434",
        help="Enter your Ollama server IP or domain"
    )
    
    model_name = st.selectbox(
        "Select Model:",
        ["llama3", "llama2", "mistral", "codellama"],
        index=0
    )
    
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
                    # Create LLM model with custom base URL
                    model = OllamaLLM(
                        model=model_name,
                        base_url=server_url,
                        temperature=temperature
                    )
                    
                    # Prompt template
                    template = """
                    Answer the question below in a helpful and informative way.
                    
                    Here is the conversation history: {context}
                    
                    Question: {question}
                    
                    Answer:
                    """
                    
                    prompt_template = ChatPromptTemplate.from_template(template)
                    chain = prompt_template | model
                    
                    # Prepare previous messages as context
                    context = "\n".join([
                        f"{msg['role']}: {msg['content']}" 
                        for msg in st.session_state.messages[-5:]  # Last 5 messages
                    ])
                    
                    # Generate response
                    response = chain.invoke({
                        "context": context,
                        "question": prompt
                    })
                    
                    st.markdown(response)
                    
                    # Add AI response to session state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")
                    st.info("Make sure your Ollama server is running and accessible.")

with col2:
    st.subheader("📋 Usage Information")
    st.info("""
    **How to Use:**
    1. Enter your Ollama server URL
    2. Select model and settings
    3. Type your question and chat!
    
    **Server Setup:**
    - Make sure port 11434 is open
    - Server needs Ollama installed
    - Models should be downloaded
    """)
    
    st.subheader("🔧 System Status")
    if st.button("Test Connection"):
        try:
            # Test server connection
            response = requests.get(f"{server_url}/api/tags")
            if response.status_code == 200:
                st.success("✅ Server connection successful!")
                # Show available models
                models = response.json().get("models", [])
                if models:
                    st.info(f"Available models: {', '.join([m['name'] for m in models])}")
            else:
                st.error(f"❌ Server error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Make sure your server has enough resources to run the selected model!")

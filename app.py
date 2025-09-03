import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Set page title and description
st.set_page_config(
    page_title="Local LLM Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Local LLM Chatbot")
st.markdown("Chat with your local LLM using Ollama!")

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
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
                    # Create LLM model
                    model = OllamaLLM(model=model_name)
                    
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
                    st.info("Make sure Ollama is running and the selected model is downloaded.")

with col2:
    st.subheader("📋 Usage Information")
    st.info("""
    **How to Use:**
    1. Select model and settings from the left sidebar
    2. Type your question in the text box below
    3. Press Enter or click the send button
    
    **Model Information:**
    - **llama3**: General purpose, powerful model
    - **llama2**: Fast and efficient
    - **mistral**: Good for code and mathematics
    - **codellama**: Programming-focused
    """)
    
    st.subheader("🔧 System Status")
    if st.button("Test Connection"):
        try:
            test_model = OllamaLLM(model=model_name)
            response = test_model.invoke("Hello")
            st.success("✅ Ollama connection successful!")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Write your questions clearly and detailed for better results!")

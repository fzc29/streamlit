# app.py
import streamlit as st
import sys
sys.path.append('.')  # Adjust to your project structure

# Import your existing functions
# from your_rag import query_index, add_document, load_faiss_index

st.set_page_config(page_title="Trade Analysis RAG", layout="wide")

# === SIDEBAR ===
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Upload section
    st.header("Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload trade data (PDF/CSV)", 
        type=['pdf', 'csv', 'txt']
    )
    
    if uploaded_file:
        if st.button("➕ Add to Index"):
            with st.spinner("Processing..."):
                # Your existing function
                # add_document(uploaded_file)
                st.success("Document added!")
    
    st.divider()
    
    # Query settings
    st.header("Query Settings")
    num_results = st.slider("Results to retrieve", 1, 10, 5)
    temperature = st.slider("Response creativity", 0.0, 1.0, 0.7)
    
    st.divider()
    
    # Index info
    st.header("Index Stats")
    # st.metric("Documents", get_doc_count())
    st.metric("Documents", "23")  # Placeholder

# === MAIN AREA ===
st.title("💼 Portfolio Analysis Assistant")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about your trades or upload new documents."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your portfolio..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            # Your existing RAG query function
            # response = query_index(prompt, num_results=num_results)
            
            # Placeholder response
            response = f"Retrieved {num_results} results for: '{prompt}'\n\n[Your RAG response would go here]"
            
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

 
import streamlit as st
from api_utils import upload_document, list_documents, delete_document
st.markdown(
    """
    <style>
    .upload {
        color: gray;
        font-size: 15px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def display_sidebar():
    # Sidebar: Model Selection
    model_options = ["mistralai/Mistral-7B-Instruct-v0.1", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"]
# First, style and render the label
    st.sidebar.markdown('<span class="upload">Select Model</span>', unsafe_allow_html=True)

    selected_model = st.sidebar.selectbox(" ", options=model_options, key="model")

    # Sidebar: Upload Document
    st.sidebar.markdown('<span class="upload">Upload Document</span>', unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html","txt"])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents()  # Refresh the list after upload

    # Sidebar: List Documents
    st.sidebar.markdown('<span class="upload">Uploaded Documents</span>',unsafe_allow_html=True)
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        
        # Delete Document
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()  # Refresh the list after deletion
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")
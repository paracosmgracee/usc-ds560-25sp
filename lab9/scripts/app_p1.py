import os
import streamlit as st
import numpy as np
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain import HuggingFacePipeline
from langchain.llms import LlamaCpp

st.set_page_config(page_title="Chat with PDFs",page_icon=":robot_face:")

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceEmbeddings(
    #     model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFacePipeline.from_model_id(
    #     model_id="lmsys/vicuna-7b-v1.3",
    #     task="text-generation",
    #     model_kwargs={"temperature": 0.01},
    # )
    # llm = LlamaCpp(
    #     model_path="models/llama-2-7b-chat.ggmlv3.q4_1.bin",  n_ctx=1024, n_batch=512)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}),
        memory=memory,
    )
    return conversation_chain


def handle_userinput(user_question):
    """Processes user questions and manages the chat history display"""
    if st.session_state.conversation is None:
        st.warning("Please upload and process documents first.")
        return
        
    with st.spinner("Thinking..."):
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            

# Function to create vector store using open-source embedding model
def get_vectorstore_opensource(text_chunks):
    """Creates embeddings using open-source Hugging Face model instead of OpenAI"""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# Function to create conversation chain using open-source LLM
def get_conversation_chain_opensource(vectorstore):
    """Creates a conversation chain using local LlamaCpp model only (no fallback)"""
    model_path = "/Users/liuyuxuan/usc-ds560-25sp/lab9/scripts/models/llama-2-7b-chat.Q4_K_M.gguf"

    if not os.path.exists(model_path):
        st.error("❌ LlamaCpp model file not found. Please make sure the model path is correct.")
        st.stop()

    llm = LlamaCpp(
        model_path=model_path,
        n_ctx=1024,
        n_batch=512,
        temperature=0.75,
        max_tokens=2000,
        top_p=1
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}),
        memory=memory
    )

    return conversation_chain


# Function to display uploaded PDF files
def display_pdf_list(pdf_docs):
    """Displays a list of uploaded PDF files with information"""
    if pdf_docs:
        st.markdown("### Uploaded Files")
        for doc in pdf_docs:
            st.markdown(f"📄 {doc.name}")
        return True
    return False


# Function to save uploaded files locally
def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to a temporary directory"""
    import os
    
    # Create temporary directory if it doesn't exist
    temp_dir = "temp_pdfs"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Save the file
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


# Driver Function
def run_driver_function():
    print("=== PDF Q&A Chatbot (Command Line Mode) ===")
    pdf_path = input("Enter the path to your PDF file: ").strip()

    if not os.path.exists(pdf_path):
        print("❌ File does not exist.")
        return

    # Step 1: Extract text
    print("[+] Extracting text from PDF...")
    text = get_pdf_text([pdf_path])

    # Step 2: Chunk text
    print("[+] Chunking text...")
    chunks = get_text_chunks(text)

    # Step 3: Create embeddings and vector store
    print("[+] Creating vector store using HuggingFace embeddings...")
    vectorstore = get_vectorstore_opensource(chunks)

    # Step 4: Load LLM and build conversation chain
    print("[+] Loading local LlamaCpp model...")
    conversation = get_conversation_chain_opensource(vectorstore)

    print("\n✅ Setup complete. You can now ask questions about the PDF.")
    print("Type 'exit' to quit.\n")

    chat_history = []

    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            print("👋 Goodbye!")
            break

        try:
            response = conversation({"question": query})
            answer = response["answer"]
            chat_history = response.get("chat_history", [])

            # Print last round clearly
            print("Bot:", answer)

            # Optional: Show full chat history (more readable)
            print("\n📝 Chat History So Far:")
            for i, msg in enumerate(chat_history):
                role = "You" if i % 2 == 0 else "Bot"
                print(f"{role}: {msg.content}")
            print("-" * 40)

        except Exception as e:
            print("⚠️ Error during response:", e)


# Main Function
def main():
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDFs :robot_face:")
    user_question = st.text_input("Ask questions about your documents:")
    if user_question:
        handle_userinput(user_question)

with st.sidebar:
    st.subheader("Your documents")
    
    # Enhanced file upload section
    pdf_docs = st.file_uploader(
        "Upload your PDFs here", accept_multiple_files=True)
    
    # Display uploaded files
    if display_pdf_list(pdf_docs):
        # Add model selection option
        model_option = st.radio(
            "Choose Model",
            ("OpenAI (API Key Required)", "Open Source (Local)")
        )
        
        if st.button("Process Documents"):
            if not pdf_docs:
                st.error("Please upload PDF files first.")
                st.stop()
                
            with st.spinner("Processing your documents..."):
                # Save uploaded files (optional)
                file_paths = []
                for pdf in pdf_docs:
                    file_path = save_uploaded_file(pdf)
                    file_paths.append(file_path)
                
                # Process PDF text
                raw_text = get_pdf_text(pdf_docs)
                st.info(f"Total extracted text: {len(raw_text)} characters")
                
                # Create text chunks
                text_chunks = get_text_chunks(raw_text)
                st.info(f"Created {len(text_chunks)} text chunks")
                
                # Create vector store and conversation chain based on user's model choice
                if model_option == "OpenAI (API Key Required)":
                    with st.spinner("Creating embeddings with OpenAI..."):
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                else:
                    with st.spinner("Creating embeddings with open source model..."):
                        vectorstore = get_vectorstore_opensource(text_chunks)
                        st.session_state.conversation = get_conversation_chain_opensource(vectorstore)
                
                st.success("✅ Processing complete! You can now ask questions about your documents.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        run_driver_function()
    else:
        main()
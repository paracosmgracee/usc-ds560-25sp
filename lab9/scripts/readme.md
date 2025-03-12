# Lab 9 - PDF Q&A Chatbot Project

## 📘 Project Overview
This project builds a Q&A chatbot that allows users to upload PDF documents and interact with them via natural language queries. The system uses embedding techniques and large language models (LLMs) to answer questions based on PDF content.

## ✨ Key Features
- Support for multiple PDF uploads
- Two interfaces: Web (Streamlit) and Command-Line (Driver Function)
- Embedding models: OpenAI or HuggingFace MiniLM
- Language models: OpenAI GPT or Local LlamaCpp (GGUF format)
- Vector database using FAISS
- Chat history tracking using LangChain ConversationBufferMemory

## 🗂 Folder Structure
```
lab9/
├── scripts/
│   └── app_p1.py
├── htmlTemplates.py
├── models/
│   └── llama-2-7b-chat.Q4_K_M.gguf
├── temp_pdfs/
├── pdfs/
├── README.md
└── requirements.txt
```

## 🛠 Setup Instructions
### Install Required Packages
```
pip install -r requirements.txt
```

### Download Llama Model (if using local model)
Place the `.gguf` model file in the `models/` directory.

## 🚀 How to Run
### Option 1: Web UI (Streamlit)
```
streamlit run scripts/app_p1.py
```

### Option 2: Command Line Interface
```
python scripts/app_p1.py cli
```

## 📋 Usage Flow
1. Upload PDFs via sidebar (Streamlit) or input path in CLI
2. Text will be extracted and chunked
3. Embeddings will be created and stored in FAISS
4. LLM will answer your questions using similarity search and memory

## 📎 Notes
- CLI mode supports full chat history printing
- Web UI has formatted bot/user avatars using htmlTemplates
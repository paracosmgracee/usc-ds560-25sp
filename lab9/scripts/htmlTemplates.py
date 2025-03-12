css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

/* New Pattern */
.stApp {
    background-color: #f0f2f6;
}
.sidebar .sidebar-content {
    background-color: #f9f9f9;
}
.upload-section {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #ffffff;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.file-list {
    margin-top: 1rem;
}
.file-item {
    padding: 0.5rem;
    border-radius: 0.3rem;
    background-color: #e1e9ff;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}
.sidebar-header {
    color: #1f2937;
    font-weight: 600;
    margin-bottom: 1rem;
}
</style>
'''

# PDF Upload Template
pdf_upload_template = '''
<div class="upload-section">
    <h3>Upload Your PDFs</h3>
    <p>Upload PDF documents to chat with them</p>
</div>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/0c/Chatbot_img.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

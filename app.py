import streamlit as st
from agent import chat
import PyPDF2
import io
from docx import Document
from memory import get_recent_conversations

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0f13;
    color: #e8e8f0;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 760px;
}

.title-block {
    text-align: center;
    padding: 2rem 0 1.5rem 0;
}
.title-block h1 {
    font-size: 2rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.title-block p {
    font-size: 0.85rem;
    color: #6b6b80;
    font-weight: 300;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.memory-badge {
    display: inline-block;
    background: #1a1025;
    border: 1px solid #7c3aed;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    color: #c4b5fd;
    margin-top: 0.5rem;
}

[data-testid="stFileUploader"] {
    background: #16161f;
    border: 1px solid #2a2a38;
    border-radius: 12px;
    padding: 1rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c3aed;
}

[data-testid="stAlert"] {
    background: #1a1025 !important;
    border: 1px solid #7c3aed !important;
    border-radius: 8px !important;
    color: #c4b5fd !important;
    font-size: 0.85rem;
}

hr {
    border: none;
    border-top: 1px solid #1e1e2a;
    margin: 1.5rem 0;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #1e1030;
    border: 1px solid #3b1f6b;
    border-radius: 16px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #16161f;
    border: 1px solid #2a2a38;
    border-radius: 16px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

[data-testid="stChatInput"] {
    background: #16161f !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: #7c3aed !important;
    border-radius: 8px !important;
}
[data-testid="stChatInputSubmitButton"]:hover {
    background: #6d28d9 !important;
}

h3 {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #6b6b80 !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0f0f13; }
::-webkit-scrollbar-thumb { background: #2a2a38; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #7c3aed; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
recent = get_recent_conversations()
memory_count = len(recent)

st.markdown(f"""
<div class="title-block">
    <h1>✦ Personal AI Assistant</h1>
    <p>Powered by Claude & Tavily Search</p>
    <span class="memory-badge">🧠 {memory_count} memories stored</span>
</div>
""", unsafe_allow_html=True)

# ── Document upload ───────────────────────────────────────────
st.subheader("📄 Document Reader (Optional)")
uploaded_file = st.file_uploader(
    "Upload a PDF, TXT or Word document",
    type=["pdf", "txt", "docx"],
    label_visibility="collapsed"
)

document_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            document_text += page.extract_text()
        st.success("✓ PDF uploaded successfully")
    elif uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode("utf-8")
        st.success("✓ Text file uploaded successfully")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(io.BytesIO(uploaded_file.read()))
        for paragraph in doc.paragraphs:
            document_text += paragraph.text + "\n"
        st.success("✓ Word document uploaded successfully")

st.divider()

# ── Voice Input ───────────────────────────────────────────────
st.subheader("🎙️ Voice Input (Optional)")
st.caption("Click record and speak — it will send automatically")

# Session state for voice
if "voice_transcript" not in st.session_state:
    st.session_state.voice_transcript = ""
if "voice_pending" not in st.session_state:
    st.session_state.voice_pending = False

st.components.v1.html("""
<script>
let recognition;
let isRecording = false;

function toggleRecording() {
    if (!isRecording) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('btn').innerText = '🎙️ Click to record';
            document.getElementById('status').innerText = '✓ Heard: ' + transcript;
            isRecording = false;

            // Find the chat input and fill it, then submit
            setTimeout(function() {
                const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                if (chatInput) {
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set;
                    nativeInputValueSetter.call(chatInput, transcript);
                    chatInput.dispatchEvent(new Event('input', { bubbles: true }));
                    setTimeout(function() {
                        chatInput.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            which: 13,
                            bubbles: true
                        }));
                    }, 100);
                }
            }, 300);
        };

        recognition.onerror = function(event) {
            document.getElementById('status').innerText = '❌ Error: ' + event.error;
            document.getElementById('btn').innerText = '🎙️ Click to record';
            isRecording = false;
        };

        recognition.onend = function() {
            isRecording = false;
            document.getElementById('btn').innerText = '🎙️ Click to record';
        };

        recognition.start();
        isRecording = true;
        document.getElementById('btn').innerText = '⏹️ Recording... click to stop';
        document.getElementById('status').innerText = 'Listening...';
    } else {
        recognition.stop();
    }
}
</script>
<button id="btn" onclick="toggleRecording()" style="
    background: #7c3aed;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.25rem;
    font-size: 0.9rem;
    cursor: pointer;
    font-family: sans-serif;
">🎙️ Click to record</button>
<p id="status" style="color: #c4b5fd; font-size: 0.8rem; margin-top: 0.5rem; font-family: sans-serif;"></p>
""", height=80)

st.divider()

# ── Chat ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    if document_text:
        max_chars = 50000
        truncated_text = document_text[:max_chars]
        full_prompt = f"The user has uploaded a document (showing first portion). Here is its content:\n\n{truncated_text}\n\nUser question: {prompt}"
    else:
        full_prompt = prompt

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(full_prompt)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
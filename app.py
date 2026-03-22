import streamlit as st
from agent import chat
import PyPDF2
import io
from docx import Document
from memory import get_recent_conversations

st.set_page_config(
    page_title="Ruby AI Assistant",
    page_icon="💎",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Raleway:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Raleway', sans-serif;
    color: #e8e8f0;
}

[data-testid="stAppViewContainer"] {
    background: #03010a;
    position: relative;
}

/* ── Nebula glow layers ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(ellipse 60% 40% at 15% 50%, rgba(138, 43, 226, 0.12) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 85% 30%, rgba(255, 20, 147, 0.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 30% at 50% 80%, rgba(75, 0, 130, 0.1) 0%, transparent 70%),
        radial-gradient(1px 1px at 5% 8%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 12% 22%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 18% 45%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 23% 67%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 28% 12%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 33% 78%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 38% 35%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 42% 55%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 47% 88%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 52% 18%, white 0%, transparent 100%),
        radial-gradient(2px 2px at 57% 42%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 62% 72%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 67% 28%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 72% 58%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 77% 15%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 82% 82%, rgba(255,179,179,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 87% 38%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 92% 65%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 96% 92%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 3% 95%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 8% 52%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 33%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 85%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 5%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 30% 48%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 35% 93%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 25%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 70%, white 0%, transparent 100%),
        radial-gradient(2px 2px at 50% 3%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 62%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 87%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 10%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 70% 40%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 75%, rgba(255,179,179,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 20%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 50%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 30%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 95% 10%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 10% 60%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 44% 44%, white 0%, transparent 100%);
    animation: twinkle1 3s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(ellipse 70% 50% at 70% 60%, rgba(186, 85, 211, 0.07) 0%, transparent 60%),
        radial-gradient(ellipse 30% 40% at 30% 20%, rgba(255, 105, 180, 0.06) 0%, transparent 60%),
        radial-gradient(1px 1px at 7% 18%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 14% 38%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 21% 58%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 29% 2%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 36% 72%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 43% 15%, white 0%, transparent 100%),
        radial-gradient(2px 2px at 49% 80%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 54% 32%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 59% 96%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 63% 50%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 68% 7%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 73% 63%, rgba(255,179,179,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 78% 85%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 83% 45%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 22%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 93% 75%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 97% 55%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 2% 42%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 16% 90%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 26% 28%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 32% 62%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 37% 8%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 46% 98%, white 0%, transparent 100%),
        radial-gradient(2px 2px at 53% 48%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 58% 20%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 66% 83%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 71% 35%, rgba(255,179,179,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 76% 58%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 81% 12%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 86% 68%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 91% 40%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 94% 92%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 4% 75%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 11% 15%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 19% 48%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 27% 88%, white 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 34% 20%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 41% 65%, rgba(224,176,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 48% 38%, white 0%, transparent 100%),
        radial-gradient(1px 1px at 56% 78%, white 0%, transparent 100%);
    animation: twinkle2 4s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes twinkle1 {
    0% { opacity: 0.4; }
    100% { opacity: 1; }
}

@keyframes twinkle2 {
    0% { opacity: 1; }
    100% { opacity: 0.3; }
}

/* ── Shooting stars ── */
.shooting-star {
    position: fixed;
    width: 180px;
    height: 2px;
    border-radius: 50px;
    background: linear-gradient(90deg, transparent, rgba(213,0,249,0.6), white);
    animation: shoot linear infinite;
    pointer-events: none;
    z-index: 0;
}
.s1 { top: 12%; left: -180px; animation-duration: 4s; animation-delay: 1s; }
.s2 { top: 28%; left: -180px; animation-duration: 5s; animation-delay: 4s; }
.s3 { top: 7%;  left: -180px; animation-duration: 6s; animation-delay: 7s; }
.s4 { top: 48%; left: -180px; animation-duration: 4.5s; animation-delay: 11s; }

@keyframes shoot {
    0%   { left: -180px; opacity: 0; }
    5%   { opacity: 1; }
    85%  { opacity: 0.8; }
    100% { left: 110%; opacity: 0; }
}

/* ── Planet ── */
.planet {
    position: fixed;
    bottom: 35%;
    right: 3%;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #6b21a8, #1e0533 60%, #0a0118);
    box-shadow:
        0 0 40px rgba(139, 92, 246, 0.3),
        0 0 80px rgba(139, 92, 246, 0.15),
        inset -20px -10px 40px rgba(0,0,0,0.6);
    pointer-events: none;
    z-index: 0;
    animation: planetFloat 8s ease-in-out infinite;
}
.planet::before {
    content: '';
    position: absolute;
    top: 50%;
    left: -20%;
    width: 140%;
    height: 30%;
    border-radius: 50%;
    border: 2px solid rgba(139, 92, 246, 0.3);
    transform: translateY(-50%) rotateX(75deg);
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.2);
}
.planet::after {
    content: '';
    position: absolute;
    top: 15%;
    left: 20%;
    width: 25%;
    height: 15%;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    filter: blur(4px);
}

@keyframes planetFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 760px;
    position: relative;
    z-index: 1;
}

/* ── Title ── */
.title-block {
    text-align: center;
    padding: 2rem 0 1.5rem 0;
}
.ruby-avatar { width: 80px; height: 80px; margin: 0 auto 1rem; }

.ruby-gem {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #ff1744 0%, #d500f9 40%, #ff4081 70%, #ff6d00 100%);
    clip-path: polygon(50% 0%, 100% 35%, 85% 100%, 15% 100%, 0% 35%);
    position: relative;
    animation: gemPulse 2.5s ease-in-out infinite;
}
.ruby-gem::after {
    content: '';
    position: absolute;
    top: 15%; left: 25%;
    width: 25%; height: 20%;
    background: rgba(255,255,255,0.4);
    clip-path: polygon(0% 0%, 100% 0%, 60% 100%, 0% 50%);
    border-radius: 2px;
}

@keyframes gemPulse {
    0%, 100% {
        box-shadow: 0 0 20px rgba(255,23,68,0.6), 0 0 40px rgba(213,0,249,0.4), 0 0 80px rgba(213,0,249,0.2);
        filter: brightness(1);
    }
    50% {
        box-shadow: 0 0 40px rgba(255,23,68,1), 0 0 80px rgba(213,0,249,0.8), 0 0 120px rgba(213,0,249,0.4), 0 0 160px rgba(255,23,68,0.2);
        filter: brightness(1.2);
    }
}

.title-block h1 {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: #ffffff;
    margin-bottom: 0.25rem;
    text-shadow: 0 0 20px rgba(213,0,249,0.6), 0 0 40px rgba(213,0,249,0.3);
}
.title-block p {
    font-size: 0.75rem;
    color: #7b6b8a;
    font-weight: 400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.memory-badge {
    display: inline-block;
    background: rgba(120,40,140,0.2);
    border: 1px solid rgba(213,0,249,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.7rem;
    color: #e0b0ff;
    margin-top: 0.5rem;
    backdrop-filter: blur(10px);
    letter-spacing: 0.05em;
    font-family: 'Orbitron', monospace;
}

/* ── Section headers ── */
h3 {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7b6b8a !important;
    font-family: 'Orbitron', monospace !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: rgba(213,0,249,0.4); }

[data-testid="stAlert"] {
    background: rgba(120,40,140,0.15) !important;
    border: 1px solid rgba(213,0,249,0.3) !important;
    border-radius: 12px !important;
    color: #e0b0ff !important;
    font-size: 0.85rem;
    backdrop-filter: blur(10px);
}

hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,23,68,0.07);
    border: 1px solid rgba(255,23,68,0.2);
    border-radius: 20px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 24px rgba(255,23,68,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(213,0,249,0.07);
    border: 1px solid rgba(213,0,249,0.2);
    border-radius: 20px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 24px rgba(213,0,249,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
}

[data-testid="stChatInput"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 50px !important;
    color: #e8e8f0 !important;
    font-family: 'Raleway', sans-serif !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(213,0,249,0.5) !important;
    box-shadow: 0 0 0 3px rgba(213,0,249,0.1), 0 0 20px rgba(213,0,249,0.15) !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #ff1744, #d500f9) !important;
    border-radius: 50% !important;
}
[data-testid="stBottom"] {
    background: transparent !important;
    backdrop-filter: none !important;
}
[data-testid="stBottom"] > div {
    background: transparent !important;
}
[data-testid="stBottom"] > div > div {
    background: transparent !important;
}

section[data-testid="stBottom"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(213,0,249,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(213,0,249,0.6); }
</style>

<div class="shooting-star s1"></div>
<div class="shooting-star s2"></div>
<div class="shooting-star s3"></div>
<div class="shooting-star s4"></div>
<div class="planet"></div>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
recent = get_recent_conversations()
memory_count = len(recent)

st.markdown(f"""
<div class="title-block">
    <div class="ruby-avatar">
        <div class="ruby-gem"></div>
    </div>
    <h1>RUBY</h1>
    <p>Deep Space AI Assistant</p>
    <span class="memory-badge">🛸 {memory_count} light years of memory</span>
</div>
""", unsafe_allow_html=True)

# ── Document upload ───────────────────────────────────────────
st.subheader("🛰️ Mission Control (Optional)")
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
        st.success("✓ Document received at mission control")
    elif uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode("utf-8")
        st.success("✓ Transmission received")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(io.BytesIO(uploaded_file.read()))
        for paragraph in doc.paragraphs:
            document_text += paragraph.text + "\n"
        st.success("✓ Document received at mission control")

st.divider()

# ── Voice Input ───────────────────────────────────────────────
st.subheader("📡 Transmission (Optional)")
st.caption("Click record and speak — your message will transmit automatically")

st.components.v1.html("""
<script>
let recognition;
let isRecording = false;

const supported = ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window);

if (!supported) {
    document.getElementById('btn').style.display = 'none';
    document.getElementById('status').innerText = '⚠️ Voice transmission not available on iPhone/iPad. Please type your message below.';
    document.getElementById('status').style.color = '#ffb3b3';
}

function toggleRecording() {
    if (!supported) return;
    if (!isRecording) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('btn').innerText = '📡 Begin Transmission';
            document.getElementById('status').innerText = '✓ Transmission received: ' + transcript;
            isRecording = false;

            setTimeout(function() {
                const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                if (chatInput) {
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set;
                    nativeInputValueSetter.call(chatInput, transcript);
                    chatInput.dispatchEvent(new Event('input', { bubbles: true }));
                    setTimeout(function() {
                        chatInput.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
                        }));
                    }, 100);
                }
            }, 300);
        };

        recognition.onerror = function(event) {
            document.getElementById('status').innerText = '❌ Transmission failed: ' + event.error;
            document.getElementById('btn').innerText = '📡 Begin Transmission';
            isRecording = false;
        };

        recognition.onend = function() {
            isRecording = false;
            document.getElementById('btn').innerText = '📡 Begin Transmission';
        };

        recognition.start();
        isRecording = true;
        document.getElementById('btn').innerText = '⏹️ Transmitting... click to stop';
        document.getElementById('status').innerText = 'Listening to transmission...';
    } else {
        recognition.stop();
    }
}
</script>
<button id="btn" onclick="toggleRecording()" style="
    background: linear-gradient(135deg, #ff1744, #d500f9);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.6rem 1.8rem;
    font-size: 0.85rem;
    cursor: pointer;
    font-family: sans-serif;
    box-shadow: 0 4px 20px rgba(213, 0, 249, 0.4);
    letter-spacing: 0.05em;
    text-transform: uppercase;
">📡 Begin Transmission</button>
<p id="status" style="color: #e0b0ff; font-size: 0.8rem; margin-top: 0.5rem; font-family: sans-serif;"></p>
""", height=80)

st.divider()

# ── Chat ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Send transmission to Ruby...")

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
        with st.spinner("Ruby is scanning the cosmos..."):
            response = chat(full_prompt)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ── Export Chat ───────────────────────────────────────────────
if st.session_state.get("messages"):
    st.divider()
    st.subheader("🌌 Export Transmission Log")
    col1, col2 = st.columns(2)

    with col1:
        chat_text = ""
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Ruby"
            chat_text += f"{role}:\n{msg['content']}\n\n"
        st.download_button(
            label="📥 Export as TXT",
            data=chat_text,
            file_name="ruby_transmission.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        chat_md = "# Ruby Transmission Log\n\n"
        for msg in st.session_state.messages:
            role = "**You**" if msg["role"] == "user" else "**Ruby**"
            chat_md += f"{role}:\n{msg['content']}\n\n---\n\n"
        st.download_button(
            label="📥 Export as Markdown",
            data=chat_md,
            file_name="ruby_transmission.md",
            mime="text/markdown",
            use_container_width=True
        )
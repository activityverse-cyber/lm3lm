import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ستايل "الحريفية" - مقاد للتليفون وللعربية
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* مقاسات خاصة للتليفون */
    .main { padding: 10px; }
    
    .stChatInput { bottom: 20px !important; }
    
    .stMarkdown { text-align: right; direction: rtl; }

    /* ستايل فقاعات الدردشة */
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        line-height: 1.6;
        display: block;
        width: 100%;
    }
    .user-bubble { background-color: #e3f2fd; border-right: 5px solid #2196f3; color: #0d47a1; }
    .teacher-bubble { background-color: #f1f8e9; border-right: 5px solid #4caf50; color: #1b5e20; }
    
    /* أيقونات الأزرار */
    .stButton>button { width: 100%; border-radius: 10px; height: 45px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط (الساروت) والذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # استعملنا 1.5-flash حيت هو اللي كيفهم الدارجة والصوت مزيان
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما راكبش!")
    st.stop()

# 3. واجهة التطبيق (كلشي فـ الوسط باش يبان فـ التليفون)
st.title("👨‍🏫 تطبيق LM3LM")
st.write("مساعدك الذكي: صور، تكلم، أو اكتب")

# --- أزرار الأدوات (التصوير والرفع) ---
col1, col2 = st.columns(2)
with col1:
    cam_file = st.camera_input("📸 صور التمرين")
with col2:
    upload_file = st.file_uploader("📁 ارفع صورة", type=["jpg", "png", "jpeg"])

# أيقونة الميكرو (تحت الصور ديريكت)
audio_file = st.audio_input("🎙️ سجل سؤالك بالصوت")

st.divider()

# --- عرض الحوار ---
for msg in st.session_state.messages:
    bubble_type = "user-bubble" if msg["role"] == "user" else "teacher-bubble"
    st.markdown(f'<div class="chat-bubble {bubble_type}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- صندوق الكتابة (Input) ---
prompt = st.chat_input("اكتب سؤالك هنا...")

# --- المعالجة (Logic) ---
if prompt or cam_file or upload_file or audio_file:
    # تحديد الصورة المستخدمة
    img = None
    if cam_file: img = Image.open(cam_file)
    elif upload_file: img = Image.open(upload_file)
    
    # تحضير السؤال للمدرب
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("assistant"):
        with st.spinner("لمعلم كيجاوب..."):
            try:
                # محتوى السؤال (نص + صورة + صوت)
                parts = ["أنت 'لمعلم' خبير مغربي. جاوب على سؤال التلميذ بالدارجة المغربية بأسلوب مشجع. اشرح الصور بوضوح واسمع الصوت إذا وجد."]
                if prompt: parts.append(prompt)
                if img: parts.append(img)
                if audio_file: parts.append({"mime_type": "audio/wav", "data": audio_file.getvalue()})

                response = model.generate_content(parts)
                st.markdown(f'<div class="chat-bubble teacher-bubble">{response.text}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

# زر مسح الحوار (فـ اللخر)
if st.button("🗑️ تمسح الحوار؟"):
    st.session_state.messages = []
    st.rerun()

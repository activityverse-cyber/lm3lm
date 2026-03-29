import streamlit as st
import google.generativeai as genai
from PIL import Image
import hashlib

# 1. الستايل الاحترافي (RTL 100% & Premium UI)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8f9fa;
    }
    .stChatMessage { direction: rtl !important; text-align: right !important; }
    .assistant-bubble { background-color: #ffffff; border-right: 5px solid #1e3c72; padding: 15px; border-radius: 12px; color: #1e3c72 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .user-bubble { background-color: #e3f2fd; border-right: 5px solid #2196f3; padding: 15px; border-radius: 12px; color: #0d47a1 !important; }
    .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط الذكي بالساروت (الرادار)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def find_working_model():
        # كيسول السيرفر على الموديلات اللي خدامين عندك دابا فعلياً
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash_models = [m for m in models if "flash" in m]
        return flash_models[0] if flash_models else models[0]
    
    WORKING_MODEL = find_working_model()
except Exception as e:
    st.error(f"⚠️ مشكل فـ الساروت أو الاتصال: {e}")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "last_hash" not in st.session_state: st.session_state.last_hash = ""

# 3. الواجهة الرئيسية
st.markdown(f'<div class="hero"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>ذكاء اصطناعي مغربي مسكد 🇲🇦</p></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    style = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{style}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. أدوات الإدخال (Sidebar)
with st.sidebar:
    st.header("🛠️ الأدوات")
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    if st.button("🗑️ مسح الحوار"):
        st.session_state.messages = []
        st.session_state.last_hash = ""
        st.rerun()

prompt = st.chat_input("اكتب سؤالك هنا...")

# 5. المنطق: منع التكرار ومعالجة الطلب
if prompt or uploaded_file:
    # بصمة رقمية (Hash) باش نعرفو واش السؤال تعاود
    current_input = f"{prompt}_{uploaded_file.name if uploaded_file else ''}"
    current_hash = hashlib.md5(current_input.encode()).hexdigest()

    if current_hash != st.session_state.last_hash:
        user_text = prompt if prompt else "شرح ليا هاد التمرين"
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيشوف الحل..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية باختصار وبأسلوب مشجع. ابدأ دائماً من اليمين."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    answer = response.text
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.last_hash = current_hash
                    st.rerun()
                except Exception as e:
                    st.error(f"مشكل تقني: {e}")

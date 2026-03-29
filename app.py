import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل الاحترافي (Pro UI) - مقاد للتليفون وللعربية
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; background-color: #f4f7f9; }
    .main-header { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; }
    .stChatMessage { border-radius: 15px; padding: 1rem; margin-bottom: 1rem; direction: rtl !important; }
    .assistant-style { background-color: #ffffff; border-right: 5px solid #1e3c72; color: #1e3c72 !important; padding: 15px; border-radius: 10px; }
    .user-style { background-color: #e3f2fd; border-right: 5px solid #2196f3; color: #0d47a1 !important; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت والبحث عن الموديل (الرادار)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # دالة ذكية كتقلب على الموديل اللي خدام دابا فالسيرفر
    @st.cache_resource
    def find_best_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # كنقلبو على اللي فيه flash هو الأول حيت هو الأسرع
        flash_models = [m for m in models if "flash" in m]
        return flash_models[0] if flash_models else models[0]
    
    WORKING_MODEL = find_best_model()
except Exception as e:
    st.error(f"⚠️ مشكل فـ الربط مع Google: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الواجهة الرئيسية
st.markdown('<div class="main-header"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>الموديل النشط: '+WORKING_MODEL+'</p></div>', unsafe_allow_html=True)

# عرض الحوار
for msg in st.session_state.messages:
    style_class = "user-style" if msg["role"] == "user" else "assistant-style"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{style_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. منطقة الإدخال
uploaded_file = st.sidebar.file_uploader("➕ ارفع صورة التمرين", type=["jpg", "png", "jpeg"])
prompt = st.chat_input("اسأل 'لمعلم' عن أي تمرين...")

# 5. منطق المعالجة
if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
    # التأكد بلي السؤال جديد
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيشوف الحل..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    parts = ["أنت 'لمعلم' خبير تعليمي مغربي. جاوب بالدارجة المغربية بأسلوب مشجع ومبسط جداً."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    answer = response.text
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.markdown(f'<div class="assistant-style">{answer}</div>', unsafe_allow_html=True)
                    st.rerun()
                except Exception as e:
                    st.error(f"وقع مشكل تقني: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

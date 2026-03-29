import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل المغربي (RTL) باش العربية تبدا من اليمين
st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stMarkdown, .stChatMessage { direction: rtl; text-align: right; }
    .teacher-bubble { background-color: #f1f8e9; border-right: 5px solid #4caf50; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط الذكي
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما راكبش فـ Secrets!")
    st.stop()

# 3. دالة البحث عن "الموديل الشغال" (الرادار)
@st.cache_resource
def get_working_model():
    try:
        # كنجبدو كاع الموديلات اللي عندك فالحساب
        available_models = genai.list_models()
        # كنقلبو على اللي كيدعم الصور (Flash هو الأفضل)
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name:
                    return m.name
        # إلا مالقيناش Flash، نخدو أول واحد متاح
        return available_models[0].name
    except:
        return "gemini-1.5-flash" # احتياط

WORKING_MODEL = get_working_model()

# 4. واجهة التطبيق
st.title("👨‍🏫 تطبيق LM3LM")
st.info(f"الموديل النشط حالياً: {WORKING_MODEL}") # هادي غير باش نعرفو شنو خدام

# أدوات التصوير والرفع
col1, col2 = st.columns(2)
with col1: cam_file = st.camera_input("📸 صور")
with col2: upload_file = st.file_uploader("📁 ارفع", type=["jpg", "png", "jpeg"])

audio_file = st.audio_input("🎙️ سجل سؤالك")

if "messages" not in st.session_state: st.session_state.messages = []

# عرض الحوار
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال النص
prompt = st.chat_input("اكتب سؤالك هنا...")

if prompt or cam_file or upload_file or audio_file:
    user_input = prompt if prompt else "شرح ليا هاد التمرين"
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("لمعلم كيشوف الحل..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                content = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية بأسلوب مشجع ومبسط."]
                if prompt: content.append(prompt)
                
                img = Image.open(cam_file if cam_file else upload_file) if (cam_file or upload_file) else None
                if img: content.append(img)
                
                if audio_file:
                    content.append({"mime_type": "audio/wav", "data": audio_file.getvalue()})

                response = model.generate_content(content)
                st.markdown(f'<div class="teacher-bubble">{response.text}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

if st.button("🗑️ مسح"):
    st.session_state.messages = []
    st.rerun()

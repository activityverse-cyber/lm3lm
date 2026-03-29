import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل الاحترافي (Premium UI) - من اليمين لليسر
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f8f9fa; }
    .hero-section { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .bubble { max-width: 85%; padding: 15px; border-radius: 18px; margin-bottom: 10px; line-height: 1.6; display: inline-block; }
    .user-bubble { background-color: #e3f2fd; color: #0d47a1; float: right; border-bottom-right-radius: 4px; border-right: 5px solid #2196f3; }
    .ai-bubble { background-color: white; color: #1e3c72; float: left; border-bottom-left-radius: 4px; border-right: 5px solid #1e3c72; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت وبحث تلقائي عن الموديل (الرادار)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # دالة ذكية كتجبد الموديل اللي خدام دابا فعليا فالسيرفر
    @st.cache_resource
    def get_working_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # كنقلبو على اللي فيه flash حيت هو الأسرع للكوطا المجانية
        flash_models = [m for m in models if "flash" in m]
        return flash_models[0] if flash_models else models[0]
    
    WORKING_MODEL = get_working_model()
except Exception as e:
    st.error(f"⚠️ مشكل فـ الساروت أو الاتصال: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الواجهة
st.markdown(f'<div class="hero-section"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>الموديل النشط: {WORKING_MODEL}</p></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    style = "user-bubble" if msg["role"] == "user" else "ai-bubble"
    st.markdown(f'<div style="width:100%; display:flow-root;"><div class="bubble {style}">{msg["content"]}</div></div>', unsafe_allow_html=True)

# 4. أدوات الإدخال
with st.sidebar:
    st.header("🛠️ الأدوات")
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    if st.button("🗑️ مسح الحوار"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("اسأل 'لمعلم' هنا...")

# 5. منطق المعالجة
if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
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
                    st.rerun()
                except Exception as e:
                    if "404" in str(e):
                        st.error("🚫 هاد الموديل مابقاش خدام فالسيرفر، عاود جرب مورا شوية غايتبدل الموديل بوحدو.")
                    else:
                        st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small>Ibravolt Digital - 2026</small></center>", unsafe_allow_html=True)

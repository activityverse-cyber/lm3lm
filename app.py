import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل "الاحترافي" - إجبار الاتجاه من اليمين لليسر (RTL)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    /* فرض اليمين على الصفحة كاملة */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* تقاد الفقاعات ديال الشات باش يبداو من اليمين */
    .stChatMessage {
        direction: rtl !important;
        text-align: right !important;
    }

    /* لون الخط أزرق غامق باش يبان واضح مع الخلفية */
    p, span, div, label, .stMarkdown {
        color: #1e3c72 !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* ستايل "لمعلم" (الرد) */
    .assistant-style {
        background-color: #ffffff;
        border-right: 5px solid #1e3c72;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: block;
        width: 100%;
    }

    /* ستايل "التلميذ" (السؤال) */
    .user-style {
        background-color: #e3f2fd;
        border-right: 5px solid #2196f3;
        padding: 15px;
        border-radius: 10px;
        display: block;
        width: 100%;
    }

    /* قاد صندوق الكتابة (Input) */
    .stChatInput textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت وبحث تلقائي عن الموديل (الرادار)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def get_working_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash = [m for m in models if "flash" in m]
        return flash[0] if flash else models[0]
    
    WORKING_MODEL = get_working_model()
except Exception as e:
    st.error(f"⚠️ مشكل فـ الساروت: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الواجهة
st.markdown('<h1 style="text-align: center; color: #1e3c72;">👨‍🏫 تطبيق LM3LM - لمعلم</h1>', unsafe_allow_html=True)

# عرض الحوار بستايل اليمين
for msg in st.session_state.messages:
    style = "user-style" if msg["role"] == "user" else "assistant-style"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{style}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. أدوات الإدخال
with st.sidebar:
    st.header("🛠️ الأدوات")
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    if st.button("🗑️ مسح الحوار"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("اسأل 'لمعلم' هنا...")

# 5. منطق المعالجة (بلا تغيير)
if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيشوف الحل..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    # وصية للمعلم باش يحترم اليمين فالهضرة
                    parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية باختصار وبأسلوب مشجع. ابدأ دائماً من اليمين."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    answer = response.text
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small>Ibravolt Digital - 2026</small></center>", unsafe_allow_html=True)

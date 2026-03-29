import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل الاحترافي - إجبار RTL (اليمين لليسار)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    /* فرض الاتجاه من اليمين لليسر على التطبيق كامل */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* تنسيق فقاعات الحوار */
    .stChatMessage {
        direction: rtl !important;
        text-align: right !important;
        margin-left: 0 !important;
        margin-right: auto !important;
    }

    /* لون الخط (أزرق غامق) باش يبان واضح */
    p, span, div, label {
        color: #1e3c72 !important;
    }

    /* تنسيق صندوق الرد (لمعلم) */
    .assistant-bubble {
        background-color: #ffffff;
        border-right: 5px solid #1e3c72;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* تنسيق صندوق السؤال (التلميذ) */
    .user-bubble {
        background-color: #e3f2fd;
        border-right: 5px solid #2196f3;
        padding: 15px;
        border-radius: 10px;
    }

    /* قاد صندوق الكتابة (Input) لتحت */
    .stChatInput textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت والبحث عن الموديل
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def find_working_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash = [m for m in models if "flash" in m]
        return flash[0] if flash else models[0]
    
    WORKING_MODEL = find_working_model()
except Exception as e:
    st.error("⚠️ مشكل فالساروت!")
    st.stop()

# 3. واجهة التطبيق
st.markdown("<h1 style='text-align: center;'>👨‍🏫 تطبيق LM3LM - لمعلم</h1>", unsafe_allow_html=True)
st.write("<center>مساعدك الدراسي الذكي بالدارجة المغربية 🇲🇦</center>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الحوار
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        style = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
        st.markdown(f'<div class="{style}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. منطقة الإدخال
uploaded_file = st.sidebar.file_uploader("➕ ارفع صورة التمرين", type=["jpg", "png", "jpeg"])
prompt = st.chat_input("اسأل 'لمعلم' هنا...")

if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
    # منع التكرار
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيجاوب..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية باختصار وبأسلوب مشجع ومقاد من اليمين."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    st.markdown(f'<div class="assistant-bubble">{response.text}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")

st.sidebar.button("🗑️ مسح الحوار", on_click=lambda: st.session_state.clear())

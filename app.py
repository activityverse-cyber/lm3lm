import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ستايل "الحريفي" - قاد ألوان الخط والخلفية
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    /* فرض الألوان باش ما يبقاش الخط أبيض */
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
        color: #1e3c72 !important; /* لون أزرق غامق للخط */
    }

    .stMarkdown, .stChatMessage, p, li {
        color: #1e3c72 !important;
        direction: rtl;
        text-align: right;
    }

    /* صندوق رد لمعلم - خلفية ملونة وخط واضح */
    .teacher-bubble {
        background-color: #f1f8e9; 
        border-right: 5px solid #4caf50; 
        padding: 20px; 
        border-radius: 15px;
        color: #1b5e20 !important; /* أخضر غامق */
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* صندوق سؤال التلميذ */
    .user-bubble {
        background-color: #e3f2fd;
        border-right: 5px solid #2196f3;
        padding: 15px;
        border-radius: 15px;
        color: #0d47a1 !important; /* أزرق غامق */
        margin-bottom: 20px;
    }

    /* تعديل صندوق الكتابة السفلي */
    .stChatInput textarea {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط الذكي بالساروت
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما راكبش!")
    st.stop()

# الرادار لجلب الموديل الخدام
@st.cache_resource
def get_working_model():
    try:
        available_models = genai.list_models()
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

WORKING_MODEL = get_working_model()

# 3. واجهة التطبيق
st.title("👨‍🏫 تطبيق LM3LM")
st.write("مساعدك الذكي: صور، تكلم، أو اكتب (بالدارجة 🇲🇦)")

# الأدوات
col1, col2 = st.columns(2)
with col1: cam_file = st.camera_input("📸 صور التمرين")
with col2: upload_file = st.file_uploader("📁 ارفع صورة", type=["jpg", "png", "jpeg"])

audio_file = st.audio_input("🎙️ سجل سؤالك بصوتك")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.divider()

# 4. عرض الحوار بالستايل الجديد
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>أنت:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="teacher-bubble"><b>لمعلم:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# 5. معالجة الإدخال
prompt = st.chat_input("اكتب سؤالك هنا...")

if prompt or cam_file or upload_file or audio_file:
    user_input = prompt if prompt else "شرح ليا هادشي"
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("لمعلم كيوجد الرد..."):
        try:
            model = genai.GenerativeModel(WORKING_MODEL)
            parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية بأسلوب مشجع ومبسط جداً."]
            if prompt: parts.append(prompt)
            
            img = Image.open(cam_file if cam_file else upload_file) if (cam_file or upload_file) else None
            if img: parts.append(img)
            
            if audio_file:
                parts.append({"mime_type": "audio/wav", "data": audio_file.getvalue()})

            response = model.generate_content(parts)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun() # باش يتحدث العرض بالألوان الجديدة
            
        except Exception as e:
            st.error(f"مشكل تقني: {e}")

if st.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

st.markdown("<hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

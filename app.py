import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل الاحترافي (RTL 100%)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .stChatMessage { direction: rtl !important; text-align: right !important; }
    p, span, div, label, .stMarkdown { color: #1e3c72 !important; direction: rtl !important; text-align: right !important; }
    .assistant-style { background-color: #ffffff; border-right: 5px solid #1e3c72; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; }
    .user-style { background-color: #e3f2fd; border-right: 5px solid #2196f3; padding: 15px; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط والبحث عن الموديل
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

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# الواجهة
st.markdown('<h1 style="text-align: center;">👨‍🏫 تطبيق LM3LM - لمعلم</h1>', unsafe_allow_html=True)

# عرض الحوار القديم
for msg in st.session_state.messages:
    style = "user-style" if msg["role"] == "user" else "assistant-style"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{style}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. أدوات الإدخال
with st.sidebar:
    st.header("🛠️ الأدوات")
    uploaded_file = st.sidebar.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    if st.sidebar.button("🗑️ مسح الحوار"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("اسأل 'لمعلم' هنا...")

# 5. المنطق: "الديجونكتور" ضد التكرار (The Pro Logic)
if prompt or uploaded_file:
    # تحديد محتوى السؤال الحالي
    current_query = prompt if prompt else "شرح ليا هاد التمرين من الصورة"
    
    # "التستور": كنشوفو واش هاد السؤال فايت جاوبنا عليه فـ آخر رسالة
    is_already_asked = False
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        # إلا كان آخر حاجة هي جواب المعلم، كنشوفو السؤال اللي قبلو
        if len(st.session_state.messages) >= 2:
            if st.session_state.messages[-2]["content"] == current_query:
                is_already_asked = True
    elif st.session_state.messages and st.session_state.messages[-1]["content"] == current_query:
        is_already_asked = True

    # إلا كان السؤال جديد، عاد نخدمو "الماكينة"
    if not is_already_asked:
        st.session_state.messages.append({"role": "user", "content": current_query})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيشوف الحل..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية باختصار وبأسلوب مشجع. ابدأ من اليمين."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun() # تحديث أخير باش نحبسو الـ Loop
                except Exception as e:
                    st.error(f"مشكل تقني: {e}")

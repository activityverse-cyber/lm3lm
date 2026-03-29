import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة والجمالية (CSS Pro)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #f8f9fa;
    }

    /* تصميم فقاعات الحوار */
    .stChatMessage {
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* ستايل مخصص لرد لمعلم */
    .assistant-style {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-right: 5px solid #1e3c72;
    }

    /* ستايل مخصص للتلميذ */
    .user-style {
        background-color: #e3f2fd;
        border-right: 5px solid #2196f3;
    }

    /* تحسين الهيدر */
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* إخفاء العلامات الزائدة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت والذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("⚠️ الساروت ناقص!")
    st.stop()

# 3. القائمة الجانبية (Sidebar) - المعلومات
with st.sidebar:
    st.markdown("### 👨‍🎓 ملف التلميذ")
    st.info(f"📍 المدينة: الجديدة\n\n🔧 الحرفة: Electrician")
    st.divider()
    st.markdown(f"📊 **الأسئلة اليوم:** {len(st.session_state.messages)//2}")
    if st.button("🗑️ مسح سجل المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. الواجهة الرئيسية
st.markdown('<div class="main-header"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>مساعدك الدراسي الذكي بلمسة مغربية</p></div>', unsafe_allow_html=True)

# عرض الرسائل بأسلوب نقي
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        style_class = "user-style" if msg["role"] == "user" else "assistant-style"
        st.markdown(f'<div class="chat-bubble {style_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 5. منطقة الإدخال (الخيوط المجموعة)
with st.container():
    col1, col2 = st.columns([4, 1])
    with col2:
        # زر الرفع والتحميل مجموع فبلاصة وحدة
        uploaded_file = st.file_uploader("➕ صورة", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    with col1:
        prompt = st.chat_input("اسأل 'لمعلم' عن أي تمرين...")

# 6. منطق المعالجة
if prompt or uploaded_file:
    user_content = prompt if prompt else "شرح ليا هاد الصورة"
    
    # منع التكرار
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_content:
        st.session_state.messages.append({"role": "user", "content": user_content})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم يحلل المعطيات..."):
                try:
                    parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة باختصار وذكاء."]
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(parts)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"خطأ: {e}")

st.markdown("---")
st.caption("<center>Ibravolt Digital Solution - 2026</center>", unsafe_allow_html=True)

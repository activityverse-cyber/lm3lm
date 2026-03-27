import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- الإعدادات ---
genai.configure(api_key="AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk") # حط المفتاح ديالك هنا
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- تصميم الواجهة (Custom CSS) ---
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stSelectbox, .stFileUploader {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2193b0, #6dd5ed);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 30px;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .app-title {
        color: #2193b0;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0;
    }
    .app-subtitle {
        color: #7f8c8d;
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True) # هنا كان الخطأ، دابا مصلح

# --- محتوى الصفحة ---
st.markdown('<h1 class="app-title">👨‍🏫 LM3LM</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">المساعد الذكي لتلاميذ الابتدائي والإعدادي 🇲🇦</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    level = st.selectbox("🎯 اختار مستواك:", ["الابتدائي", "الإعدادي"])

with col2:
    if level == "الابتدائي":
        subject = st.selectbox("📚 أشنو المادة؟", ["اللغة العربية", "الرياضيات", "الفرنسية", "النشاط العلمي"])
    else:
        subject = st.selectbox("📚 أشنو المادة؟", ["الرياضيات", "الفيزياء والكيمياء", "اللغات", "علوم الحياة والأرض"])

st.markdown("---")

uploaded_file = st.file_uploader("📸 صور التمرين أو الحل ديالك هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='المعاينة', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم جالس كيشوف فالتمرين... 🧐'):
            try:
                if level == "الابتدائي":
                    instruction = f"أنت 'لمعلم' خبير في {subject} للابتدائي. شرح للطفل بدارجة مغربية مبسطة ومحفزة واستخدم إيموجيات. لا تعط الحل بل وجهه بذكاء."
                else:
                    instruction = f"أنت 'لمعلم' خبير في {subject} للإعدادي. ساعد التلميذ بدارجة مغربية احترافية، ركز على المنهجية العلمية ووجهه لاكتشاف خطئه بنفسه."

                response = model.generate_content([instruction, image])
                
                st.markdown("### 💡 شنو قال ليك لمعلم:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

st.markdown("<br><hr><center><small>تطبيق LM3LM © 2026 - صنع بذكاء لمساعدة تلاميذ المغرب</small></center>", unsafe_allow_html=True)
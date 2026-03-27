import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد المفتاح (API KEY)
# درت ليك هاد الطريقة باش يخدم ليك فالحاسوب وفالسيرفر (GitHub)
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

# الإعداد السحري لتفادي خطأ 404: تحديد الإصدار v1 (المستقر)
genai.configure(api_key=API_KEY, transport='rest') 

# تحديد الموديل (تأكد من كتابة السمية هكا بالظبط)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 2. تصميم الواجهة (Modern & Clean UI)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main { background-color: #f8f9fa; }
    .stButton > button {
        background: linear-gradient(90deg, #2193b0, #6dd5ed);
        color: white;
        border-radius: 25px;
        padding: 12px;
        font-size: 20px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .app-title { color: #2193b0; text-align: center; font-size: 2.5rem; margin-bottom: 0; }
    .app-subtitle { text-align: center; color: #7f8c8d; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. محتوى التطبيق
st.markdown('<h1 class="app-title">👨‍🏫 تطبيق LM3LM (لمعلم)</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">المساعد الدراسي لتلاميذ الابتدائي والإعدادي 🇲🇦</p>', unsafe_allow_html=True)

# اختيار المستوى والمادة في صف واحد
col1, col2 = st.columns(2)
with col1:
    level = st.selectbox("🎯 اختار مستواك:", ["الابتدائي", "الإعدادي"])
with col2:
    if level == "الابتدائي":
        subjects = ["اللغة العربية", "الرياضيات", "الفرنسية", "النشاط العلمي"]
    else:
        subjects = ["الرياضيات", "الفيزياء والكيمياء", "اللغات", "علوم الحياة والأرض"]
    subject = st.selectbox("📚 أشنو المادة؟", subjects)

st.divider()

# منطقة رفع الصورة
uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا (JPG, PNG)...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='المعاينة ديال التمرين', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم جالس كيشوف فالتمرين... 🧐'):
            try:
                # البرومت المخصص
                prompt = f"""
                أنت 'لمعلم' خبير في التعليم المغربي لمستوى {level} مادة {subject}.
                خاطب التلميذ بلهجة مغربية (دارجة) محفزة وودودة.
                لا تعطِ الحل النهائي مباشرة، بل اشرح الطريقة بتبسيط ووجهه لاكتشاف الخطأ إن وجد.
                استعمل إيموجيات تشجيعية.
                """
                
                # إرسال الطلب (هنا فين كتحل المشاكل ديال الإصدار)
                response = model.generate_content([prompt, image])
                
                st.markdown("### 💡 رد لمعلم:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.warning("نصيحة: تأكد من تحديث المكتبة: pip install --upgrade google-generativeai")

st.markdown("<br><hr><center><small>تطبيق LM3LM © 2026 - مشروع Ibravolt الذكي</small></center>", unsafe_allow_html=True)

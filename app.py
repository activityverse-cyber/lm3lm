import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات المفتاح
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

# الحل النهائي: كنحيدو api_version من configure حيت هي اللي دارت TypeError
# وكنعوضوها بـ transport='rest' باش نتفاداو خطأ 404
try:
    genai.configure(api_key=API_KEY, transport='rest')
except Exception:
    genai.configure(api_key=API_KEY)

# تعريف الموديل
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 2. تصميم الواجهة
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.subheader("المساعد الدراسي الذكي 🇲🇦")

# اختيار المستوى والمادة
level = st.selectbox("🎯 المستواك:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء", "اللغات", "النشاط العلمي"])

uploaded_file = st.file_uploader("📸 صور التمرين ديالك...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='المعاينة', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيفكر...'):
            try:
                # التعليمات بدارجة مغربية
                prompt = f"أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين من مستوى {level} مادة {subject} بالدارجة وبلا ما تعطيه الحل نيشان."
                
                # إرسال الطلب
                response = model.generate_content([prompt, image])
                st.info(response.text)
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

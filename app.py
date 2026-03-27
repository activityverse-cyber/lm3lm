import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات المفتاح (API KEY)
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

# الطريقة الأبسط والأضمن لتفادي 404 و TypeError
# كنخليو الإعدادات عادية وكنركزو على تحديث المكتبة فالسيرفر
genai.configure(api_key=API_KEY)

# تعريف الموديل
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 2. تصميم الواجهة (نفس الشكل اللي عجبك)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; border-radius: 20px; width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.subheader("المساعد الدراسي الذكي 🇲🇦")

level = st.selectbox("🎯 المستوى الدراسي:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء والكيمياء", "اللغات", "النشاط العلمي"])

uploaded_file = st.file_uploader("📸 صور التمرين ديالك...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين اللي صورتي', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                # محتوى الطلب (Prompt)
                instruction = f"أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين من مستوى {level} مادة {subject} بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."
                
                # إرسال الطلب (هنا حيدنا كاع التعقيدات اللي دارت TypeError)
                response = model.generate_content([instruction, image])
                
                st.markdown("### 💡 رد لمعلم:")
                st.success(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.info("نصيحة 'لمعلم': تأكد من تحديث ملف requirements.txt لآخر نسخة (0.8.3).")

st.markdown("<hr><center><small>مشروع Ibravolt - الجديدة 2026</small></center>", unsafe_allow_html=True)

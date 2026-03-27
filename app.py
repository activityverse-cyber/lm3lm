import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- الإعدادات ---
# ملاحظة: فـ Streamlit Cloud، غانستعملو st.secrets باش نخبيو المفتاح
try:
    API_KEY = st.secrets["AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"]
except:
    API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

genai.configure(api_key=AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk)

# السطر السحري اللي غايحل مشكل 404:
# كنحددوا الموديل بالسمية الكاملة ديالو فالسيرفر
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# --- تصميم الواجهة ---
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { background: linear-gradient(90deg, #2193b0, #6dd5ed); color: white; border-radius: 30px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.subheader("المساعد الذكي للابتدائي والإعدادي 🇲🇦")

level = st.selectbox("🎯 اختار مستواك:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "النشاط العلمي", "اللغات", "الفيزياء"])

uploaded_file = st.file_uploader("📸 صور التمرين ديالك...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيشوف فالتمرين...'):
            try:
                # محاولة الإرسال مع تحديد الإصدار
                response = model.generate_content([
                    "أنت 'لمعلم' خبير تعليمي مغربي. شرح للتلميذ بدارجة مبسطة ووجهه للخطأ بلا ما تعطيه الحل.", 
                    image
                ])
                st.markdown("### 💡 شنو قال ليك لمعلم:")
                st.info(response.text)
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.warning("نصيحة: تأكد بلي الـ API Key صحيح وبلي درتي update للمكتبة.")

import streamlit as st
import google.generativeai as genai
from PIL import Image
import google.ai.generativelanguage as gl

# 1. إعدادات المفتاح
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

# السطر السحري اللي كيقطع الطريق على v1beta نهائياً:
client_options = {"api_endpoint": "generativelanguage.googleapis.com"}
genai.configure(api_key=API_KEY, transport="rest", client_options=client_options)

# تعريف الموديل مع فرض نسخة v1 فكل طلب
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 2. تصميم الواجهة (نفس الديزاين اللي عجبك)
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

# اختيار المستوى والمادة
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
                instruction = f"أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين (مستوى {level} مادة {subject}) بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."
                
                # إرسال الطلب مع تحديد الـ API Version يدوياً
                response = model.generate_content(
                    [instruction, image],
                    request_options={"timeout": 600, "api_version": "v1"}
                )
                
                st.markdown("### 💡 رد لمعلم:")
                st.success(response.text)
                
            except Exception as e:
                # إذا طاح "ديجونكتور" آخر، غايطلع لينا هنا بالظبط فين كاين
                st.error(f"وقع مشكل تقني: {e}")
                st.info("نصيحة: تأكد من تحديث ملف requirements.txt لآخر نسخة.")

st.markdown("<hr><center><small>مشروع Ibravolt - الجديدة 2026</small></center>", unsafe_allow_html=True)

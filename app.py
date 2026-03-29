import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد المفتاح (API KEY) اللي عطيتيني
API_KEY = "AIzaSyA8xWX9xME_mIu2XccX0h2iNG8Qa-Rr1Pk"
genai.configure(api_key=API_KEY)

# تحديد الموديل (Gemini 1.5 Flash هو اللي كيقرا التصاور بذكاء)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. تصميم الواجهة (UI) لـ تطبيق "لمعلم"
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

# ستايل مغربي خفيف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; border-radius: 20px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.write("المساعد الدراسي الذكي للتلاميذ 🇲🇦 - نسخة 2026")

# الاختيارات (المستوى والمادة)
level = st.selectbox("🎯 المستوى الدراسي:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء والكيمياء", "اللغات", "النشاط العلمي"])

# تحميل صورة التمرين
uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين اللي بغيتي تشرحو', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين ويوجد الشرح...'):
            try:
                # البرومت الاحترافي بالدارجة
                instruction = f"أنت 'لمعلم' خبير تعليمي مغربي. اشرح للتلميذ (مستوى {level} مادة {subject}) هذا التمرين بالدارجة المغربية بأسلوب مشجع ومبسط. لا تعطه الحل النهائي مباشرة، بل وجهه للحل خطوة بخطوة."
                
                # إرسال الطلب لـ Gemini
                response = model.generate_content([instruction, image])
                
                st.markdown("---")
                st.markdown("### 💡 رد لمعلم:")
                st.success(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.info("تأكد بلي الـ API Key مفعل فيه Gemini 1.5 Flash فـ Google AI Studio.")

st.markdown("<br><hr><center><small>مشروع LM3LM - الجديدة 2026</small></center>", unsafe_allow_html=True)

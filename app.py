import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الوصول (The Credentials)
# هادا هو المفتاح اللي عطيتيني "يا لمعلم"
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

# السطر السحري اللي كيحيد مشكل 404 فـ 2026:
# كنحددوا api_version="v1" باش نهربوا من النسخة التجريبية (v1beta) اللي فيها المشكل
genai.configure(api_key=API_KEY, api_version="v1", transport="rest")

# تعريف الموديل
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 2. تصميم الواجهة (Custom Styling)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .main { background-color: #f0f2f6; }
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 20px;
        padding: 15px;
        font-size: 22px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .app-title { color: #1e3c72; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. محتوى الصفحة الرئيسي
st.markdown('<h1 class="app-title">👨‍🏫 تطبيق LM3LM (لمعلم)</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #555;">مساعدك الذكي في تمارين الابتدائي والإعدادي 🇲🇦</p>', unsafe_allow_html=True)

st.divider()

# اختيارات المستوى والمادة
col1, col2 = st.columns(2)
with col1:
    level = st.selectbox("🎯 مستواك الدراسي:", ["الابتدائي", "الإعدادي"])
with col2:
    if level == "الابتدائي":
        subjects = ["اللغة العربية", "الرياضيات", "الفرنسية", "النشاط العلمي"]
    else:
        subjects = ["الرياضيات", "الفيزياء والكيمياء", "علوم الحياة والأرض", "اللغات"]
    subject = st.selectbox("📚 المادة:", subjects)

# رفع الصورة من طرف التلميذ
uploaded_file = st.file_uploader("📸 صور التمرين أو الحل وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # عرض الصورة للمعاينة
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة اللي رفعتي', use_container_width=True)

    # زر التحليل
    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين وكيحلل... 🧐'):
            try:
                # تعليمات 'لمعلم' بالدارجة
                prompt = f"""
                أنت 'لمعلم' خبير تعليمي مغربي لمستوى {level} في مادة {subject}.
                1. تكلم بالدارجة المغربية بأسلوب مشجع وحنين (مثل المعلمين المغاربة القدماء).
                2. لا تعط الجواب مباشرة، اشرح الطريقة بتبسيط.
                3. إذا وجد خطأ، قل 'أجي نعاودو نفكرو فهاد السطر' وشرح ليه علاش.
                4. استخدم إيموجيات مغربية محفزة.
                """
                
                # إرسال الصورة والتعليمات
                response = model.generate_content([prompt, image])
                
                # عرض النتيجة
                st.markdown("### 💡 رد لمعلم:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.warning("نصيحة 'لمعلم': تأكد بلي درتي Reboot للتطبيق فـ Streamlit Cloud.")

st.markdown("<br><hr><center><small>تطبيق LM3LM © 2026 - مشروع Ibravolt المبتكر</small></center>", unsafe_allow_html=True)

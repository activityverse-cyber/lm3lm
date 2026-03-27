import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد المفتاح (API KEY) اللي عطيتيني
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"
genai.configure(api_key=API_KEY)

# هاد السطر كيحدد أننا بغينا النسخة المستقرة v1
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 3. تصميم واجهة "لمعلم" (Professional UI)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stButton > button {
        background: linear-gradient(90deg, #2193b0, #6dd5ed);
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 18px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .app-header {
        text-align: center;
        color: #2193b0;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. محتوى الصفحة
st.markdown('<h1 class="app-header">👨‍🏫 تطبيق LM3LM (لمعلم)</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #7f8c8d;">المساعد الدراسي الذكي للابتدائي والإعدادي 🇲🇦</p>', unsafe_allow_html=True)

st.divider()

# اختيار المستوى والمادة
col1, col2 = st.columns(2)
with col1:
    level = st.selectbox("🎯 المستوى الدراسي:", ["الابتدائي", "الإعدادي"])
with col2:
    if level == "الابتدائي":
        subject = st.selectbox("📚 المادة:", ["اللغة العربية", "الرياضيات", "الفرنسية", "النشاط العلمي"])
    else:
        subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء والكيمياء", "اللغات", "علوم الحياة والأرض"])

# رفع الصورة
uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هاد التمرين"):
        with st.spinner('لمعلم كيقرا التمرين بالخاطر... 🧐'):
            try:
                # التعليمات المخصصة للمعلم (System Instructions)
                prompt = f"""
                أنت 'لمعلم' خبير في التعليم المغربي. التلميذ في مستوى {level} ويحتاج مساعدة في {subject}.
                1. تكلم بالدارجة المغربية بأسلوب مشجع وحنين.
                2. لا تعط الجواب النهائي مباشرة.
                3. اشرح الخطوات بتبسيط (مثلاً للابتدائي استعمل أمثلة من الواقع).
                4. إذا كان هناك خطأ في الحل، نبه التلميذ بذكاء وقل له 'أجي نفكرو فهادي'.
                """
                
                # إرسال الصورة والطلب لـ Gemini
                response = model.generate_content([prompt, image])
                
                st.markdown("### 💡 رد لمعلم:")
                st.success(response.text)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")
                st.info("نصيحة: تأكد بلي درتي pip install --upgrade google-generativeai في الـ Terminal.")

st.markdown("<br><hr><center><small>حقوق النشر © 2026 - مشروع LM3LM لمساعدة تلاميذ المغرب</small></center>", unsafe_allow_html=True)

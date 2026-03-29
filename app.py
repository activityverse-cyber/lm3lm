import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الصفحة والستايل (CSS) باش نقادو العربية
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stMarkdown, .stText, .stAlert {
        direction: rtl;
        text-align: right;
    }

    /* ستايل خاص لرد لمعلم */
    .answer-box {
        background-color: #f0f7ff;
        border-right: 5px solid #2a5298;
        padding: 20px;
        border-radius: 10px;
        color: #1e3c72;
        font-weight: 500;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط مع الساروت
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما كاينش فـ Secrets!")
    st.stop()

# 3. واجهة المستخدم
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.write("مساعدك الدراسي الذكي بالدارجة المغربية 🇲🇦")

uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                # البحث عن الموديل في الخلفية بلا ما نبينوه
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if "flash" in m or "vision" in m), None)
                
                if target_model:
                    model = genai.GenerativeModel(target_model)
                    # البرومت معدل باش يجاوب بعربية/دارجة مقادة
                    response = model.generate_content([
                        "أنت 'لمعلم' خبير تعليمي مغربي. اشرح هذا التمرين للتلميذ بالدارجة المغربية بأسلوب مشجع. لا تعطِ الحل النهائي مباشرة، بل وجهه للحل خطوة بخطوة.", 
                        image
                    ])
                    
                    st.markdown("---")
                    st.markdown("### 💡 رد لمعلم:")
                    # عرض النتيجة وسط "بوكس" مقاد
                    st.markdown(f'<div class="answer-box">{response.text}</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ عذراً، كاين مشكل فالسيرفر حالياً.")

            except Exception as e:
                st.error(f"وقع مشكل: {e}")

st.markdown("<br><hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

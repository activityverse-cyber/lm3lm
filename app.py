import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الصفحة والستايل (CSS)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stMarkdown, .stText, .stAlert { direction: rtl; text-align: right; }
    .answer-box {
        background-color: #f0f7ff;
        border-right: 5px solid #2a5298;
        padding: 20px;
        border-radius: 10px;
        color: #1e3c72;
        line-height: 1.6;
    }
    /* ستايل لبوتون الكاميرا */
    .stCameraInput > label { font-weight: bold; color: #2a5298; }
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
st.write("صور تمرينك و 'لمعلم' يشرح ليك بالدارجة 🇲🇦")

# ديرو جوج طرق: كاميرا ولا رفع ملف
tab1, tab2 = st.tabs(["📸 صور دابا", "📁 جبد من التيليفون"])

img_to_process = None

with tab1:
    # هادي هي "الأيقونة" والخاصية اللي طلبتي د الكاميرا
    cam_image = st.camera_input("وجه الكاميرا للتمرين وصور")
    if cam_image:
        img_to_process = Image.open(cam_image)

with tab2:
    file_image = st.file_uploader("اختار صورة من الغاليري", type=["jpg", "png", "jpeg"])
    if file_image:
        img_to_process = Image.open(file_image)

# 4. المعالجة والرد
if img_to_process:
    st.image(img_to_process, caption='الصورة اللي غانشرحو', use_container_width=True)

    if st.button("يا لمعلم، شرح ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if "flash" in m or "vision" in m), None)
                
                if target_model:
                    model = genai.GenerativeModel(target_model)
                    response = model.generate_content([
                        "أنت 'لمعلم' خبير تعليمي مغربي. اشرح هذا التمرين للتلميذ بالدارجة المغربية بأسلوب مشجع ومبسط. لا تعطِ الحل النهائي مباشرة، بل وجهه للحل خطوة بخطوة.", 
                        img_to_process
                    ])
                    
                    st.markdown("---")
                    st.markdown("### 💡 رد لمعلم:")
                    st.markdown(f'<div class="answer-box">{response.text}</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ عذراً، كاين مشكل فالسيرفر.")
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

st.markdown("<br><hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

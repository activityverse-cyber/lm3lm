import streamlit as st
import requests
from PIL import Image
import io
import base64

# 1. الإعدادات
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# وظيفة لتحويل الصورة لـ Base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 2. واجهة التطبيق
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.write("المساعد الدراسي الذكي - نسخة 2026 🇲🇦")

level = st.selectbox("🎯 المستوى:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء", "اللغات", "النشاط العلمي"])

uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption='التمرين المرفوع', use_container_width=True)
    
    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                # تجهيز البيانات للإرسال "Direct"
                image_base64 = encode_image(uploaded_file)
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": f"أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين من مستوى {level} مادة {subject} بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                        ]
                    }]
                }
                
                # إرسال الطلب مباشرة لـ Google API v1
                response = requests.post(URL, json=payload)
                result = response.json()
                
                # إظهار الجواب
                if "candidates" in result:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 💡 رد لمعلم:")
                    st.info(answer)
                else:
                    st.error(f"خطأ من Google: {result}")
                    
            except Exception as e:
                st.error(f"مشكل فالاتصال: {e}")

st.markdown("<hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

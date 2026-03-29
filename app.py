import streamlit as st
import requests
import base64

# الإعدادات الأساسية
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"
# هاد الرابط هو "الساروت" الصحيح لعام 2026
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="LM3LM", layout="centered")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.write("مساعد دراسي للتلاميذ 🇲🇦")

# اختيار المادة والمستوى
level = st.selectbox("🎯 المستوى:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء", "اللغات", "النشاط العلمي"])

uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)
    
    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('جاري التحليل...'):
            try:
                # تحويل الصورة لـ Base64
                img_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
                
                # بناء الطلب (Payload)
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": f"أنت 'لمعلم' خبير تعليمي. شرح للتلميذ هاد التمرين من مستوى {level} مادة {subject} بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                        ]
                    }]
                }
                
                # إرسال الطلب
                response = requests.post(URL, json=payload)
                result = response.json()
                
                if "candidates" in result:
                    st.info(result['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"خطأ من السيرفر: {result}")
                    
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

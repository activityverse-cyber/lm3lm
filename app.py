import streamlit as st
import requests
import base64
from PIL import Image

# 1. الإعدادات التقنية
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"
# الرابط الصحيح والمباشر للموديل فـ 2026
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 2. واجهة التطبيق "لمعلم"
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; border-radius: 20px; width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

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
                image_base64 = encode_image(uploaded_file)
                
                # هيكل البيانات الصحيح (v1 structure)
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": f"أنت 'لمعلم' خبير تعليمي مغربي. التلميذ في مستوى {level} مادة {subject}. شرح له التمرين بالدارجة المغربية بأسلوب مشجع ولا تعطه الحل مباشرة."},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg", 
                                    "data": image_base64
                                }
                            }
                        ]
                    }]
                }
                
                # إرسال الطلب
                response = requests.post(URL, json=payload)
                result = response.json()
                
                # معالجة الرد
                if "candidates" in result:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 💡 رد لمعلم:")
                    st.info(answer)
                else:
                    st.error(f"مشكل من السيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                    st.warning("جرب ترفع صورة أصغر أو تأكد من الـ API Key.")
                    
            except Exception as e:
                st.error(f"مشكل فالاتصال: {e}")

st.markdown("<hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

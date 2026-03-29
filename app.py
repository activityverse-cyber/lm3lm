import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. إعداد الواجهة
st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

# 2. جلب الساروت من الخزنة (Secrets)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # الرابط المباشر لنسخة v1 الرسمية
    URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
except:
    st.error("⚠️ الساروت (API Key) ما كاينش فـ Secrets! تأكد من GOOGLE_API_KEY")
    st.stop()

# دالة لتحويل الصورة لـ Base64
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# 3. واجهة المستخدم
uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption='التمرين المرفوع', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                # تجهيز البيانات
                image_base64 = encode_image(uploaded_file)
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                        ]
                    }]
                }
                
                # إرسال الطلب مباشرة (v1)
                response = requests.post(URL, json=payload)
                result = response.json()
                
                if "candidates" in result:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 💡 رد لمعلم:")
                    st.info(answer)
                else:
                    st.error(f"مشكل من السيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                    
            except Exception as e:
                st.error(f"وقع مشكل فالاتصال: {e}")

st.markdown("<hr><center><small>مشروع LM3LM - الجديدة 2026</small></center>", unsafe_allow_html=True)

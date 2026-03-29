import streamlit as st
import requests
import base64
from PIL import Image

# 1. إعداد الواجهة
st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

# 2. جلب المفتاح
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ الساروت (API Key) ما كاينش فـ Secrets!")
    st.stop()

# دالة الإرسال "الجذرية"
def call_gemini(model_name, img_base64):
    # استعملنا v1beta حيت هي اللي كتقبل الموديلات القديمة والجديدة بجوج
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": "أنت 'لمعلم' خبير تعليمي مغربي. شرح هاد التمرين بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
            ]
        }]
    }
    return requests.post(url, json=payload)

# 3. واجهة المستخدم
uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا...'):
            try:
                img_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                
                # الخطة الجذرية: جرب الموديلات واحد بواحد حتى يخدم شي خيط
                models_to_test = ["gemini-1.5-flash", "gemini-pro-vision", "gemini-1.5-pro"]
                
                success = False
                for model in models_to_test:
                    response = call_gemini(model, img_data)
                    result = response.json()
                    
                    if "candidates" in result:
                        answer = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(f"### 💡 رد لمعلم (بواسطة {model}):")
                        st.success(answer)
                        success = True
                        break # لقينا الخيط الخدام، حبس!
                
                if not success:
                    st.error("حتى موديل ما بغا يخدم. هادشي كيعني أن الـ API Key محتاج 'تفعيل' يدوي فـ Google AI Studio.")
                    st.json(result) # باش نشوفو أخر خطأ طلع
                    
            except Exception as e:
                st.error(f"وقع مشكل فالاتصال: {e}")

st.markdown("<hr><center><small>Ibravolt - الجديدة 2026</small></center>", unsafe_allow_html=True)

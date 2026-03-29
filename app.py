import streamlit as st
import requests
import base64

# 1. الإعدادات
API_KEY = "AIzaSyB4KsUP8EVImF8dhkFs2Bcln6e206o7nHk"

def get_response(model_name, img_data, level, subject):
    # جربنا v1 و v1beta، دابا غانخدمو بـ v1 اللي هي الرسمية فـ 2026
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": f"أنت 'لمعلم' خبير تعليمي مغربي. اشرح للتلميذ هذا التمرين (مستوى {level} مادة {subject}) بالدارجة المغربية بأسلوب مشجع ولا تعطه الحل مباشرة."},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
            ]
        }]
    }
    return requests.post(url, json=payload)

st.set_page_config(page_title="LM3LM", layout="centered")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

level = st.selectbox("🎯 المستوى:", ["الابتدائي", "الإعدادي"])
subject = st.selectbox("📚 المادة:", ["الرياضيات", "الفيزياء", "اللغات", "النشاط العلمي"])

uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)
    
    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('جاري محاولة الاتصال بالسيرفر...'):
            try:
                img_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
                
                # المحاولة الأولى بـ gemini-1.5-flash
                res = get_response("gemini-1.5-flash", img_data, level, subject)
                
                # إلا عطى 404، جرب النسخة الاحتياطية gemini-pro-vision
                if res.status_code == 404:
                    res = get_response("gemini-pro-vision", img_data, level, subject)
                
                result = res.json()
                
                if "candidates" in result:
                    st.success(result['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"مشكل فالسيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                    st.info("نصيحة: تأكد من تفعيل الموديل في Google AI Studio.")
                    
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")

st.markdown("<hr><center>LM3LM Project - 2026</center>", unsafe_allow_html=True)

import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. إعدادات الساروت
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("⚠️ الساروت (HF_TOKEN) ما كاينش فـ Secrets!")
    st.stop()

# موديل Microsoft Florence-2 (خفيف وكيخدم دغيا)
API_URL = "https://router.huggingface.co/hf-inference/models/microsoft/Florence-2-large"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا...'):
            try:
                # تجهيز الصورة
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_data = img_byte_arr.getvalue()

                # إرسال الطلب (Data Binary مباشرة)
                response = requests.post(API_URL, headers=headers, data=img_data)
                
                # فحص الرد قبل القراءة (باش ما يطلعش خطأ char 0)
                if response.status_code == 200:
                    result = response.json()
                    st.success("💡 رد لمعلم:")
                    # الموديل كيعطي وصف دقيق للتمرين
                    if isinstance(result, list):
                        st.write(result[0].get('generated_text', 'ما كاينش نص'))
                    else:
                        st.write(result.get('generated_text', 'ما كاينش نص'))
                elif response.status_code == 503:
                    st.warning("⚠️ السيرفر كيوجد (Loading).. عاود ورك مورا 20 ثانية.")
                else:
                    st.error(f"خطأ من السيرفر ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"مشكل فـ الكود: {e}")

st.markdown("<hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

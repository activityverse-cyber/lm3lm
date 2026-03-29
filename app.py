import streamlit as st
import google.generativeai as genai
from PIL import Image

# جلب المفتاح من Secrets
try:
    API_KEY = st.secrets["AIzaSyCCSrhV1UkH-hppIBijV_4r3LUGKVsyIxo"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash") # جرب 1.5 حيت هي المستقرة
except Exception as e:
    st.error("الساروت (API Key) ما راكبش مزيان فـ Secrets!")

st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا...'):
            try:
                response = model.generate_content([
                    "أنت 'لمعلم' خبير مغربي. شرح هاد التمرين بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان.", 
                    image
                ])
                st.success(response.text)
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

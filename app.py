import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الواجهة
st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

# 2. الربط مع Google (الساروت اللي فـ Secrets)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما كاينش فـ Secrets!")
    st.stop()

# 3. واجهة المستخدم
uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيشوف شنو الموديل اللي مسموح ليه يخدم بيه...'):
            try:
                # هاد السطر هو "التستور" اللي غايقول لينا شنو اللي خدام عندك
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # غانقلبو على أول واحد فيه كلمة "flash" أو "vision"
                target_model = None
                for m in available_models:
                    if "flash" in m or "vision" in m:
                        target_model = m
                        break
                
                if target_model:
                    model = genai.GenerativeModel(target_model)
                    response = model.generate_content(["شرح هاد التمرين بالدارجة المغربية بأسلوب مبسط.", image])
                    st.success(f"💡 رد لمعلم (باستعمال {target_model}):")
                    st.write(response.text)
                else:
                    st.error("❌ مالقينا حتى موديل كيقرا التصاور فالحساب ديالك. جرب Gmail آخر.")
                    st.write("الموديلات اللي عندك هما:", available_models)

            except Exception as e:
                st.error(f"وقع مشكل: {e}")

st.markdown("<hr><center><small>Ibravolt - 2026</small></center>", unsafe_allow_html=True)

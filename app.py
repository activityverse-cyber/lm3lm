import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد المفتاح (API KEY) اللي عطيتيني
API_KEY = "AIzaSyA8xWX9xME_mIu2XccX0h2iNG8Qa-Rr1Pk"
genai.configure(api_key=API_KEY)

# 2. دالة ذكية لاختيار الموديل المتاح
def get_available_model():
    # غانحاولوا بـ 2.5 هي الأولى حيت هي اللي شفتي عندك
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-pro-vision"]
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(m_name)
            # تجربة خفيفة باش نشوفو واش الموديل موجود
            return model, m_name
        except:
            continue
    return None, None

model, active_model_name = get_available_model()

# 3. واجهة التطبيق
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

if active_model_name:
    st.sidebar.success(f"الموديل الخدام دابا: {active_model_name}")
else:
    st.error("السيرفر مالقى حتى موديل خدام فالحساب ديالك!")

uploaded_file = st.file_uploader("📸 صور التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file and model:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا...'):
            try:
                instruction = "أنت 'لمعلم' خبير مغربي. شرح هاد التمرين بالدارجة المغربية بأسلوب مشجع."
                response = model.generate_content([instruction, image])
                st.success(response.text)
            except Exception as e:
                st.error(f"خطأ تقني: {e}")

import streamlit as st
import requests
from PIL import Image
import io

# 1. إعدادات الساروت الجديد (HF_TOKEN)
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("⚠️ الساروت (HF_TOKEN) ما كاينش فـ Secrets ديال Streamlit!")
    st.stop()

# رابط الموديل (Moondream - متخصص ففهم الصور)
API_URL = "https://api-inference.huggingface.co/models/vikhyatk/moondream2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")
st.write("نسخة Hugging Face الاحترافية 🇲🇦")

uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين...'):
            try:
                # تحويل الصورة لـ Base64 باش يصيفطها للسيرفر
                import base64
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                # إرسال السؤال للموديل
                # طلبنا منو يوصف التمرين ويشرحو
                output = query({
                    "inputs": {
                        "image": img_str,
                        "text": "Explain this educational exercise and provide a hint to solve it in Moroccan Darija Arabic if possible."
                    }
                })

                st.markdown("---")
                st.markdown("### 💡 رد لمعلم:")
                if 'generated_text' in output:
                    st.success(output['generated_text'])
                else:
                    st.info(output) # فاش كيكون الموديل كيسخن (Loading)
            
            except Exception as e:
                st.error(f"وقع مشكل فالسيرفر: {e}")

st.markdown("<br><hr><center><small>مشروع LM3LM - الجديدة 2026</small></center>", unsafe_allow_html=True)

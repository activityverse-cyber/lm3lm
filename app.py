import streamlit as st
import requests
from PIL import Image
import io
import base64

# 1. إعدادات الساروت (HF_TOKEN) من Secrets
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("⚠️ الساروت (HF_TOKEN) ما كاينش فـ Secrets!")
    st.stop()

# العنوان الجديد (الروتر) اللي طلبو منك Hugging Face
# استعملنا موديل Qwen2-VL حيت واعر بزاف فـ 2026 وكيقرا العربية
API_URL = "https://router.huggingface.co/hf-inference/models/Qwen/Qwen2-VL-7B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        with st.spinner('لمعلم كيقرا التمرين من الروتر الجديد...'):
            try:
                # تحويل الصورة لـ Base64
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                # بناء الطلب للموديل الجديد (Qwen2-VL)
                payload = {
                    "inputs": f"<html><img src='data:image/jpeg;base64,{img_str}'></html>\nشرح هاد التمرين بالدارجة المغربية بأسلوب مبسط للتلميذ.",
                    "parameters": {"max_new_tokens": 500}
                }

                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()

                st.markdown("---")
                st.markdown("### 💡 رد لمعلم:")
                
                # التعامل مع ردود السيرفر (إما نص مباشر أو قائمة)
                if isinstance(result, list) and 'generated_text' in result[0]:
                    st.success(result[0]['generated_text'])
                elif 'generated_text' in result:
                    st.success(result['generated_text'])
                else:
                    # إلا كان الموديل عاد كيتشارجا (Loading)
                    if 'estimated_time' in result:
                        st.warning(f"السيرفر كيوجد.. عاود ورك على البوتون مورا {int(result['estimated_time'])} ثانية.")
                    else:
                        st.error(f"خطأ غير متوقع: {result}")
            
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")

st.markdown("<hr><center><small>Ibravolt - El Jadida 2026</small></center>", unsafe_allow_html=True)

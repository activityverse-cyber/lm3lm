import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الواجهة (ديما هي الأولى)
st.set_page_config(page_title="LM3LM", page_icon="👨‍🏫")
st.title("👨‍🏫 تطبيق LM3LM (لمعلم)")

# 2. "توصيل الضو" (الـ API Key والموديل)
# غانعرفو الموديل خارج الـ try باش يكون "Global"
model = None

try:
    # جلب المفتاح من Secrets (الخزنة المستورة)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # تعريف الموديل (استعملنا 1.5 حيت هي اللي كتقرا التصاور مزيان)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("⚠️ الساروت (API Key) ما راكبش مزيان فـ Secrets! تأكد بلي سميتو GOOGLE_API_KEY")
    st.info("نصيحة: دخل لـ Settings -> Secrets فـ Streamlit Cloud وحط الساروت تما.")

# 3. واجهة المستخدم
uploaded_file = st.file_uploader("📸 صور التمرين وحطو هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)

    if st.button("يا لمعلم، شوف ليا هادشي"):
        # تأكدنا بلي الموديل "Defined" وخدام
        if model is not None:
            with st.spinner('لمعلم كيقرا التمرين...'):
                try:
                    # الطلب بدارجة مغربية
                    instruction = "أنت 'لمعلم' خبير مغربي. شرح للتلميذ هاد التمرين بالدارجة المغربية بأسلوب مشجع وبلا ما تعطيه الحل نيشان."
                    
                    response = model.generate_content([instruction, image])
                    
                    st.markdown("### 💡 رد لمعلم:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"وقع مشكل تقني فاش لمعلم بغا يجاوب: {e}")
        else:
            st.warning("⚠️ ما يمكنش نجاوب حيت الموديل ما خدامش. شوف الميساج ديال الخطأ الفوق.")

st.markdown("<hr><center><small>مشروع LM3LM - الجديدة 2026</small></center>", unsafe_allow_html=True)

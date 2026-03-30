import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الواجهة (Advanced UI/UX)
st.set_page_config(page_title="أستاذ - Oustad Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&family=Inter:wght@400;600&display=swap');
    
    /* الأساسيات */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', 'Inter', sans-serif !important;
        background-color: #fcfdfe;
    }

    /* هيدر احترافي */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 3rem;
        border-radius: 0 0 50px 50px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* تحكم تلقائي في اتجاه النص (Auto-Direction) */
    .chat-bubble {
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        line-height: 1.8;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        /* هاد الخاصية كتقاد اليمين واليسار بوحدها */
        unicode-bidi: plaintext;
        text-align: start; 
    }

    .user-style {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        color: #2d3436;
        margin-left: 20%; /* دفع الرسالة لليسر */
    }

    .ai-style {
        background-color: #eef5ff;
        border-right: 6px solid #1a73e8;
        color: #1e3c72;
        margin-right: 10%; /* دفع الرسالة لليمين */
    }

    /* ستايل خاص للصور والملفات */
    .stFileUploader {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #1a73e8;
    }

    /* إخفاء الزوائد */
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الذاكرة والموديل (بدون 404)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def load_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        best = [m for m in models if "flash" in m]
        return best[0] if best else models[0]
    
    WORKING_MODEL = load_model()
except:
    st.error("⚠️ تأكد من إعداد API Key في Secrets")
    st.stop()

# 3. واجهة أستاذ
st.markdown('<div class="main-header"><h1>👨‍🏫 أستاذ (Oustad Pro)</h1><p>منصة الشرح الذكي - تفاعل، تعلم، وتفوق</p></div>', unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=100)
    st.title("إعدادات الدرس")
    subject = st.selectbox("المادة الحالية:", ["الرياضيات", "الفيزياء", "الكيمياء", "علوم الحياة", "اللغات"])
    uploaded_file = st.file_uploader("📸 صور التمرين أو الدرس", type=["jpg", "png", "jpeg"])
    if st.button("🔄 حوار جديد"):
        st.session_state.chat_history = []
        st.rerun()

# 4. عرض الشات
for chat in st.session_state.chat_history:
    bubble_class = "user-style" if chat["role"] == "user" else "ai-style"
    with st.container():
        st.markdown(f'<div class="chat-bubble {bubble_class}">{chat["content"]}</div>', unsafe_allow_html=True)

# 5. منطقة التفاعل
user_input = st.chat_input("تواصل مع أستاذ هنا...")

if user_input or uploaded_file:
    # تحديد النص للعرض
    display_text = user_input if user_input else "ممكن تشرح ليا هاد الصورة؟"
    
    # منع التكرار
    if not st.session_state.chat_history or st.session_state.chat_history[-1]["content"] != display_text:
        st.session_state.chat_history.append({"role": "user", "content": display_text})
        
        with st.chat_message("assistant"):
            with st.spinner("أستاذ كيكتب ليك الشرح..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    
                    # سياق أستاذ (الذكاء البيداغوجي)
                    instruction = f"""أنت 'أستاذ' مغربي خبير. 
                    - المادة: {subject}.
                    - اللغة: جاوب بالدارجة المغربية بأسلوب تربوي مبسط.
                    - التنسيق: إذا كتبت بالعربية ابدأ من اليمين، وإذا كتبت معادلات أو فرنسية اتركها تظهر من اليسار.
                    - المهمة: اشرح المفهوم بذكاء، استعمل أمثلة من الواقع، ولا تعطي الحلول الجاهزة فقط."""
                    
                    # بناء محتوى الطلب
                    parts = [instruction]
                    # إضافة سياق المحادثة (الذاكرة)
                    for m in st.session_state.chat_history[-6:]:
                        parts.append(f"{m['role']}: {m['content']}")
                    
                    if uploaded_file:
                        parts.append(Image.open(uploaded_file))
                    if user_input:
                        parts.append(user_input)

                    response = model.generate_content(parts)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    st.rerun()

                except Exception as e:
                    st.error(f"عذراً، وقع مشكل تقني: {e}")

st.markdown("<hr><center><p style='color: #a0aec0;'>منصة أستاذ - ذكاء تعليمي مغربي 2026</p></center>", unsafe_allow_html=True)

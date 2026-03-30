import streamlit as st
import google.generativeai as genai
from PIL import Image
import hashlib

# 1. إعداد الواجهة الاحترافية (Minimalist & Pro UI)
st.set_page_config(page_title="أستاذ - Oustad", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #ffffff;
        color: #000000 !important;
    }

    /* هيدر الأداة */
    .main-header {
        text-align: center;
        padding: 40px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 30px;
    }
    .main-header h1 { color: #1a73e8; font-size: 2.5rem; }

    /* صناديق الرسائل (Chat Bubbles) */
    .message-container {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        max-width: 85%;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    .user-msg { background-color: #f8f9fa; border: 1px solid #eee; float: right; color: #3c4043 !important; }
    .ai-msg { background-color: #e8f0fe; border-right: 5px solid #1a73e8; float: left; color: #1967d2 !important; }

    /* إخفاء واجهة ستريمليت الزايدة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد "أستاذ" (الرادار الأوتوماتيكي للخدمة)
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # كنقلبو على أحسن موديل متاح بلا ما نكتبو سميتو (ضد الـ 404)
    @st.cache_resource
    def get_best_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash_models = [m for m in models if "flash" in m]
        return flash_models[0] if flash_models else models[0]
    
    WORKING_MODEL = get_best_model()
except Exception as e:
    st.error("⚠️ مشكل فـ الساروت (API Key)!")
    st.stop()

# 3. واجهة "أستاذ" الرئيسية
st.markdown('<div class="main-header"><h1>👨‍🏫 أستاذ (Oustad)</h1><p>شرح مبسط، تفاعلي، وذكي لكل التمارين</p></div>', unsafe_allow_html=True)

# القائمة الجانبية (الأدوات)
with st.sidebar:
    st.markdown("### 📚 أدوات الأستاذ")
    subject = st.selectbox("اختر المادة:", ["رياضيات", "فيزياء", "كيمياء", "علوم الحياة والأرض", "أخرى"])
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين هنا", type=["jpg", "png", "jpeg"])
    if st.button("🗑️ مسح الحوار وابدأ من جديد"):
        st.session_state.messages = []
        st.rerun()

# 4. منطقة الحوار (Chat Display)
for msg in st.session_state.messages:
    style = "user-msg" if msg["role"] == "user" else "ai-msg"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="message-container {style}">{msg["content"]}</div>', unsafe_allow_html=True)

# 5. منطق التعامل مع الأسئلة (Chat & Scan)
prompt = st.chat_input("اسأل أستاذ عن أي حاجة فـ التمرين...")

if prompt or uploaded_file:
    # تحديد محتوى الإدخال
    user_content = prompt if prompt else "ممكن تشرح ليا هاد التمرين اللي فـ الصورة؟"
    
    # منع التكرار
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_content:
        st.session_state.messages.append({"role": "user", "content": user_content})
        
        with st.chat_message("assistant"):
            with st.spinner("أستاذ كيشوف فـ المعطيات..."):
                try:
                    model = genai.GenerativeModel(WORKING_MODEL)
                    
                    # صياغة السياق (أستاذ كيشرح وماشي غير كيعطي الحل)
                    context = f"""أنت 'أستاذ' خبير تعليمي مغربي. هدفك هو مساعدة التلميذ على فهم المادة ({subject}).
                    - اشرح الخطوات بالدارجة المغربية بأسلوب تربوي، سهل ومبسط.
                    - لا تعطي الحل النهائي مباشرة، بل اشرح 'لماذا' وكيف وصلنا للنتيجة.
                    - تفاعل مع التلميذ كأستاذ حقيقي في القسم.
                    - اكتب دائماً من اليمين إلى اليسار وبخط واضح."""
                    
                    parts = [context]
                    
                    # إذا كان هناك حوار سابق، نزود الموديل بيه (Chat Memory)
                    for m in st.session_state.messages[-5:]: # آخر 5 رسائل للحفاظ على الكوطا
                        parts.append(f"{m['role']}: {m['content']}")
                    
                    if uploaded_file:
                        parts.append(Image.open(uploaded_file))
                    
                    if prompt:
                        parts.append(prompt)

                    response = model.generate_content(parts)
                    answer = response.text
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"وقع مشكل تقني: {e}")

st.markdown("<br><center><small>منصة أستاذ التعليمية - 2026</small></center>", unsafe_allow_html=True)

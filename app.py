import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل (RTL) والألوان الواضحة
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; color: #1e3c72 !important; }
    .stMarkdown, .stChatMessage, p { direction: rtl; text-align: right; color: #1e3c72 !important; }
    .teacher-bubble { background-color: #f1f8e9; border-right: 5px solid #4caf50; padding: 15px; border-radius: 10px; color: #1b5e20 !important; margin-bottom: 10px; }
    .user-bubble { background-color: #e3f2fd; border-right: 5px solid #2196f3; padding: 15px; border-radius: 10px; color: #0d47a1 !important; margin-bottom: 10px; }
    .stChatInput textarea { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت والذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما راكبش!")
    st.stop()

@st.cache_resource
def get_working_model():
    try:
        available_models = genai.list_models()
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

WORKING_MODEL = get_working_model()

# 3. واجهة التطبيق
st.title("👨‍🏫 تطبيق LM3LM")
st.write("ارفع صورة التمرين أو اكتب سؤالك (بالدارجة 🇲🇦)")

# خلينا غير "بريز" واحد للصور (Uploader) - هو اللي فيه الكاميرا والغاليري فالتلفون
upload_file = st.file_uploader("📁 ارفع صورة التمرين (أو صور دابا من التيليفون)", type=["jpg", "png", "jpeg"])
audio_file = st.audio_input("🎙️ سجل سؤالك بصوتك")

st.divider()

# عرض الحوار القديم
for msg in st.session_state.messages:
    bubble = "user-bubble" if msg["role"] == "user" else "teacher-bubble"
    st.markdown(f'<div class="{bubble}"><b>{"أنت" if msg["role"]=="user" else "لمعلم"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# صندوق الكتابة
prompt = st.chat_input("اكتب سؤالك هنا...")

# 4. المنطق: المعالجة فقط عند وجود إدخال جديد
if prompt or upload_file or audio_file:
    
    # تحضير المحتوى
    user_input = prompt if prompt else "شرح ليا هاد التمرين"
    
    # منع التكرار: كنشوفو واش هاد السؤال ديجا جاوبنا عليه
    is_new = True
    if st.session_state.messages:
        if st.session_state.messages[-1]["content"] == user_input:
            is_new = False

    if is_new:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-bubble"><b>أنت:</b><br>{user_input}</div>', unsafe_allow_html=True)

        with st.spinner("لمعلم كيوجد الرد..."):
            try:
                model = genai.GenerativeModel(
                    model_name=WORKING_MODEL,
                    generation_config={"max_output_tokens": 400, "temperature": 0.7}
                )
                
                parts = ["أنت 'لمعلم' خبير مغربي. جاوب بالدارجة باختصار ومفيد. اشرح الصور بوضوح."]
                if prompt: parts.append(prompt)
                if upload_file: parts.append(Image.open(upload_file))
                if audio_file: parts.append({"mime_type": "audio/wav", "data": audio_file.getvalue()})

                response = model.generate_content(parts)
                answer = response.text
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.markdown(f'<div class="teacher-bubble"><b>لمعلم:</b><br>{answer}</div>', unsafe_allow_html=True)
                
                st.rerun() # تحديث الصفحة لحبس الـ Loop
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

if st.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

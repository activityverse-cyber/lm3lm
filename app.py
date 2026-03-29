import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. الستايل الاحترافي (Pro UI) والعربية من اليمين
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif; direction: rtl; text-align: right; background-color: #f4f7f9; }
    .main-header { background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 2rem; }
    .stChatMessage { border-radius: 15px; padding: 1rem; margin-bottom: 1rem; direction: rtl !important; }
    .assistant-style { background-color: #ffffff; border-right: 5px solid #1e3c72; color: #1e3c72 !important; }
    .user-style { background-color: #e3f2fd; border-right: 5px solid #2196f3; color: #0d47a1 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب الساروت (API Key) من الخزنة
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # الرابط الرسمي v1 المباشر (مافيهش 404)
    URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ناقص فـ Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الواجهة الرئيسية
st.markdown('<div class="main-header"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>نسخة 2026 المستقرة</p></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    style_class = "user-style" if msg["role"] == "user" else "assistant-style"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="{style_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 4. منطقة الإدخال
uploaded_file = st.sidebar.file_uploader("➕ ارفع صورة التمرين", type=["jpg", "png", "jpeg"])
prompt = st.chat_input("اسأل 'لمعلم' عن أي تمرين...")

# 5. منطق المعالجة (خيط ديريكت)
if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيحلل التمرين..."):
                try:
                    # تحويل الصورة لـ Base64
                    parts = [{"text": f"أنت 'لمعلم' خبير تعليمي مغربي. اشرح للتلميذ بالدارجة المغربية بأسلوب مشجع. سؤاله: {user_text}"}]
                    
                    if uploaded_file:
                        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_b64}})
                    
                    # إرسال الطلب (v1 المباشر)
                    response = requests.post(URL, json={"contents": [{"parts": parts}]})
                    result = response.json()

                    if "candidates" in result:
                        answer = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.rerun()
                    else:
                        st.error(f"مشكل فالسيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                except Exception as e:
                    st.error(f"وقع مشكل تقني: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

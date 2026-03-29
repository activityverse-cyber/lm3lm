import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. الستايل الاحترافي (Premium UI)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Vazirmatn', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f8f9fa; }
    .hero-section { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .bubble { max-width: 85%; padding: 15px; border-radius: 18px; margin-bottom: 10px; line-height: 1.6; display: inline-block; }
    .user-bubble { background-color: #e3f2fd; color: #0d47a1; float: right; border-bottom-right-radius: 4px; border-right: 5px solid #2196f3; }
    .ai-bubble { background-color: white; color: #1e3c72; float: left; border-bottom-left-radius: 4px; border-right: 5px solid #1e3c72; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .stChatInput { direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الرابط المباشر (Direct API)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # استعملنا v1 (النسخة المستقرة) اللي مافيهاش 404
    API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ناقص فـ Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الواجهة
st.markdown('<div class="hero-section"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>ذكاء اصطناعي مغربي نقي ومسكد 🇲🇦</p></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    style = "user-bubble" if msg["role"] == "user" else "ai-bubble"
    st.markdown(f'<div style="width:100%; display:flow-root;"><div class="bubble {style}">{msg["content"]}</div></div>', unsafe_allow_html=True)

# 4. أدوات الإدخال
with st.sidebar:
    st.header("🛠️ الأدوات")
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    if st.button("🗑️ مسح الحوار"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("اسأل 'لمعلم' هنا...")

# 5. منطق الإرسال (The Pro Direct Connection)
if prompt or uploaded_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            with st.spinner("لمعلم كيجاوب دبا..."):
                try:
                    # تحضير البيانات
                    parts = [{"text": f"أنت 'لمعلم' خبير مغربي. جاوب بالدارجة باختصار ومفيد. سؤاله: {user_text}"}]
                    
                    if uploaded_file:
                        img_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_data}})
                    
                    # طلب مباشر للسيرفر
                    payload = {"contents": [{"parts": parts}]}
                    response = requests.post(API_URL, json=payload)
                    result = response.json()

                    if "candidates" in result:
                        answer = result['candidates'][0]['content']['parts'][0]['text']
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.rerun()
                    else:
                        st.error(f"مشكل فالسيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")
                except Exception as e:
                    st.error(f"وقع مشكل تقني: {e}")

st.markdown("<br><center><small>Ibravolt Digital - El Jadida 2026</small></center>", unsafe_allow_html=True)

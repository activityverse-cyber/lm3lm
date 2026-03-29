import streamlit as st
import requests
import base64
from PIL import Image
import io

# 1. إعداد الصفحة (العربية من اليمين 100%)
st.set_page_config(page_title="LM3LM - لملم", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .stMarkdown, .stText, .stAlert, .stChatMessage { direction: rtl; text-align: right; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin: 10px 0; display: block; width: 100%; }
    .user-bubble { background-color: #e3f2fd; border-right: 5px solid #2196f3; color: #0d47a1; }
    .teacher-bubble { background-color: #f1f8e9; border-right: 5px solid #4caf50; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب الساروت (API Key)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # الرابط الرسمي v1 اللي ما كيديرش 404
    URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ناقص فـ Secrets!")
    st.stop()

# 3. واجهة التطبيق
st.title("👨‍🏫 تطبيق LM3LM")
st.write("مساعدك الدراسي الذكي بالدارجة 🇲🇦")

# أدوات التصوير والرفع (جنب لجنب)
col1, col2 = st.columns(2)
with col1:
    cam_file = st.camera_input("📸 صور التمرين")
with col2:
    upload_file = st.file_uploader("📁 ارفع صورة", type=["jpg", "png", "jpeg"])

# الميكرو
audio_file = st.audio_input("🎙️ سجل سؤالك بصوتك")

st.divider()

# ذاكرة الحوار
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الحوار
for msg in st.session_state.messages:
    bubble_type = "user-bubble" if msg["role"] == "user" else "teacher-bubble"
    st.markdown(f'<div class="chat-bubble {bubble_type}">{msg["content"]}</div>', unsafe_allow_html=True)

# صندوق الكتابة
prompt = st.chat_input("اكتب سؤالك هنا...")

# دالة تحويل الصور لـ Base64
def img_to_b64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# 4. معالجة الطلب
if prompt or cam_file or upload_file or audio_file:
    user_text = prompt if prompt else "شرح ليا هاد التمرين"
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.spinner("لمعلم كيوجد الرد..."):
        try:
            parts = [{"text": f"أنت 'لمعلم' خبير تعليمي مغربي. اشرح للتلميذ بالدارجة المغربية بأسلوب مشجع ومبسط. سؤاله: {user_text}"}]
            
            # إضافة الصورة إذا وجدت
            active_img = cam_file if cam_file else upload_file
            if active_img:
                img_b64 = img_to_b64(Image.open(active_img))
                parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_b64}})
            
            # إضافة الصوت إذا وجد
            if audio_file:
                audio_b64 = base64.b64encode(audio_file.getvalue()).decode("utf-8")
                parts.append({"inline_data": {"mime_type": "audio/wav", "data": audio_b64}})

            # إرسال الطلب (v1)
            payload = {"contents": [{"parts": parts}]}
            response = requests.post(URL, json=payload)
            result = response.json()

            if "candidates" in result:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(f'<div class="chat-bubble teacher-bubble">{answer}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"مشكل فالسيرفر: {result.get('error', {}).get('message', 'خطأ غير معروف')}")

        except Exception as e:
            st.error(f"وقع مشكل تقني: {e}")

if st.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

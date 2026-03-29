import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="LM3LM - الحوار الذكي", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .chat-message { padding: 15px; border-radius: 15px; margin-bottom: 10px; display: inline-block; width: auto; max-width: 80%; }
    .user-msg { background-color: #e1f5fe; float: right; color: #0277bd; }
    .teacher-msg { background-color: #f1f8e9; float: left; border-right: 5px solid #558b2f; color: #2e7d32; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. تفعيل الذاكرة (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. الربط مع الساروت
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("⚠️ الساروت ناقص!")
    st.stop()

# 4. واجهة المستخدم
st.title("👨‍🏫 معلمك الخاص: حوار ذكي")

# --- القائمة الجانبية للكاميرا والصوت ---
with st.sidebar:
    st.header("📸 أدوات المساعدة")
    
    # اختيار الكاميرا (زدنا تحسين باش تبان أوضح)
    enable_cam = st.checkbox("فتح الكاميرا")
    img_file = None
    if enable_cam:
        img_file = st.camera_input("صور التمرين بوضوح", help="حاول تجيب الضو مزيان باش تكون الصورة واضحة")
    
    st.divider()
    
    # أيقونة الميكرو (ملاحظة: Streamlit كتحتاج إضافة خاصة للصوت، غانديرو دابا مساحة للصوت)
    st.write("🎙️ التحدث مع لمعلم")
    audio_value = st.audio_input("اضغط وسجل سؤالك")

# --- عرض الحوار (Chat Interface) ---
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role_class = "user-msg" if message["role"] == "user" else "teacher-msg"
        st.markdown(f'<div class="chat-message {role_class}">{message["content"]}</div>', unsafe_allow_html=True)
        st.write("") # فاصل

# --- إدخال النص أو معالجة الصورة ---
prompt = st.chat_input("اكتب سؤالك هنا أو صور التمرين...")

if prompt or img_file or audio_value:
    user_content = prompt if prompt else "شوف هاد التمرين (صورة/صوت)"
    
    # إضافة سؤال التلميذ للذاكرة
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("assistant"):
        with st.spinner("لمعلم كيفكر..."):
            try:
                # جمع البيانات (نص + صورة + صوت إذا وجد)
                content_list = [f"أنت 'لمعلم' خبير مغربي. جاوب التلميذ بالدارجة المغربية بأسلوب مشجع. إذا كانت هناك صورة، اشرحها خطوة بخطوة."]
                if prompt: content_list.append(prompt)
                if img_file: content_list.append(Image.open(img_file))
                if audio_value: content_list.append("التلميذ أرسل تسجيلاً صوتياً، جاوبه على سؤاله.")

                response = model.generate_content(content_list)
                full_response = response.text
                
                st.markdown(f'<div class="chat-message teacher-msg">{full_response}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"وقع مشكل: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("تمسح الحوار؟"):
    st.session_state.messages = []
    st.rerun()

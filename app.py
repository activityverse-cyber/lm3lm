import streamlit as st
import google.generativeai as genai
from PIL import Image

# ... (نفس الستايل والربط اللي درنا قبل)

# 1. إعداد الذاكرة والحالة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. واجهة التطبيق
st.title("👨‍🏫 تطبيق LM3LM")

# الأدوات (صور، رفع، صوت)
col1, col2 = st.columns(2)
with col1: cam_file = st.camera_input("📸 صور")
with col2: upload_file = st.file_uploader("📁 ارفع", type=["jpg", "png", "jpeg"])
audio_file = st.audio_input("🎙️ سجل")

# عرض الحوار القديم (باش ما يتكررش)
for msg in st.session_state.messages:
    role_bubble = "user-bubble" if msg["role"] == "user" else "teacher-bubble"
    st.markdown(f'<div class="{role_bubble}">{msg["content"]}</div>', unsafe_allow_html=True)

# صندوق الكتابة
prompt = st.chat_input("اكتب سؤالك هنا...")

# 3. المنطق: "الديجونكتور" اللي كيمنع التكرار
# الجواب كيكون "فقط" إلا ضغطنا على Enter فـ ChatInput أو صورنا حاجة جديدة
if prompt or cam_file or upload_file or audio_file:
    
    # تحريفة ذكية: كنشوفو واش هاد السؤال هو نيت اللخر اللي كاين فـ الذاكرة
    last_msg = st.session_state.messages[-1]["content"] if st.session_state.messages else ""
    
    # إلا كان السؤال جديد وماشي تكرار
    if prompt != last_msg:
        user_input = prompt if prompt else "شرح ليا هاد التمرين"
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # كنعاودو نرسمو سؤال المستخدم دغيا
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
        
        with st.spinner("لمعلم كيشوف الحل..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                # ... (نفس إعدادات التوليد اللي درنا قبل)
                
                response = model.generate_content(parts)
                answer = response.text
                
                # حفظ الجواب فـ الذاكرة وعرضه مرة واحدة
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.markdown(f'<div class="teacher-bubble">{answer}</div>', unsafe_allow_html=True)
                
                # مهم جداً: كديرو Rerun باش نحبسو أي Loop
                st.rerun()
                
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

# زر المسح
if st.button("🗑️ مسح الحوار"):
    st.session_state.messages = []
    st.rerun()

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. القالب الجمالي (Advanced CSS)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right;
        background-color: #f0f2f6;
    }

    /* هيدر عصري (Gradient Hero) */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* فقاعات الشات الاحترافية */
    .chat-row { display: flex; margin-bottom: 20px; width: 100%; }
    .row-reverse { flex-direction: row-reverse; }
    
    .bubble {
        max-width: 80%;
        padding: 15px 20px;
        border-radius: 20px;
        font-size: 1.1rem;
        line-height: 1.5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .user-bubble {
        background-color: #2196f3;
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .ai-bubble {
        background-color: white;
        color: #1e3c72;
        border-bottom-left-radius: 4px;
        border-right: 6px solid #1e3c72;
    }

    /* تحسين الأزرار */
    .stButton>button {
        border-radius: 30px;
        border: none;
        background: #1e3c72;
        color: white;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #2a5298; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد "الماكينة" (Model Configuration)
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # 1.5-flash هو الموديل "الديونامو" لعام 2026
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("⚠️ الساروت GOOGLE_API_KEY ما راكبش مزيان فـ Secrets")
    st.stop()

# 3. واجهة المستخدم (UI)
st.markdown('<div class="hero-section"><h1>👨‍🏫 LM3LM - لمعلم</h1><p>ذكاء اصطناعي بلمسة "حريفية" مغربية 🇲🇦</p></div>', unsafe_allow_html=True)

# عرض سجل الحوار بستايل نظيف
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    alignment = "row-reverse" if is_user else ""
    bubble_type = "user-bubble" if is_user else "ai-bubble"
    
    st.markdown(f"""
        <div class="chat-row {alignment}">
            <div class="bubble {bubble_type}">{msg["content"]}</div>
        </div>
    """, unsafe_allow_html=True)

# 4. منطقة الأدوات (Sidebar)
with st.sidebar:
    st.header("🛠️ أدوات المساعدة")
    uploaded_file = st.file_uploader("📸 ارفع صورة التمرين", type=["jpg", "jpeg", "png"])
    audio_data = st.audio_input("🎙️ سجل سؤالك بالصوت")
    st.divider()
    if st.button("🗑️ مسح الحوار", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.info("📍 Ibravolt - El Jadida")

# 5. صندوق الشات الرئيسي
prompt = st.chat_input("اسأل 'لمعلم' عن أي حاجة...")

# 6. منطق المعالجة الاحترافي (Smart Logic)
if prompt or uploaded_file or audio_data:
    # تحديد محتوى سؤال المستخدم
    current_user_content = prompt if prompt else "شوف هاد التمرين (صورة/صوت)"
    
    # "الديجونكتور": التأكد بلي ما كنكرروش نفس السؤال
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != current_user_content:
        st.session_state.messages.append({"role": "user", "content": current_user_content})
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("لمعلم كيشرح..."):
                try:
                    # تحضير "البرانشمان" للموديل
                    instruction = "أنت 'لمعلم' خبير مغربي. جاوب بالدارجة المغربية بأسلوب مبسط ومحفز. ركز على الخطوات."
                    parts = [instruction]
                    
                    if prompt: parts.append(prompt)
                    if uploaded_file: parts.append(Image.open(uploaded_file))
                    if audio_data: parts.append({"mime_type": "audio/wav", "data": audio_data.getvalue()})
                    
                    response = model.generate_content(parts)
                    full_response = response.text
                    
                    # حفظ وعرض الجواب
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun() # تحديث الصفحة لعرض الحوار مرتب
                    
                except Exception as e:
                    if "429" in str(e):
                        st.error("🚫 الكوطا تسالات! تسنى 20 ثانية وعاود ورك.")
                    else:
                        st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small>Ibravolt Digital Solutions - 2026</small></center>", unsafe_allow_html=True)

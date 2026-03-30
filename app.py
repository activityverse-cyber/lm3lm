import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعدادات الواجهة الاحترافية (Premium UI/UX)
st.set_page_config(page_title="أستاذ - Oustad Pro", page_icon="👨‍🏫", layout="wide")

# CSS لإجبار التصميم واللغة والاتجاه
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        background-color: #fcfdfe !important;
    }

    /* هيدر احترافي */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 5%;
        background: white;
        border-bottom: 1px solid #f0f0f0;
    }
    .credit-badge {
        background: #fff9db;
        color: #f08c00;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #ffe066;
    }

    /* كارت الخطة */
    .plan-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    /* تنسيق اختيار المادة (Cards) */
    .stRadio div[role="radiogroup"] {
        display: flex;
        gap: 15px;
        justify-content: center;
        flex-wrap: wrap;
    }
    .stRadio div[role="radiogroup"] label {
        background: white !important;
        border: 2px solid #f1f3f5 !important;
        border-radius: 15px !important;
        padding: 15px 25px !important;
        transition: 0.3s !important;
    }
    .stRadio div[role="radiogroup"] label:hover {
        border-color: #1a73e8 !important;
    }

    /* منطقة الشرح (Answer Box) */
    .answer-container {
        background: white;
        border-right: 6px solid #1a73e8;
        padding: 30px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        unicode-bidi: plaintext; /* سحر اليمين لليسار التلقائي */
        text-align: start;
        color: #2d3436 !important;
    }

    /* إخفاء الزوائد */
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد "أستاذ" (AI Logic)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def load_ustad_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash = [m for m in models if "flash" in m]
        return flash[0] if flash else models[0]
    
    WORKING_MODEL = load_ustad_model()
except:
    st.error("⚠️ يرجى ضبط مفتاح API في Secrets (GOOGLE_API_KEY)")
    st.stop()

# 3. بناء واجهة المستخدم (The Interface)
st.markdown("""
    <div class="top-nav">
        <h2 style="color:#1a73e8; margin:0;">👨‍🏫 أستاذ (Oustad)</h2>
        <div class="credit-badge">⚡ رصيد اليوم: 1</div>
    </div>
    <div class="plan-card">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:24px;">🔓</div>
            <div>
                <b style="color:black;">الخطة المجانية</b><br>
                <small style="color:gray;">تمرين واحد متبقي لك اليوم</small>
            </div>
        </div>
        <button style="background:#00b894; color:white; border:none; padding:10px 20px; border-radius:10px; font-weight:bold;">الترقية لـ Premium</button>
    </div>
    """, unsafe_allow_html=True)

# قسم اختيار المادة (إجباري وفعال)
st.markdown("<div style='max-width:800px; margin:0 auto;'><b>اختر المادة:</b></div>", unsafe_allow_html=True)
subject = st.radio(
    "المادة",
    ["📐 رياضيات", "⚛️ فيزياء", "🧪 كيمياء", "📚 أخرى"],
    horizontal=True,
    label_visibility="collapsed"
)

# 4. استيراد التمرين والشات (Interaction Zone)
st.markdown("<br><div style='max-width:800px; margin:0 auto;'><b>استيراد التمرين أو طرح سؤال:</b></div>", unsafe_allow_html=True)

col_chat, col_upload = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader("ارفع صورة التمرين", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        st.image(uploaded_file, caption="التمرين المرفوع", use_container_width=True)

with col_chat:
    user_input = st.chat_input("اسأل أستاذ عن أي شيء...")

# 5. منطق المعالجة (The Engine)
if user_input or uploaded_file:
    # تحديد النص المطلوب معالجته
    final_query = user_input if user_input else f"ممكن تشرح ليا هاد التمرين فـ مادة {subject}؟"
    
    # إضافة سؤال المستخدم للذاكرة
    st.session_state.chat_history.append({"role": "user", "content": final_query})
    
    with st.chat_message("assistant"):
        with st.spinner("أستاذ يحلل ويشرح..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                
                # توجيهات بيداغوجية صارمة
                instruction = f"""أنت 'أستاذ' مغربي خبير في مادة {subject}.
                - اشرح بلهجة مغربية (دارجة) بيضاء، محترمة، وسهلة الفهم.
                - ابدأ بالترحيب بالتلميذ.
                - لا تعطي الجواب مباشرة، بل اشرح المراحل والقواعد المستعملة.
                - إذا كان هناك نص بالفرنسية أو معادلات، حافظ على ترتيبها من اليسار.
                - إذا كان النص عربياً، ابدأه من اليمين."""
                
                parts = [instruction]
                # إضافة الذاكرة (آخر 3 رسائل للخفة)
                for m in st.session_state.chat_history[-3:]:
                    parts.append(f"{m['role']}: {m['content']}")
                
                if uploaded_file:
                    parts.append(Image.open(uploaded_file))
                if user_input:
                    parts.append(user_input)

                response = model.generate_content(parts)
                answer = response.text
                
                # عرض النتيجة في إطار "أستاذ" الفخم
                st.markdown(f"""
                    <div class="answer-container">
                        <b style="color:#1a73e8; font-size:1.2rem;">💡 شرح الأستاذ:</b><br><br>
                        {answer}
                    </div>
                """, unsafe_allow_html=True)
                
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"عذراً، وقع عطل فني: {e}")

st.markdown("<br><hr><center><small style='color:gray;'>منصة أستاذ التعليمية - تطويـر Ibravolt 2026</small></center>", unsafe_allow_html=True)

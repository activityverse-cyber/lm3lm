import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعدادات الصفحة (Page Configuration)
st.set_page_config(
    page_title="أستاذ - Oustad Pro",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. كود CSS "الفينيسيون" (Custom Styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        background-color: #fcfdfe !important;
    }

    /* تنسيق السايدبار */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-left: 1px solid #f0f0f0; }
    .sidebar-item { display: flex; align-items: center; padding: 12px 20px; margin: 5px 10px; border-radius: 12px; color: #3c4043; font-weight: 500; }
    .active-item { background-color: #e6fcf5 !important; color: #00b894 !important; }
    .pro-item { background-color: #fff9db !important; color: #f08c00 !important; }

    /* الهيدر العلوي */
    .header-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: white; border-bottom: 1px solid #f0f0f0; }
    .logo-text { color: #1a73e8; font-weight: 700; font-size: 1.5rem; }
    .credit-tag { background: #fff9db; padding: 5px 15px; border-radius: 20px; color: #f08c00; font-weight: bold; border: 1px solid #ffe066; }

    /* منطقة الرفع والحل */
    .upload-card { background: white; border: 2px dashed #dfe6e9; border-radius: 24px; padding: 40px; text-align: center; max-width: 800px; margin: 0 auto; }
    .answer-box { background: white; border-right: 6px solid #1a73e8; padding: 25px; border-radius: 15px; margin-top: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); unicode-bidi: plaintext; text-align: start; color: #000 !important; }
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header {visibility: hidden;}
    .stFileUploader label { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد "أستاذ" (AI Setup)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    @st.cache_resource
    def get_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash = [m for m in models if "flash" in m]
        return flash[0] if flash else models[0]
    WORKING_MODEL = get_model()
except:
    st.error("⚠️ تأكد من وضع GOOGLE_API_KEY في Secrets")
    st.stop()

# 4. بناء السايدبار (Sidebar)
with st.sidebar:
    st.markdown("""
        <div class="sidebar-item active-item">🏠 &nbsp; Accueil</div>
        <div class="sidebar-item">🕒 &nbsp; Historique</div>
        <div class="sidebar-item pro-item">⚡ &nbsp; Passer au pro</div>
        <div style="height: 45vh;"></div>
        <div style="border-top: 1px solid #eee; padding-top: 20px;">
            <div class="sidebar-item">🌐 &nbsp; FR Français</div>
            <div class="sidebar-item">⚙️ &nbsp; Paramètres</div>
            <div class="sidebar-item" style="color: #eb4d4b;">↪️ &nbsp; Déconnexion</div>
        </div>
    """, unsafe_allow_html=True)

# 5. واجهة المستخدم الرئيسية (Main UI)
st.markdown("""
    <div class="header-bar">
        <div class="logo-text">👨‍🏫 أستاذ</div>
        <div class="credit-tag">⚡ رصيد يومي : 1</div>
    </div>
    """, unsafe_allow_html=True)

# اختيار المادة
st.markdown('<div style="max-width:800px; margin: 20px auto 10px;"><b>اختر المادة:</b></div>', unsafe_allow_html=True)
subject = st.radio("Matière", ["📊 Maths", "⚛️ Physique", "🧪 Chimie", "📚 Autre"], horizontal=True, label_visibility="collapsed")

# منطقة الرفع
st.markdown('<div style="max-width:800px; margin: 20px auto 10px;"><b>استورد تمرينك:</b></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"])

if not uploaded_file:
    st.markdown("""
        <div class="upload-card">
            <div style="font-size:50px;">📤</div>
            <h3 style="color:#2d3436;">Importez votre exercice</h3>
            <p style="color:#636e72;">اضغط هنا أو اسحب الصورة<br><small>PNG, JPG حتى 10MB</small></p>
        </div>
    """, unsafe_allow_html=True)
else:
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين المرفوع", width=400)
    
    if st.button("يا أستاذ، عطيني الحل", use_container_width=True):
        with st.spinner("أستاذ كيشرح ليك دابا..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                response = model.generate_content([
                    f"أنت 'أستاذ' مغربي خبير. اشرح هاد التمرين ديال {subject} بالدارجة المغربية بأسلوب مبسط وواضح. ابدأ من اليمين واستعمل اللون الأسود.",
                    img
                ])
                st.markdown(f'<div class="answer-box"><b>💡 شرح الأستاذ:</b><br><br>{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small>© 2026 Oustad Pro - Ibravolt</small></center>", unsafe_allow_html=True)

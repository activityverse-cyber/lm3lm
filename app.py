import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة (هادشي كيتكتب مرة وحدة فالفوق)
st.set_page_config(page_title="أستاذ - Oustad Pro", page_icon="👨‍🏫", layout="wide")

# 2. الفينيسيون (CSS) - كاع الزواق واللغة هنا
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    /* فرض اليمين والخط الأسود */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #fcfdfe !important;
        color: #000000 !important;
    }

    /* الهيدر العلوي */
    .header-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: white; border-bottom: 1px solid #f0f0f0; }
    .logo-text { color: #1a73e8; font-weight: 700; font-size: 1.5rem; }

    /* السايدبار */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-left: 1px solid #f0f0f0; }
    .sidebar-item { padding: 12px 20px; margin: 5px 10px; border-radius: 12px; color: #3c4043; font-weight: 500; }
    .active-item { background-color: #e6fcf5; color: #00b894; }

    /* إطار الجواب (واضح جدا) */
    .answer-box {
        background: white; border-right: 8px solid #1a73e8; padding: 25px; 
        border-radius: 15px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        color: #000000 !important; font-size: 1.2rem; text-align: right;
    }
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. الربط بالساروت (API)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # دالة ذكية باش ما يوقعش مشكل 404
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    WORKING_MODEL = [m for m in models if "flash" in m][0]
except:
    st.error("⚠️ خاصك تزيد GOOGLE_API_KEY فـ Secrets ديال Streamlit")
    st.stop()

# 4. بناء السايدبار (Sidebar)
with st.sidebar:
    st.markdown('<div class="sidebar-item active-item">🏠 الرئيسية</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🕒 التاريخ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item" style="background:#fff9db; color:#f08c00;">⚡ ترقية للحساب</div>', unsafe_allow_html=True)
    st.write("---")
    st.markdown('<div class="sidebar-item">⚙️ الإعدادات</div>', unsafe_allow_html=True)

# 5. الواجهة الرئيسية
st.markdown("""
    <div class="header-bar">
        <div class="logo-text">👨‍🏫 أستاذ (Oustad)</div>
        <div style="font-weight:bold; color:#f08c00;">⚡ رصيد اليوم: 1</div>
    </div>
    """, unsafe_allow_html=True)

# اختيار المادة
st.write("### اختر المادة:")
subject = st.radio("Matière", ["رياضيات", "فيزياء", "كيمياء", "أخرى"], horizontal=True, label_visibility="collapsed")

# منطقة الرفع
st.write("### استيراد التمرين:")
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين المرفوع", width=400)
    
    if st.button("يا أستاذ، شرح ليا هادشي بوضوح", use_container_width=True):
        with st.spinner("أستاذ كيكتب ليك الحل..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                response = model.generate_content([
                    f"أنت 'أستاذ' مغربي. اشرح هاد التمرين ديال {subject} بالدارجة المغربية بأسلوب مبسط جدا. استعمل الخط العريض والأسود. ابدأ من اليمين.",
                    img
                ])
                # عرض الجواب فإطار فخم
                st.markdown(f'<div class="answer-box"><b>💡 شرح الأستاذ:</b><br><br>{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"مشكل تقني: {e}")
else:
    st.info("👆 ارفع صورة التمرين باش يبدأ الأستاذ الشرح")

st.markdown("<br><center><small>© 2026 Oustad Pro - Ibravolt</small></center>", unsafe_allow_html=True)

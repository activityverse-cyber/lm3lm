import streamlit as st

# 1. إعدادات الهوية البصرية (Meta Tags & Page Config)
st.set_page_config(
    page_title="أستاذ - Oustad Pro",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. كود CSS الاحترافي (الفينيسيون ديال ScanToSolve)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;700&display=swap');
    
    /* الأساسيات */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        background-color: #fcfdfe !important;
    }

    /* الهيدر العلوي (Top Navigation) */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 5%;
        background: white;
        border-bottom: 1px solid #f0f0f0;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .logo-text { color: #1a73e8; font-weight: 700; font-size: 1.5rem; }
    .credit-box {
        background: #fff9db;
        border: 1px solid #ffe066;
        padding: 5px 15px;
        border-radius: 20px;
        color: #f08c00;
        font-weight: bold;
    }

    /* كارت الخطة (Premium Card) */
    .plan-section {
        max-width: 800px;
        margin: 20px auto;
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #eef0f2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .btn-upgrade {
        background-color: #00b894;
        color: white !important;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
    }

    /* عنوان الأقسام */
    .section-label {
        max-width: 800px;
        margin: 30px auto 10px;
        font-weight: bold;
        color: #2d3436;
    }

    /* منطقة الرفع (Upload Zone) */
    .upload-container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        border: 2px dashed #dfe6e9;
        border-radius: 24px;
        padding: 50px 20px;
        text-align: center;
        transition: 0.3s;
    }
    .upload-container:hover { border-color: #1a73e8; background: #f8fbff; }

    /* إخفاء واجهة ستريمليت الأصلية */
    #MainMenu, footer, header {visibility: hidden;}
    .stFileUploader label { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. رسم الواجهة (UI Elements)

# --- الهيدر ---
st.markdown("""
    <div class="header-bar">
        <div class="logo-text">👨‍🏫 أستاذ</div>
        <div class="credit-box">⚡ رصيد يومي : 1</div>
    </div>
    """, unsafe_allow_html=True)

# --- كارت الخطة ---
st.markdown("""
    <div class="plan-section">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:24px;">🔓</div>
            <div>
                <b style="color:black;">الخطة المجانية</b><br>
                <small style="color:gray;">1 تمرين متبقي اليوم</small>
            </div>
        </div>
        <a class="btn-upgrade">Passer à Premium</a>
    </div>
    """, unsafe_allow_html=True)

# --- اختيار المادة ---
st.markdown('<div class="section-label">Sélectionnez la matière</div>', unsafe_allow_html=True)

# هنا غانخدمو بـ columns باش نديرو المربعات ديال المواد
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("📊 Maths", use_container_width=True)
with col2:
    st.button("⚛️ Physique", use_container_width=True)
with col3:
    st.button("🧪 Chimie", use_container_width=True)
with col4:
    st.button("📚 Autre", use_container_width=True)

# --- منطقة الرفع ---
st.markdown('<div class="section-label">Importez votre exercice</div>', unsafe_allow_html=True)

# الـ Uploader الحقيقي غانغطيوه بالديكور
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"])

if not uploaded_file:
    st.markdown("""
        <div class="upload-container">
            <div style="font-size:50px; color:#1a73e8; margin-bottom:15px;">📤</div>
            <h3 style="color:#2d3436; margin-bottom:5px;">Importez votre exercice</h3>
            <p style="color:#636e72;">Cliquez ou glissez-déposez une image<br><small>PNG, JPG jusqu'à 10MB</small></p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("✅ الصورة ترفعات ناضية! دابا خاصنا نربطوها بـ 'أستاذ'.")

st.markdown("<br><br><center><small style='color:#a0aec0;'>© 2026 Oustad Pro - Powered by Ibravolt</small></center>", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="LM3LM - ScanToSolve", page_icon="👨‍🏫", layout="wide")

# 2. كود CSS "الحريفي" لقلب الموازين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        background-color: #fcfdfe !important;
    }

    /* هيدر النقط (Credits) */
    .top-bar {
        display: flex;
        justify-content: flex-end;
        padding: 10px 20px;
    }
    .credits-tag {
        background: white;
        padding: 5px 15px;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        font-weight: bold;
        color: #ffa502;
    }

    /* كارت الخطة المجانية */
    .plan-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        margin: 20px auto;
        max-width: 800px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .btn-premium {
        background-color: #00b894;
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
    }

    /* قسم اختيار المواد */
    .section-title { margin: 30px auto 20px; max-width: 800px; font-weight: bold; color: #2d3436; }
    
    .subject-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        max-width: 800px;
        margin: 0 auto 30px;
    }
    .subject-item {
        background: white;
        border: 2px solid #f0f0f0;
        border-radius: 15px;
        padding: 25px 10px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
    }
    .subject-item:hover { border-color: #00b894; transform: translateY(-3px); }
    .subject-item.active { border-color: #00b894; background: #f0fffb; }
    .sub-icon { font-size: 28px; margin-bottom: 10px; display: block; }

    /* منطقة الرفع (The Large Drop Zone) */
    .drop-zone {
        background: white;
        border: 2px dashed #dfe6e9;
        border-radius: 20px;
        padding: 60px 20px;
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        color: #636e72;
    }
    .upload-icon { font-size: 50px; color: #00b894; margin-bottom: 15px; }

    /* إخفاء واجهة ستريمليت الأصلية */
    [data-testid="stFileUploader"] {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر العلوي
st.markdown("""
    <div class="top-bar">
        <div class="credits-tag">⚡ رصيد اليوم: 1</div>
    </div>
    <div class="plan-card">
        <div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:#e6fcf5; padding:10px; border-radius:12px;">⚡</div>
                <div>
                    <b style="font-size:16px;">الخطة المجانية</b><br>
                    <small style="color:#636e72;">تمرين واحد متبقي اليوم</small>
                </div>
            </div>
        </div>
        <button class="btn-premium">الترقية لـ Premium</button>
    </div>
    """, unsafe_allow_html=True)

# 4. اختيار المادة (Grid)
st.markdown('<div class="section-title">اختر المادة</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="subject-grid">
        <div class="subject-item active">
            <span class="sub-icon">📊</span>
            <b>رياضيات</b>
        </div>
        <div class="subject-item">
            <span class="sub-icon">⚛️</span>
            <b>فيزياء</b>
        </div>
        <div class="subject-item">
            <span class="sub-icon">🧪</span>
            <b>كيمياء</b>
        </div>
        <div class="subject-item">
            <span class="sub-icon">📚</span>
            <b>أخرى</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. منطقة الرفع (The Functional Part)
st.markdown('<div class="section-title">استيراد التمرين</div>', unsafe_allow_html=True)

# غانحطو الـ Uploader الحقيقي فوق الديكور بـ ستايل مخفي
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if not uploaded_file:
    st.markdown("""
        <div class="drop-zone">
            <div class="upload-icon">📤</div>
            <h3>استورد تمرينك</h3>
            <p>اضغط هنا أو اسحب الصورة<br><small>PNG, JPG حتى 10MB</small></p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.image(uploaded_file, caption="التمرين جاهز للتحليل", use_container_width=True)
    if st.button("يا لمعلم، عطيني الحل", use_container_width=True):
        with st.spinner("لمعلم كيشوف فـ الورقة..."):
            # هنا كيدخل كود الذكاء الاصطناعي ديالنا
            st.info("لمعلم كيقرا دابا.. الجواب غايطلع هنا!")

st.markdown("<br><br><center><small>Ibravolt Digital Solution - El Jadida 2026</small></center>", unsafe_allow_html=True)

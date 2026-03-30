import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. إعداد الصفحة والستايل (RTL & ScanToSolve Design)
st.set_page_config(page_title="LM3LM - Scan & Solve", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;700&display=swap');
    
    /* فرض اليمين لليسار على كل شيء */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #fcfdfe !important;
    }

    /* الهيدر العلوي */
    .top-bar { display: flex; justify-content: flex-end; padding: 10px 20px; }
    .credits-tag { background: white; padding: 5px 15px; border-radius: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #eee; font-weight: bold; color: #ffa502; }

    /* كارت الخطة */
    .plan-card {
        background: #ffffff; border-radius: 20px; padding: 20px; margin: 20px auto; max-width: 800px;
        display: flex; justify-content: space-between; align-items: center; border: 1px solid #f0f0f0;
    }
    .btn-premium { background-color: #00b894; color: white; border: none; padding: 10px 25px; border-radius: 12px; font-weight: bold; }

    /* شبكة المواد */
    .subject-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; max-width: 800px; margin: 0 auto 30px; }
    .subject-item { background: white; border: 2px solid #f0f0f0; border-radius: 15px; padding: 20px 10px; text-align: center; }
    .subject-item.active { border-color: #00b894; background: #f0fffb; }

    /* منطقة الرفع */
    .drop-zone { background: white; border: 2px dashed #dfe6e9; border-radius: 20px; padding: 40px; text-align: center; max-width: 800px; margin: 0 auto; }
    
    /* تنسيق رد المعلم */
    .answer-box {
        background-color: #ffffff; border-right: 6px solid #1e3c72; padding: 20px; 
        border-radius: 15px; margin: 20px auto; max-width: 800px; color: #1e3c72;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد "المعلم" (Gemini API)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # البحث عن الموديل الشغال تلقائياً
    model_name = "gemini-1.5-flash" 
    model = genai.GenerativeModel(model_name)
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ناقص فـ Secrets!")
    st.stop()

# 3. عرض الواجهة (HTML)
st.markdown("""
    <div class="top-bar"><div class="credits-tag">⚡ رصيد اليوم: 1</div></div>
    <div class="plan-card">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="background:#e6fcf5; padding:10px; border-radius:12px;">⚡</div>
            <div><b>الخطة المجانية</b><br><small style="color:#636e72;">تمرين واحد متبقي اليوم</small></div>
        </div>
        <button class="btn-premium">الترقية لـ Premium</button>
    </div>
    <div style="max-width:800px; margin:0 auto;"><b>اختر المادة</b></div>
    <div class="subject-grid">
        <div class="subject-item active"><span>📊</span><br><b>رياضيات</b></div>
        <div class="subject-item"><span>⚛️</span><br><b>فيزياء</b></div>
        <div class="subject-item"><span>🧪</span><br><b>كيمياء</b></div>
        <div class="subject-item"><span>📚</span><br><b>أخرى</b></div>
    </div>
    """, unsafe_allow_html=True)

# 4. منطقة الرفع والعمل (Logic)
st.markdown('<div style="max-width:800px; margin:0 auto; margin-bottom:10px;"><b>استيراد التمرين</b></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if not uploaded_file:
    st.markdown("""
        <div class="drop-zone">
            <div style="font-size:40px; color:#00b894;">📤</div>
            <h3>استورد تمرينك</h3>
            <p>اضغط هنا أو اسحب الصورة</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # عرض الصورة المصغرة
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين جاهز", width=300)
    
    # الزر الحقيقي اللي غايخدم "لمعلم"
    if st.button("يا لمعلم، عطيني الحل ودير الواجب", use_container_width=True):
        with st.spinner("لمعلم كيقرا التمرين بالدقة..."):
            try:
                # إرسال الصورة للموديل
                response = model.generate_content([
                    "أنت 'لمعلم' خبير مغربي. اشرح هذا التمرين بالدارجة المغربية بأسلوب مشجع ومبسط. ابدأ دائما من اليمين.",
                    img
                ])
                
                # عرض الجواب في إطار جميل
                st.markdown(f"""
                    <div class="answer-box">
                        <h3 style="color:#00b894;">💡 رد لمعلم:</h3>
                        {response.text}
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"وقع مشكل تقني: {e}")

st.markdown("<br><center><small>Ibravolt Digital - El Jadida 2026</small></center>", unsafe_allow_html=True)

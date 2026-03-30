import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد الصفحة والستايل (RTL & High Contrast Design)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    /* فرض اللغة العربية من اليمين وألوان خط واضحة جداً */
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #fcfdfe !important;
        color: #000000 !important; /* خط أسود أساسي */
    }

    /* هيدر الصفحة */
    .hero { 
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        color: white !important; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 20px; 
    }

    /* فقاعات الحوار - ألوان داكنة للخط */
    .stChatMessage, .stMarkdown, p, li, span {
        color: #000000 !important; /* كاع النصوص تولي سوداء واضحة */
        direction: rtl !important;
        text-align: right !important;
    }

    /* إطار رد لمعلم (High Contrast) */
    .answer-box {
        background-color: #ffffff; 
        border-right: 8px solid #1e3c72; 
        padding: 25px; 
        border-radius: 15px; 
        margin: 20px auto; 
        max-width: 850px; 
        color: #000000 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        line-height: 1.8;
        font-size: 1.2rem;
    }

    /* صناديق اختيار المواد */
    .subject-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; max-width: 850px; margin: 0 auto 30px; }
    .subject-item { 
        background: white; 
        border: 2px solid #2d3436; 
        border-radius: 15px; 
        padding: 15px; 
        text-align: center;
        color: #000000 !important;
        font-weight: bold;
    }
    .subject-item.active { border-color: #00b894; background: #e6fcf5; }

    /* صندوق الكتابة (Input) */
    .stChatInput textarea {
        color: #000000 !important;
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("⚠️ الساروت GOOGLE_API_KEY ناقص فـ Secrets!")
    st.stop()

# 3. واجهة ScanToSolve (المغربية)
st.markdown('<div class="hero"><h1>👨‍🏫 LM3LM - لمعلم</h1><p style="color:white !important;">صور تمرينك.. الحل غايوصلك بالدارجة بوضوح</p></div>', unsafe_allow_html=True)

st.markdown('<div style="max-width:850px; margin:0 auto;"><b>اختر المادة:</b></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="subject-grid">
        <div class="subject-item active">📊<br>رياضيات</div>
        <div class="subject-item">⚛️<br>فيزياء</div>
        <div class="subject-item">🧪<br>كيمياء</div>
        <div class="subject-item">📚<br>أخرى</div>
    </div>
    """, unsafe_allow_html=True)

# 4. منطقة الرفع والحل
st.markdown('<div style="max-width:850px; margin:0 auto;"><b>استيراد التمرين:</b></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين المرفوع", width=400)
    
    if st.button("يا لمعلم، عطيني الحل بوضوح", use_container_width=True):
        with st.spinner("لمعلم كيقرا ويكتب بالخط العريض..."):
            try:
                response = model.generate_content([
                    "أنت 'لمعلم' خبير مغربي. اشرح هذا التمرين بالدارجة المغربية بأسلوب مبسط. اجعل الخطوات واضحة جدا. ابدأ من اليمين.",
                    img
                ])
                
                # عرض الجواب فـ إطار "بروفيسيونال" بخط أسود غامق
                st.markdown(f"""
                    <div class="answer-box">
                        <h2 style="color:#1e3c72; border-bottom: 2px solid #1e3c72; padding-bottom:10px;">💡 رد لمعلم:</h2>
                        <div style="font-size: 1.3rem; font-weight: 500;">
                        {response.text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small style='color:black;'>Ibravolt Digital Solution - El Jadida 2026</small></center>", unsafe_allow_html=True)

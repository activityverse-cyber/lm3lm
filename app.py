import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل الاحترافي (High Contrast & RTL)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #fcfdfe !important;
    }

    /* الهيدر */
    .hero { 
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        color: white !important; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* تنسيق اختيار المواد (Radio Buttons as Cards) */
    .stRadio div[role="radiogroup"] {
        display: flex; gap: 15px; justify-content: center;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #000000 !important; font-weight: bold; font-size: 1.1rem;
    }

    /* إطار الجواب (Answer Box) */
    .answer-box {
        background-color: #ffffff; border-right: 8px solid #1e3c72; 
        padding: 25px; border-radius: 15px; margin: 25px auto; 
        max-width: 900px; color: #000000 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        line-height: 1.8; font-size: 1.2rem;
    }
    
    /* وضوح الخط الأسود */
    .stMarkdown, p, span, label { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط الذكي (الرادار ضد 404)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    @st.cache_resource
    def get_working_model():
        # كيسول السيرفر على الموديلات اللي عاطياك Google دابا
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        flash = [m for m in models if "flash" in m]
        return flash[0] if flash else models[0]
    
    WORKING_MODEL = get_working_model()
except Exception as e:
    st.error(f"⚠️ مشكل فالساروت: {e}")
    st.stop()

# 3. واجهة التطبيق (ScanToSolve Style)
st.markdown('<div class="hero"><h1>👨‍🏫 LM3LM - لمعلم</h1><p style="color:white !important;">صور تمرينك.. وحدد المادة باش "لمعلم" يخرج ليك الحل ناضي</p></div>', unsafe_allow_html=True)

# اختيار المادة (لاكابلاج خدام)
st.markdown('<div style="max-width:900px; margin:0 auto; margin-bottom:10px;"><b>1. اختر المادة:</b></div>', unsafe_allow_html=True)
subject = st.radio(
    "المادة",
    ["📊 رياضيات", "⚛️ فيزياء", "🧪 كيمياء", "📚 أخرى"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# منطقة الرفع
st.markdown('<div style="max-width:900px; margin:0 auto; margin-bottom:10px;"><b>2. استيراد التمرين:</b></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين المرفوع", width=400)
    
    if st.button("يا لمعلم، عطيني الحل بوضوح", use_container_width=True):
        with st.spinner(f"لمعلم كيشوف فـ تمرين {subject}..."):
            try:
                model = genai.GenerativeModel(WORKING_MODEL)
                prompt_text = f"أنت 'لمعلم' خبير مغربي. اشرح هذا التمرين الخاص بمادة {subject} بالدارجة المغربية بأسلوب مبسط وواضح جدا. ابدأ دائما من اليمين واستعمل الخط العريض للنتائج."
                
                response = model.generate_content([prompt_text, img])
                
                # عرض الجواب فـ إطار ملكي
                st.markdown(f"""
                    <div class="answer-box">
                        <h2 style="color:#1e3c72; border-bottom: 2px solid #1e3c72; padding-bottom:10px;">💡 رد لمعلم ({subject}):</h2>
                        <div style="color: #000000 !important;">
                            {response.text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small style='color:black;'>Ibravolt Digital Solution - El Jadida 2026</small></center>", unsafe_allow_html=True)

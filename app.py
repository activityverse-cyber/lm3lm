import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. الستايل (RTL & High Contrast)
st.set_page_config(page_title="LM3LM Pro", page_icon="👨‍🏫", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Vazirmatn', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        color: #000000 !important;
    }
    .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white !important; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    
    /* ستايل باش نرجعو الراديو يبان بحال الكارويات */
    div[data-testid="stWidgetLabel"] { display: none; } /* إخفاء لابل الراديو */
    .st-emotion-cache-16idsys p { font-size: 1.1rem; font-weight: bold; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالساروت
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("⚠️ الساروت ناقص!")
    st.stop()

# 3. الواجهة
st.markdown('<div class="hero"><h1>👨‍🏫 LM3LM - لمعلم</h1><p style="color:white !important;">صور تمرينك.. وحدد المادة باش الجواب يكون دقيق</p></div>', unsafe_allow_html=True)

# --- هنا "لاكابلاج" الجديد ديال المواد ---
st.markdown('<div style="max-width:850px; margin:0 auto;"><b>1. اختر المادة (ضروري):</b></div>', unsafe_allow_html=True)

# استعملنا st.radio ودرنا ليه Horizontal باش يجي مستف
selected_subject = st.radio(
    "المادة",
    ["📊 رياضيات", "⚛️ فيزياء", "🧪 كيمياء", "📚 أخرى"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write(f"✅ المادة المختارة: **{selected_subject}**")
st.divider()

# 4. منطقة الرفع والحل
st.markdown('<div style="max-width:850px; margin:0 auto;"><b>2. استيراد التمرين:</b></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("upload", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="التمرين المرفوع", width=350)
    
    if st.button("يا لمعلم، عطيني الحل بوضوح", use_container_width=True):
        with st.spinner(f"لمعلم كيشوف فـ تمرين {selected_subject}..."):
            try:
                # دابا صيفطنا للموديل حتى المادة باش يعرف اشنو كيدير
                prompt_text = f"أنت 'لمعلم' خبير مغربي. اشرح هذا التمرين الخاص بمادة {selected_subject} بالدارجة المغربية بأسلوب مبسط. اجعل الخطوات واضحة جدا باللون الأسود. ابدأ من اليمين."
                
                response = model.generate_content([prompt_text, img])
                
                st.markdown(f"""
                    <div style="background-color: #ffffff; border-right: 8px solid #1e3c72; padding: 25px; border-radius: 15px; margin: 20px auto; max-width: 850px; color: #000000 !important; box-shadow: 0 10px 25px rgba(0,0,0,0.1); line-height: 1.8;">
                        <h2 style="color:#1e3c72; border-bottom: 2px solid #1e3c72; padding-bottom:10px;">💡 رد لمعلم ({selected_subject}):</h2>
                        <div style="font-size: 1.2rem; font-weight: 500; color: black !important;">
                        {response.text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"مشكل تقني: {e}")

st.markdown("<br><center><small style='color:black;'>Ibravolt Digital Solution - El Jadida 2026</small></center>", unsafe_allow_html=True)

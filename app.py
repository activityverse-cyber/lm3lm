import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# --- إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="مكنون OSTAD", page_icon="🎓", layout="centered")

# تصميم RTL متطور كيشبه الكود ديالك
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .gradient-hero {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #2563eb, #0ea5e9);
        color: white;
        border: none;
        padding: 0.75rem;
        font-weight: bold;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- إعداد Gemini API ---
API_KEY = "AIzaSyAwRhHWoBqwjFSbjtQmOcwD_55UOHZdY1w"
genai.configure(api_key=API_KEY)

# موجه النظام (System Prompt) - الالتزام التام بطلبك
SYSTEM_PROMPT = """
{  "system_prompt": "You are PROMPT-NEXUS-8.0, operating as 'Ustad Maghribi', an expert educational assistant for primary and secondary school students in Morocco... [أكمل هنا الموجه الذي قدمته بالكامل]"}
"""

# --- الواجهة (UI) ---
st.markdown('<div class="gradient-hero"><h1>م | مكنون OSTAD</h1><p>أستاذك الذكي - صوّر التمرين ديالك وأنا نشرحو ليك</p></div>', unsafe_allow_html=True)

# اختيار المادة (Subject Selector)
subject = st.selectbox("ختار المادة:", ["تلقائي (Auto)", "رياضيات", "فيزياء وكيمياء", "علوم الحياة والأرض", "لغة عربية", "لغة فرنسية"])

# رفع الصورة (Image Upload)
uploaded_file = st.file_uploader("ارفع صورة التمرين (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)
    
    if st.button("تحليل التمرين 🚀"):
        with st.spinner('صبر شوية، الأستاذ كيقرا 📖...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash') # أو gemini-2.0-flash إذا توفر
                response = model.generate_content(
                    [f"المادة المختارة: {subject}\n\n{SYSTEM_PROMPT}", image],
                    generation_config={"response_mime_type": "application/json"}
                )
                
                # استخراج البيانات
                res_data = json.loads(response.text)
                
                # --- عرض النتائج (ExplanationDisplay) ---
                st.balloons()
                st.markdown(f"### ✨ {res_data['lesson_title']}")
                st.success(res_data['encouragement_message'])
                
                with st.container():
                    st.markdown("#### 👨‍🏫 الشرح:")
                    st.info(res_data['pedagogical_explanation'])
                    
                    st.markdown("#### 📝 خطوات المساعدة:")
                    for step in res_data['example_solution_steps']:
                        st.markdown(f"✅ **{step['step_number']}:** {step['instruction']}")
                
                if res_data.get('terminology_notes'):
                    with st.expander("🔍 شرح المصطلحات"):
                        for term in res_data['terminology_notes']:
                            st.write(f"• **{term['term']}**: {term['explanation']}")
                
                st.markdown("---")
                st.warning(f"💡 **نصيحة الأستاذ:** {res_data['final_summary']}")

            except Exception as e:
                st.error("وقع خطأ فني. تأكد من جودة الصورة أو مفتاح API.")
                st.info(f"الخطأ: {str(e)}")

st.markdown('<p style="text-align:center; color:gray; font-size:12px;">مكنون OSTAD © 2026 — أستاذك الذكي</p>', unsafe_allow_html=True)

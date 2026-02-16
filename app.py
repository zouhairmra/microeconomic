import streamlit as st
from app_shared import rtl

st.set_page_config(
    page_title="الاقتصاد الجزئي | مسار عربي",
    page_icon="📘",
    layout="wide",
)

rtl()

st.title("📘 منصة تفاعلية لمبادئ الاقتصاد الجزئي")
st.caption("مسار عربي – موجّه لطلبة المرحلة الجامعية")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(
        """
        ## ماذا ستتعلم؟
        -  **الفصل 1:** تحديد التوازن في السوق وتحليل التحولات في العرض والطلب.
        -                    **الفصل 2:** حساب المرونات وتفسيرها اقتصاديًا.
        - **الفصل 3:** فهم التكاليف والإيرادات والربح وتعظيم الربح في المنافسة الكاملة.

        استخدم القائمة الجانبية للتنقّل بين الفصول.
        """
    )

with col2:
    st.info("💡 نصيحة: جرّب تحريك المنزلقات في كل فصل لرؤية الأثر على الرسوم والنتائج.")

st.markdown("---")
st.markdown(
    """
    ```bash
    git init
    git add .
    git commit -m "Initial commit: Microeconomics Arabic Streamlit module"
    git branch -M main
    git remote add origin https://github.com/<USER>/<REPO>.git
    git push -u origin main
    ```

    ثم انشر عبر Streamlit Community Cloud وحدّد `app.py` كملف التشغيل.
    """
)

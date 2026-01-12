import streamlit as st
import numpy as np

from app_shared import rtl

st.set_page_config(page_title="الفصل 2: المرونة", page_icon="🧮", layout="wide")
rtl()

st.title("🧮 الفصل 2: المرونة")

with st.expander("📌 ملخص نظري سريع", expanded=False):
    st.markdown(open("content/ch2.md", encoding="utf-8").read())

st.subheader("حاسبة المرونة السعرية للطلب (طريقة النقطة الوسطى)")

col1, col2 = st.columns(2)
with col1:
    P1 = st.number_input("السعر P1", value=10.0)
    Q1 = st.number_input("الكمية Q1", value=100.0)
with col2:
    P2 = st.number_input("السعر P2", value=12.0)
    Q2 = st.number_input("الكمية Q2", value=92.0)

pct_dQ = (Q2 - Q1) / ((Q1 + Q2) / 2) if (Q1 + Q2) != 0 else np.nan
pct_dP = (P2 - P1) / ((P1 + P2) / 2) if (P1 + P2) != 0 else np.nan
Ed = pct_dQ / pct_dP if pct_dP not in [0, np.nan] else np.nan

st.write(f"%ΔQ = {pct_dQ * 100:.2f}%")
st.write(f"%ΔP = {pct_dP * 100:.2f}%")
st.success(f"مرونة الطلب السعرية Ed = {Ed:.2f} (عادة سالبة)")

absEd = abs(Ed)
if absEd > 1:
    st.info("الطلب **مرن**")
elif absEd < 1:
    st.info("الطلب **غير مرن**")
else:
    st.info("**مرونة وحدية**")

st.markdown("---")
st.subheader("نشاط: الإيراد الكلي")
P = st.slider("السعر P", 1.0, 50.0, 10.0, 0.5)
Q = st.slider("الكمية Q", 1.0, 500.0, 100.0, 1.0)
st.metric("الإيراد الكلي TR", f"{(P * Q):,.2f}")

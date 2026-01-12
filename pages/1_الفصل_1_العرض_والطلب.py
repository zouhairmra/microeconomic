import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from app_shared import rtl

st.set_page_config(page_title="الفصل 1: العرض والطلب", page_icon="📈", layout="wide")
rtl()

st.title("📈 الفصل 1: العرض والطلب")

with st.expander("📌 ملخص نظري سريع", expanded=False):
    st.markdown(open("content/ch1.md", encoding="utf-8").read())

st.subheader("أداة تفاعلية: توازن السوق (نماذج خطية)")

colA, colB = st.columns(2)
with colA:
    st.markdown("### إعدادات الطلب:  Qd = a - bP")
    a = st.slider("a (مقطع الطلب)", 10.0, 200.0, 120.0, 1.0)
    b = st.slider("b (ميل الطلب)", 0.1, 5.0, 1.0, 0.1)

with colB:
    st.markdown("### إعدادات العرض:  Qs = c + dP")
    c = st.slider("c (مقطع العرض)", -50.0, 150.0, 10.0, 1.0)
    d = st.slider("d (ميل العرض)", 0.1, 5.0, 1.2, 0.1)

P_star = (a - c) / (b + d)
Q_star = a - b * P_star

st.success(f"السعر التوازني P* = {P_star:.2f} | الكمية التوازنية Q* = {Q_star:.2f}")

P = np.linspace(0, max(1, P_star * 2, 50), 200)
Qd = a - b * P
Qs = c + d * P

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(Qd, P, label="الطلب (Qd)")
ax.plot(Qs, P, label="العرض (Qs)")
ax.scatter([Q_star], [P_star], zorder=5)
ax.annotate("التوازن", (Q_star, P_star), textcoords="offset points", xytext=(10, 10))
ax.set_xlabel("الكمية Q")
ax.set_ylabel("السعر P")
ax.set_title("توازن السوق")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

st.markdown("---")
st.subheader("تحولات بسيطة")
st.caption("غيّر a أو c لمحاكاة انتقال الطلب أو العرض.")

quiz = st.radio(
    "سؤال سريع: إذا ارتفع الطلب وبقي العرض ثابتاً، ماذا يحدث للسعر التوازني؟",
    ["ينخفض", "يرتفع", "لا يتغير"],
    index=1,
)
if quiz == "يرتفع":
    st.write("✅ صحيح")
else:
    st.write("❌ الصحيح: يرتفع")

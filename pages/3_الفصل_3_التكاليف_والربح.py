import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from app_shared import rtl

st.set_page_config(page_title="الفصل 3: التكاليف والربح", page_icon="🏭", layout="wide")
rtl()

st.title("🏭 الفصل 3: الإنتاج، التكاليف، والربح")

with st.expander("📌 ملخص نظري سريع", expanded=False):
    st.markdown(open("content/ch3.md", encoding="utf-8").read())

st.subheader("نموذج مبسّط للتكلفة:  TC(Q) = FC + αQ + βQ²")

col1, col2, col3 = st.columns(3)
with col1:
    FC = st.number_input("التكلفة الثابتة FC", value=200.0, min_value=0.0)
with col2:
    alpha = st.number_input("α", value=10.0, min_value=0.0)
with col3:
    beta = st.number_input("β", value=0.5, min_value=0.0)

P = st.number_input("السعر السوقي P (منافسة كاملة)", value=25.0, min_value=0.0)

Q_star = (P - alpha) / (2 * beta) if beta > 0 else 0
Q_star = max(0.0, Q_star)

Q = np.linspace(0, max(1, Q_star * 2, 60), 200)
TC = FC + alpha * Q + beta * (Q ** 2)
TR = P * Q
pi = TR - TC

VC = alpha * Q + beta * (Q ** 2)
AVC = np.divide(VC, Q, out=np.zeros_like(Q), where=Q > 0)
min_avc = float(AVC[Q > 0].min()) if (Q > 0).any() else 0.0

st.success(f"الكمية التي تعظم الربح تقريباً: Q* = {Q_star:.2f}")

TC_star = FC + alpha * Q_star + beta * (Q_star ** 2)
TR_star = P * Q_star
pi_star = TR_star - TC_star

c1, c2, c3 = st.columns(3)
c1.metric("TR عند Q*", f"{TR_star:,.2f}")
c2.metric("TC عند Q*", f"{TC_star:,.2f}")
c3.metric("الربح π عند Q*", f"{pi_star:,.2f}")

if P < min_avc:
    st.warning(f"قد يكون الإغلاق أفضل: P < min(AVC) ≈ {min_avc:.2f}")
else:
    st.info(f"الإنتاج ممكن: P ≥ min(AVC) ≈ {min_avc:.2f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(Q, TR, label="TR")
ax.plot(Q, TC, label="TC")
ax.plot(Q, pi, label="الربح π")
ax.axvline(Q_star, linestyle="--", alpha=0.6)
ax.set_xlabel("الكمية Q")
ax.set_ylabel("القيمة")
ax.set_title("TR, TC, والربح")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

st.markdown("---")
ans = st.radio("شرط تعظيم الربح في المنافسة الكاملة:", ["MR = MC", "P = ATC", "MC = AVC"], index=0)
if ans == "MR = MC":
    st.write("✅ صحيح")
else:
    st.write("❌ الصحيح: MR = MC")

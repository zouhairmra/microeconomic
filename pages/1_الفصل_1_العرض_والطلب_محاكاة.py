import streamlit as st
import numpy as np
import plotly.graph_objects as go

from app_shared import rtl

st.set_page_config(page_title="الفصل 1: العرض والطلب (محاكاة)", page_icon="📈", layout="wide")
rtl()

st.title("📈 الفصل 1: العرض والطلب — محاكاة انتقال المنحنيات")

with st.expander("📌 ملخص نظري سريع", expanded=False):
    st.markdown(open("content/ch1.md", encoding="utf-8").read())

st.subheader("المحاكاة")
st.caption("اختر عاملًا وحدّد اتجاهه وحجمه، ثم شاهد كيف تنتقل المنحنيات (Shift). لا نعرض معادلات الطلب/العرض — فقط الحركة.")

# --- Baseline curves (defined as points; we do not display any formula) ---
Q = np.linspace(0, 100, 101)

# Demand baseline: downward sloping line in (Q,P) space
P_d0 = 90 - 0.6 * Q

# Supply baseline: upward sloping
P_s0 = 10 + 0.6 * Q

# Keep within plot range
P_d0 = np.clip(P_d0, 0, 100)
P_s0 = np.clip(P_s0, 0, 100)

# --- Choose shock ---
shock_type = st.selectbox(
    "اختر نوع العامل:",
    [
        "(طلب) الدخل (سلعة عادية)",
        "(طلب) الدخل (سلعة رديئة)",
        "(طلب) سعر السلعة البديلة",
        "(طلب) سعر السلعة المكملة",
        "(طلب) عدد المشترين",
        "(طلب) التفضيلات/الإعلان",
        "(عرض) تكلفة المدخلات",
        "(عرض) التكنولوجيا/الإنتاجية",
        "(عرض) عدد البائعين",
        "(عرض) ضريبة/إعانة",
    ],
)

direction = st.radio("الاتجاه:", ["زيادة", "انخفاض"], horizontal=True)
magnitude = st.slider("حجم الصدمة (قوة الانتقال)", 0.0, 30.0, 12.0, 1.0)

st.markdown("---")
colA, colB = st.columns([1, 1])
with colA:
    steps = st.slider("عدد خطوات الحركة (لنعومة الأنيميشن)", 5, 40, 20, 1)
with colB:
    show_final = st.checkbox("إظهار المنحنى النهائي كخط متقطع أيضاً", value=True)

# Determine shift direction: +Q shift means curve moves right (more Q at any P)
# We'll implement shift as horizontal translation in Q, which visually shifts curve.
# For demand: right shift => higher Q at same P => in (Q,P), curve moves right.
# For supply: right shift => more supplied at any P => curve moves right.

sign = 1 if direction == "زيادة" else -1

# Map shocks to whether they shift demand or supply and which direction
# For each factor, define effect of 'زيادة'. For 'انخفاض' we invert via sign.

# effect: +1 means right shift for increase; -1 means left shift for increase
EFFECT = {
    "(طلب) الدخل (سلعة عادية)": +1,
    "(طلب) الدخل (سلعة رديئة)": -1,
    "(طلب) سعر السلعة البديلة": +1,
    "(طلب) سعر السلعة المكملة": -1,
    "(طلب) عدد المشترين": +1,
    "(طلب) التفضيلات/الإعلان": +1,
    "(عرض) تكلفة المدخلات": -1,
    "(عرض) التكنولوجيا/الإنتاجية": +1,
    "(عرض) عدد البائعين": +1,
    "(عرض) ضريبة/إعانة": -1,  # treat as tax increase; if you choose "انخفاض" it becomes subsidy
}

is_demand = shock_type.startswith("(طلب)")
base_effect = EFFECT[shock_type]
shift_Q_final = magnitude * base_effect * sign

# Build frames
frames = []
for i in range(steps + 1):
    t = i / steps
    shift_Q = t * shift_Q_final

    if is_demand:
        Qd = Q + shift_Q
        Pd = P_d0
        Qs = Q
        Ps = P_s0
    else:
        Qd = Q
        Pd = P_d0
        Qs = Q + shift_Q
        Ps = P_s0

    frames.append(
        go.Frame(
            data=[
                go.Scatter(x=Qd, y=Pd, mode="lines", name="الطلب D"),
                go.Scatter(x=Qs, y=Ps, mode="lines", name="العرض S"),
            ],
            name=f"f{i}",
        )
    )

# Initial data
init = frames[0].data

fig = go.Figure(data=init, frames=frames)

# Optional: add final dashed curve
if show_final and magnitude > 0:
    if is_demand:
        fig.add_trace(
            go.Scatter(
                x=Q + shift_Q_final,
                y=P_d0,
                mode="lines",
                name="الطلب بعد الصدمة",
                line=dict(dash="dash"),
                opacity=0.7,
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=Q + shift_Q_final,
                y=P_s0,
                mode="lines",
                name="العرض بعد الصدمة",
                line=dict(dash="dash"),
                opacity=0.7,
            )
        )

# Layout + animation buttons
fig.update_layout(
    title="انتقال منحنيات العرض والطلب",
    xaxis_title="الكمية Q",
    yaxis_title="السعر P",
    xaxis=dict(range=[-20, 140]),
    yaxis=dict(range=[0, 100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=60, b=40),
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.0,
            y=1.15,
            buttons=[
                dict(
                    label="▶ تشغيل",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 60, "redraw": True},
                            "transition": {"duration": 0},
                            "fromcurrent": True,
                            "mode": "immediate",
                        },
                    ],
                ),
                dict(
                    label="⏸ إيقاف",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                ),
                dict(
                    label="⟲ إعادة",
                    method="animate",
                    args=[["f0"], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                ),
            ],
        )
    ],
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("تفسير سريع")
if magnitude == 0:
    st.info("اختر حجم صدمة أكبر من صفر لمشاهدة انتقال المنحنى.")
else:
    target = "الطلب" if is_demand else "العرض"
    if shift_Q_final > 0:
        st.success(f"هذه الصدمة تُحرك منحنى **{target}** إلى **اليمين** (زيادة الكمية عند كل سعر).")
    else:
        st.warning(f"هذه الصدمة تُحرك منحنى **{target}** إلى **اليسار** (انخفاض الكمية عند كل سعر).")

st.caption("ملاحظة تعليمية: هذه محاكاة بصريّة للتغيّر في العوامل غير السعرية. لا يعني ذلك أن شكل المنحنى الحقيقي دائمًا خطي.")

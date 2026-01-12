import streamlit as st


def rtl():
    """Apply basic RTL (right-to-left) styling for Arabic UI."""
    st.markdown(
        """
        <style>
          html, body, [class*="css"]  { direction: rtl; text-align: right; }
          .stMarkdown, .stText, .stTextInput, .stSelectbox, .stSlider { direction: rtl; }
          h1, h2, h3, h4 { text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )

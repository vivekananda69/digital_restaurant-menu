# ============================================================
#  RESTAURANT DIGITAL QR MENU BUILDER
#  app.py — Main Entry Point & Home Page
# ============================================================

import streamlit as st
from pathlib import Path


# ── 1. PAGE CONFIGURATION ────────────────────────────────────
# This MUST be the first Streamlit command in the entire app.
# It sets the browser tab title, icon, and layout width.
st.set_page_config(
    page_title="QR Menu Builder",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── 2. LOAD CUSTOM CSS ────────────────────────────────────────
# We read our CSS file and inject it into the Streamlit page.
# This is how we apply our premium dark theme.
def load_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── 3. SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🍽️ QR Menu Builder")
    st.markdown("---")
    st.markdown(
        """
        <div style='font-family: Inter, sans-serif; font-size: 0.85rem;
                    color: #A0A0B0; line-height: 1.8;'>
        📌 <b style='color:#C8A96E'>Home</b> — You are here<br><br>
        🛠️ <b style='color:#C8A96E'>Admin Panel</b> — Build your menu<br><br>
        👁️ <b style='color:#C8A96E'>Customer Menu</b> — Preview customer view
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        """
        <div style='font-family: Inter, sans-serif; font-size: 0.75rem;
                    color: #606070; text-align: center;'>
        Built with ❤️ using Streamlit<br>
        Restaurant QR Menu Builder v1.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── 4. HERO SECTION ───────────────────────────────────────────
st.markdown(
    """
    <div class='hero-banner'>
        <div class='hero-title'>🍽️ QR Menu Builder</div>
        <div class='hero-subtitle'>
            Create beautiful digital menus • Generate QR codes • Delight your customers
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── 5. FEATURE CARDS ROW ──────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class='feature-card'>
            <span class='feature-icon'>🏪</span>
            <div class='feature-title'>Brand Your Restaurant</div>
            <div class='feature-desc'>Upload your logo and set your restaurant name for a personalised menu.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class='feature-card'>
            <span class='feature-icon'>🍜</span>
            <div class='feature-title'>Build Your Menu</div>
            <div class='feature-desc'>Add categories, items, prices, descriptions, and beautiful food photos.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class='feature-card'>
            <span class='feature-icon'>👁️</span>
            <div class='feature-title'>Preview Live</div>
            <div class='feature-desc'>See exactly how your customers will experience the digital menu.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class='feature-card'>
            <span class='feature-icon'>📱</span>
            <div class='feature-title'>Generate QR Code</div>
            <div class='feature-desc'>One click to generate and download your scannable QR code.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── 6. DIVIDER ────────────────────────────────────────────────
st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)


# ── 7. HOW IT WORKS SECTION ───────────────────────────────────
st.markdown(
    "<div class='section-header'>⚡ How It Works</div>",
    unsafe_allow_html=True,
)

step1, step2, step3, step4 = st.columns(4)

steps = [
    ("01", "Go to Admin Panel", "Use the sidebar to navigate to the Admin Panel page."),
    ("02", "Build Your Menu",   "Add your restaurant info, categories, and menu items."),
    ("03", "Preview Menu",      "Check the Customer Menu page to see how it looks."),
    ("04", "Get QR Code",       "Generate and download your QR code from the Admin Panel."),
]

for col, (number, title, desc) in zip([step1, step2, step3, step4], steps):
    with col:
        st.markdown(
            f"""
            <div class='feature-card'>
                <div style='font-family: Playfair Display, serif;
                            font-size: 2.5rem; color: rgba(200,169,110,0.3);
                            font-weight: 700; margin-bottom: 0.5rem;'>
                    {number}
                </div>
                <div class='feature-title'>{title}</div>
                <div class='feature-desc'>{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── 8. DIVIDER ────────────────────────────────────────────────
st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)


# ── 9. CALL TO ACTION ─────────────────────────────────────────
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-family: Playfair Display, serif;
                    font-size: 1.6rem; color: #C8A96E; margin-bottom: 0.8rem;'>
            Ready to build your digital menu?
        </div>
        <div style='font-family: Inter, sans-serif;
                    font-size: 1rem; color: #A0A0B0;'>
            👈 Click <b style='color:#C8A96E'>Admin Panel</b> in the sidebar to get started
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
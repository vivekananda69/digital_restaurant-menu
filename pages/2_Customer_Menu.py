# ============================================================
#  pages/2_Customer_Menu.py
#  Customer-facing digital menu — read-only, premium UI
#  Polished version with improved food cards and layout
# ============================================================

import streamlit as st
from pathlib import Path
import base64

from storage.menu_store import (
    get_restaurant,
    get_categories,
    get_items_by_category,
    get_all_items,
)


# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Menu",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── Load CSS ──────────────────────────────────────────────────
def load_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── Extra CSS for Customer Page ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

[data-testid="collapsedControl"] { display: none; }
[data-testid="stSidebar"]        { display: none; }

.restaurant-header {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%);
    border: 1px solid rgba(200,169,110,0.25);
    border-radius: 24px;
    padding: 3rem 2rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
}
.restaurant-name-big {
    font-family: "Playfair Display", serif;
    font-size: 2.8rem;
    color: #C8A96E;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
}
.restaurant-tagline-big {
    font-family: "Inter", sans-serif;
    font-size: 1rem;
    color: #A0A0B0;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.stats-row {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 1rem;
}
.stat-pill {
    font-family: "Inter", sans-serif;
    font-size: 0.8rem;
    color: #606070;
    text-align: center;
}
.stat-pill-num {
    font-family: "Playfair Display", serif;
    font-size: 1.4rem;
    color: #C8A96E;
    font-weight: 700;
    display: block;
}
.cat-title {
    font-family: "Playfair Display", serif;
    font-size: 1.7rem;
    color: #C8A96E;
    font-weight: 700;
    padding: 0.5rem 0;
    margin: 2rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(200,169,110,0.2);
}
.food-card-wrap {
    background: linear-gradient(145deg, #16213E, #1A1A2E);
    border: 1px solid rgba(200,169,110,0.15);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
    height: 100%;
}
.food-card-wrap:hover {
    border-color: rgba(200,169,110,0.5);
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
}
.food-img-placeholder {
    width: 100%;
    height: 175px;
    background: linear-gradient(135deg, #0F3460 0%, #16213E 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;
}
.food-body {
    padding: 1.1rem 1.2rem 1.3rem 1.2rem;
}
.food-name {
    font-family: "Playfair Display", serif;
    font-size: 1.1rem;
    color: #F0F0F0;
    font-weight: 600;
    margin-bottom: 0.35rem;
    line-height: 1.35;
}
.food-desc {
    font-family: "Inter", sans-serif;
    font-size: 0.8rem;
    color: #7A7A8A;
    line-height: 1.65;
    margin-bottom: 0.9rem;
    min-height: 3rem;
}
.food-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 0.6rem;
    border-top: 1px solid rgba(200,169,110,0.1);
}
.food-price {
    font-family: "Inter", sans-serif;
    font-size: 1.25rem;
    color: #C8A96E;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-avail {
    background: rgba(76,175,130,0.12);
    border: 1px solid rgba(76,175,130,0.35);
    color: #4CAF82;
    font-family: "Inter", sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.22rem 0.65rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.filter-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    margin-bottom: 2rem;
}
.page-footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    margin-top: 1rem;
}
.page-footer-name {
    font-family: "Playfair Display", serif;
    font-size: 1.2rem;
    color: rgba(200,169,110,0.6);
    margin-bottom: 0.3rem;
}
.page-footer-sub {
    font-family: "Inter", sans-serif;
    font-size: 0.72rem;
    color: #303040;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
}
.empty-state-icon { font-size: 4rem; margin-bottom: 1rem; }
.empty-state-title {
    font-family: "Playfair Display", serif;
    font-size: 1.8rem;
    color: #C8A96E;
    margin-bottom: 0.6rem;
}
.empty-state-sub {
    font-family: "Inter", sans-serif;
    font-size: 0.9rem;
    color: #505060;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: image → base64 for inline HTML ────────────────────
def img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lstrip(".").lower()
    ext = "jpeg" if ext == "jpg" else ext
    return f"data:image/{ext};base64,{data}"


# ── Load Data ─────────────────────────────────────────────────
restaurant = get_restaurant()
categories = get_categories()
all_items  = get_all_items()

r_name    = restaurant.get("name",            "Our Restaurant")
r_tagline = restaurant.get("tagline",         "")
r_logo    = restaurant.get("logo_path",       "")
currency  = restaurant.get("currency_symbol", "₹")

avail_items = [i for i in all_items if i.get("available", True)]


# ── Empty state — menu not built yet ─────────────────────────
if not categories and not all_items:
    st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>🍽️</div>
            <div class='empty-state-title'>Menu Coming Soon</div>
            <div class='empty-state-sub'>
                The restaurant is still preparing this menu.<br>
                Please check back soon.
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Restaurant Header ─────────────────────────────────────────
# Logo (rendered via st.image above the HTML block)
if r_logo and Path(r_logo).exists():
    lc1, lc2, lc3 = st.columns([2, 1, 2])
    with lc2:
        st.image(r_logo, width=110)

tagline_html = (
    f"<div class='restaurant-tagline-big'>{r_tagline}</div>"
    if r_tagline else ""
)

st.markdown(f"""
    <div class='restaurant-header'>
        <div class='restaurant-name-big'>{r_name}</div>
        {tagline_html}
        <div class='stats-row'>
            <div class='stat-pill'>
                <span class='stat-pill-num'>{len(categories)}</span>
                Categories
            </div>
            <div class='stat-pill'>
                <span class='stat-pill-num'>{len(avail_items)}</span>
                Dishes Available
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ── Category Filter ───────────────────────────────────────────
if "sel_cat" not in st.session_state:
    st.session_state["sel_cat"] = "ALL"

filter_options = ["ALL"] + categories
num_filters    = len(filter_options)
filter_cols    = st.columns(num_filters)

for i, opt in enumerate(filter_options):
    with filter_cols[i]:
        label     = "🍽️ All" if opt == "ALL" else opt
        is_active = st.session_state["sel_cat"] == opt
        btn_style = (
            "background:linear-gradient(135deg,#C8A96E,#A8894E);"
            "color:#1A1A2E;font-weight:700;border:none;"
            "border-radius:25px;padding:0.4rem 0.5rem;"
            "font-family:Inter,sans-serif;font-size:0.82rem;"
            "width:100%;cursor:pointer;"
        ) if is_active else (
            "background:transparent;color:#C8A96E;"
            "border:1px solid rgba(200,169,110,0.35);"
            "border-radius:25px;padding:0.4rem 0.5rem;"
            "font-family:Inter,sans-serif;font-size:0.82rem;"
            "width:100%;cursor:pointer;"
        )
        if st.button(label, key=f"flt_{i}", use_container_width=True):
            st.session_state["sel_cat"] = opt
            st.rerun()

st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)


# ── Render Menu Items ─────────────────────────────────────────
selected        = st.session_state["sel_cat"]
cats_to_display = categories if selected == "ALL" else [selected]
any_shown       = False

for cat in cats_to_display:
    cat_items = [
        i for i in get_items_by_category(cat)
        if i.get("available", True)
    ]
    if not cat_items:
        continue

    any_shown = True

    # Category heading
    st.markdown(
        f"<div class='cat-title'>✦ &nbsp;{cat}</div>",
        unsafe_allow_html=True,
    )

    # 3-column grid
    cols_per_row = 3
    rows = [
        cat_items[i:i + cols_per_row]
        for i in range(0, len(cat_items), cols_per_row)
    ]

    for row in rows:
        grid = st.columns(cols_per_row, gap="medium")
        for col_idx, item in enumerate(row):
            with grid[col_idx]:
                # ── Build card HTML ───────────────────────────
                img_path = item.get("image_path", "")

                # Image section
                if img_path and Path(img_path).exists():
                    b64_src = img_to_base64(img_path)
                    img_html = (
                        f"<img src='{b64_src}' "
                        f"style='width:100%;height:175px;"
                        f"object-fit:cover;display:block;'>"
                    )
                else:
                    img_html = "<div class='food-img-placeholder'>🍴</div>"

                # Description — truncate for card
                desc      = item.get("description", "")
                short_desc = (desc[:88] + "…") if len(desc) > 88 else desc
                if not short_desc:
                    short_desc = "A delicious dish crafted with care."

                price_str = f"{currency}{item.get('price', 0):.2f}"

                card_html = f"""
                <div class='food-card-wrap'>
                    {img_html}
                    <div class='food-body'>
                        <div class='food-name'>{item.get('name','')}</div>
                        <div class='food-desc'>{short_desc}</div>
                        <div class='food-footer'>
                            <div class='food-price'>{price_str}</div>
                            <span class='badge-avail'>✓ Available</span>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ── No items in selected category ────────────────────────────
if not any_shown:
    st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>🔍</div>
            <div class='empty-state-title'>Nothing Here Yet</div>
            <div class='empty-state-sub'>
                No available dishes in this category right now.
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── Page Footer ───────────────────────────────────────────────
st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
    <div class='page-footer'>
        <div class='page-footer-name'>{r_name}</div>
        <div class='page-footer-sub'>
            Digital Menu &nbsp;•&nbsp; Powered by QR Menu Builder
        </div>
    </div>
""", unsafe_allow_html=True)
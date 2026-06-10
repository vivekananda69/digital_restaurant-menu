# ============================================================
#  pages/1_Admin_Panel.py
#  Restaurant Owner's Control Panel — FIXED VERSION
#  Tabs: Restaurant Info | Categories | Menu Items | QR Code
# ============================================================

import streamlit as st
from pathlib import Path
import io
import qrcode
import base64

from storage.menu_store import (
    get_restaurant, save_restaurant, save_logo,
    get_categories, add_category, delete_category,
    get_all_items, get_items_by_category,
    add_item, update_item, delete_item, toggle_availability,
    get_stats,
)


# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Admin Panel — QR Menu Builder",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Load CSS ──────────────────────────────────────────────────
def load_css():
    css_path = Path("assets/styles.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠️ Admin Panel")
    st.markdown("---")
    stats = get_stats()
    st.markdown(
        f"""
        <div style='font-family:Inter,sans-serif;'>
            <div class='stat-box' style='margin-bottom:0.8rem;'>
                <div class='stat-number'>{stats['total_categories']}</div>
                <div class='stat-label'>Categories</div>
            </div>
            <div class='stat-box' style='margin-bottom:0.8rem;'>
                <div class='stat-number'>{stats['total_items']}</div>
                <div class='stat-label'>Menu Items</div>
            </div>
            <div class='stat-box'>
                <div class='stat-number'>{stats['available_items']}</div>
                <div class='stat-label'>Available</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    restaurant = get_restaurant()
    rname = restaurant.get("name", "")
    if rname:
        st.markdown(
            f"<div style='text-align:center;color:#C8A96E;"
            f"font-family:Playfair Display,serif;font-size:1rem;"
            f"font-weight:600;'>{rname}</div>",
            unsafe_allow_html=True,
        )


# ── Page Header ───────────────────────────────────────────────
st.markdown(
    "<div class='hero-banner' style='padding:2rem;'>"
    "<div class='hero-title' style='font-size:2rem;'>🛠️ Admin Panel</div>"
    "<div class='hero-subtitle'>Manage your restaurant menu from one place</div>"
    "</div>",
    unsafe_allow_html=True,
)


# ── Four Tabs ─────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏪 Restaurant Info",
    "📂 Categories",
    "🍜 Menu Items",
    "📱 QR Code",
])


# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 1 — RESTAURANT INFO                                ║
# ╚══════════════════════════════════════════════════════════╝
with tab1:
    st.markdown(
        "<div class='section-header'>🏪 Restaurant Information</div>",
        unsafe_allow_html=True,
    )

    restaurant = get_restaurant()
    col_form, col_preview = st.columns([3, 2], gap="large")

    with col_form:
        st.markdown("#### ✏️ Basic Details")

        r_name = st.text_input(
            "Restaurant Name *",
            value=restaurant.get("name", ""),
            placeholder="e.g. The Golden Fork",
        )
        r_tagline = st.text_input(
            "Tagline / Slogan",
            value=restaurant.get("tagline", ""),
            placeholder="e.g. Fine Dining Experience",
        )

        currency_options = ["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)", "¥ (JPY)", "د.إ (AED)"]
        current_symbol   = restaurant.get("currency_symbol", "₹")
        symbol_map       = {"₹": 0, "$": 1, "€": 2, "£": 3, "¥": 4, "د.إ": 5}
        default_index    = symbol_map.get(current_symbol, 0)

        r_currency = st.selectbox(
            "Currency",
            currency_options,
            index=default_index,
        )
        currency_symbol = r_currency.split(" ")[0]

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Restaurant Info", use_container_width=True):
            if not r_name.strip():
                st.error("❌ Restaurant name is required.")
            else:
                save_restaurant(r_name, r_tagline, currency_symbol)
                st.success(f"✅ Restaurant info saved for '{r_name}'!")
                st.rerun()

    with col_preview:
        st.markdown("#### 🖼️ Restaurant Logo")

        logo_path = restaurant.get("logo_path", "")
        if logo_path and Path(logo_path).exists():
            st.image(logo_path, width=200, caption="Current Logo")
        else:
            st.markdown(
                """
                <div style='background:#16213E;border:2px dashed rgba(200,169,110,0.3);
                border-radius:12px;padding:2rem;text-align:center;color:#606070;
                font-family:Inter,sans-serif;font-size:0.9rem;'>
                    📷<br>No logo uploaded yet
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_logo = st.file_uploader(
            "Upload Logo",
            type=["png", "jpg", "jpeg", "webp"],
            help="Recommended: square image, at least 200×200px",
        )
        if uploaded_logo is not None:
            if st.button("📤 Upload Logo", use_container_width=True):
                save_logo(uploaded_logo)
                st.success("✅ Logo uploaded successfully!")
                st.rerun()

    # ── Preview Card ──────────────────────────────────────────
    st.markdown("<div class='premium-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 👁️ Current Restaurant Card Preview")

    restaurant    = get_restaurant()
    preview_name    = restaurant.get("name",    "Your Restaurant Name")
    preview_tagline = restaurant.get("tagline", "Your Tagline Here")
    preview_logo    = restaurant.get("logo_path", "")

    pcol1, pcol2, pcol3 = st.columns([1, 3, 1])
    with pcol2:
        if preview_logo and Path(preview_logo).exists():
            lc1, lc2, lc3 = st.columns([2, 1, 2])
            with lc2:
                st.image(preview_logo, width=80)

        st.markdown(
            f"""
            <div style='background:linear-gradient(135deg,#16213E,#1A1A2E);
                        border:1px solid rgba(200,169,110,0.3);border-radius:16px;
                        padding:2rem;text-align:center;'>
                <div style='font-family:"Playfair Display",serif;font-size:1.6rem;
                            color:#C8A96E;font-weight:700;margin-bottom:0.4rem;'>
                    {preview_name or "Your Restaurant Name"}
                </div>
                <div style='font-family:"Inter",sans-serif;font-size:0.9rem;
                            color:#A0A0B0;'>
                    {preview_tagline or "Your tagline appears here"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 2 — CATEGORIES                                     ║
# ╚══════════════════════════════════════════════════════════╝
with tab2:
    st.markdown(
        "<div class='section-header'>📂 Category Management</div>",
        unsafe_allow_html=True,
    )

    col_add, col_list = st.columns([2, 3], gap="large")

    with col_add:
        st.markdown("#### ➕ Add New Category")
        st.markdown(
            "<div style='font-family:Inter,sans-serif;font-size:0.85rem;"
            "color:#A0A0B0;margin-bottom:1rem;'>Categories group your menu items "
            "(e.g. Starters, Mains, Desserts, Drinks)</div>",
            unsafe_allow_html=True,
        )

        new_cat = st.text_input(
            "Category Name",
            placeholder="e.g. Starters",
            key="new_category_input",
        )

        st.markdown(
            "<div style='font-family:Inter,sans-serif;font-size:0.8rem;"
            "color:#A0A0B0;margin-bottom:0.5rem;'>Quick suggestions:</div>",
            unsafe_allow_html=True,
        )
        suggestions = ["Starters", "Main Course", "Desserts",
                       "Beverages", "Specials", "Snacks"]
        existing    = get_categories()
        sug_cols    = st.columns(3)
        for idx, sug in enumerate(suggestions):
            with sug_cols[idx % 3]:
                if st.button(
                    sug,
                    key=f"sug_{sug}",
                    disabled=(sug in existing),
                    use_container_width=True,
                ):
                    ok, msg = add_category(sug)
                    if ok:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Category", use_container_width=True, key="add_cat_btn"):
            if new_cat.strip():
                ok, msg = add_category(new_cat)
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
            else:
                st.warning("⚠️ Please enter a category name.")

    with col_list:
        st.markdown("#### 📋 Existing Categories")
        categories = get_categories()

        if not categories:
            st.markdown(
                """
                <div style='background:#16213E;border:2px dashed rgba(200,169,110,0.2);
                border-radius:12px;padding:2rem;text-align:center;
                color:#606070;font-family:Inter,sans-serif;'>
                    📂 No categories yet.<br>Add your first category on the left.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for cat in categories:
                item_count = len(get_items_by_category(cat))
                c1, c2, c3 = st.columns([4, 2, 1])
                with c1:
                    st.markdown(
                        f"""
                        <div style='background:#16213E;border:1px solid rgba(200,169,110,0.2);
                        border-radius:10px;padding:0.8rem 1rem;'>
                            <span style='font-family:"Playfair Display",serif;
                                         font-size:1rem;color:#F5F5F5;'>{cat}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        f"<div style='padding:0.8rem 0;font-family:Inter,sans-serif;"
                        f"font-size:0.85rem;color:#A0A0B0;'>"
                        f"🍽️ {item_count} item{'s' if item_count != 1 else ''}</div>",
                        unsafe_allow_html=True,
                    )
                with c3:
                    if st.button("🗑️", key=f"del_cat_{cat}",
                                 help=f"Delete {cat}"):
                        ok, msg = delete_category(cat)
                        if ok:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
                        st.rerun()

            st.markdown(
                f"<div style='font-family:Inter,sans-serif;font-size:0.85rem;"
                f"color:#A0A0B0;margin-top:1rem;'>Total: {len(categories)} "
                f"categor{'ies' if len(categories)!=1 else 'y'}</div>",
                unsafe_allow_html=True,
            )


# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 3 — MENU ITEMS                                     ║
# ╚══════════════════════════════════════════════════════════╝
with tab3:
    st.markdown(
        "<div class='section-header'>🍜 Menu Item Management</div>",
        unsafe_allow_html=True,
    )

    categories = get_categories()

    if not categories:
        st.warning("⚠️ Please add at least one category in the "
                   "**Categories** tab before adding menu items.")
    else:
        # ── Add New Item Form ─────────────────────────────────
        with st.expander("➕ Add New Menu Item", expanded=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                new_item_name  = st.text_input(
                    "Item Name *", placeholder="e.g. Paneer Tikka",
                    key="new_item_name")
                new_item_cat   = st.selectbox(
                    "Category *", categories, key="new_item_cat")
                new_item_price = st.number_input(
                    "Price *", min_value=0.0, step=0.5,
                    format="%.2f", key="new_item_price")
            with fc2:
                new_item_desc = st.text_area(
                    "Description",
                    placeholder="Describe the dish...",
                    height=120, key="new_item_desc")
                new_item_img  = st.file_uploader(
                    "Food Image (optional)",
                    type=["png","jpg","jpeg","webp"],
                    key="new_item_img")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Add Item to Menu",
                         use_container_width=True, key="add_item_btn"):
                ok, msg = add_item(
                    name        = new_item_name,
                    category    = new_item_cat,
                    price       = new_item_price,
                    description = new_item_desc,
                    image_file  = new_item_img,
                )
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        st.markdown("<div class='premium-divider'></div>",
                    unsafe_allow_html=True)

        # ── Display Items ─────────────────────────────────────
        st.markdown("#### 📋 All Menu Items")

        all_items  = get_all_items()
        restaurant = get_restaurant()
        currency   = restaurant.get("currency_symbol", "₹")

        if not all_items:
            st.markdown(
                """
                <div style='background:#16213E;border:2px dashed rgba(200,169,110,0.2);
                border-radius:12px;padding:2rem;text-align:center;
                color:#606070;font-family:Inter,sans-serif;'>
                    🍽️ No menu items yet. Add your first item above.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # ── CRITICAL FIX: use a global counter for all keys ──
            # This guarantees every widget key is unique across
            # all items and all categories on the page.
            widget_counter = 0

            for cat in categories:
                cat_items = get_items_by_category(cat)
                if not cat_items:
                    continue

                st.markdown(
                    f"<div class='category-badge'>"
                    f"📂 {cat} — {len(cat_items)} item(s)</div>",
                    unsafe_allow_html=True,
                )

                for item in cat_items:
                    # Each item gets its own unique counter value
                    widget_counter += 1
                    wc = widget_counter          # shorthand
                    item_id = item["id"]

                    i1, i2, i3, i4, i5 = st.columns([3, 2, 2, 1, 1])

                    with i1:
                        avail_icon = "🟢" if item.get("available", True) else "🔴"
                        st.markdown(
                            f"<div style='font-family:\"Playfair Display\",serif;"
                            f"font-size:1rem;color:#F5F5F5;padding:0.5rem 0;'>"
                            f"{avail_icon} {item['name']}</div>",
                            unsafe_allow_html=True,
                        )
                    with i2:
                        st.markdown(
                            f"<div style='font-family:Inter,sans-serif;"
                            f"font-size:0.95rem;color:#C8A96E;"
                            f"padding:0.5rem 0;font-weight:600;'>"
                            f"{currency}{item['price']:.2f}</div>",
                            unsafe_allow_html=True,
                        )
                    with i3:
                        desc = item.get("description", "")
                        short = (desc[:35] + "…") if len(desc) > 35 else desc
                        st.markdown(
                            f"<div style='font-family:Inter,sans-serif;"
                            f"font-size:0.8rem;color:#A0A0B0;padding:0.5rem 0;'>"
                            f"{short or '—'}</div>",
                            unsafe_allow_html=True,
                        )
                    with i4:
                        lbl = "🔴 Hide" if item.get("available", True) else "🟢 Show"
                        # KEY uses counter — always unique
                        if st.button(lbl, key=f"tog_{wc}",
                                     use_container_width=True):
                            toggle_availability(item_id)
                            st.rerun()
                    with i5:
                        if st.button("🗑️", key=f"del_{wc}",
                                     help=f"Delete {item['name']}"):
                            ok, msg = delete_item(item_id)
                            if ok:
                                st.success(f"✅ {msg}")
                                st.rerun()

                    # Edit expander — also uses counter for all keys
                    with st.expander(f"✏️ Edit — {item['name']}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_name  = st.text_input(
                                "Name", value=item["name"],
                                key=f"en_{wc}")
                            e_cat   = st.selectbox(
                                "Category", categories,
                                index=categories.index(item["category"])
                                      if item["category"] in categories else 0,
                                key=f"ec_{wc}")
                            e_price = st.number_input(
                                "Price", value=float(item["price"]),
                                min_value=0.0, step=0.5, format="%.2f",
                                key=f"ep_{wc}")
                        with ec2:
                            e_desc = st.text_area(
                                "Description",
                                value=item.get("description", ""),
                                height=100, key=f"ed_{wc}")
                            e_img  = st.file_uploader(
                                "Replace Image",
                                type=["png","jpg","jpeg","webp"],
                                key=f"ei_{wc}")
                            curr_img = item.get("image_path", "")
                            if curr_img and Path(curr_img).exists():
                                st.image(curr_img, width=120,
                                         caption="Current image")

                        if st.button("💾 Save Changes",
                                     key=f"save_{wc}",
                                     use_container_width=True):
                            ok, msg = update_item(
                                item_id     = item_id,
                                name        = e_name,
                                category    = e_cat,
                                price       = e_price,
                                description = e_desc,
                                image_file  = e_img,
                            )
                            if ok:
                                st.success(f"✅ {msg}")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

                st.markdown("---")


# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 4 — QR CODE                                        ║
# ╚══════════════════════════════════════════════════════════╝
with tab4:
    st.markdown(
        "<div class='section-header'>📱 QR Code Generator</div>",
        unsafe_allow_html=True,
    )

    restaurant = get_restaurant()
    r_name     = restaurant.get("name", "")

    if not r_name:
        st.warning("⚠️ Please set your Restaurant Name in the "
                   "**Restaurant Info** tab first.")
    else:
        st.markdown(
            f"""
            <div style='font-family:Inter,sans-serif;font-size:0.95rem;
                        color:#A0A0B0;margin-bottom:1.5rem;'>
                Your QR code will link customers to the
                <b style='color:#C8A96E;'>Customer Menu</b> page.
                When scanned, it opens the digital menu directly in their browser.
            </div>
            """,
            unsafe_allow_html=True,
        )

        qcol1, qcol2 = st.columns([2, 3], gap="large")

        with qcol1:
            st.markdown("#### ⚙️ QR Code Settings")

            menu_url = st.text_input(
                "Menu URL",
                value="ttps://digitalrestaurant-menu-keuve2cmjlwjwylvpy4arv.streamlit.app/Customer_Menu",
                # help="When deployed, replace this with your Streamlit Cloud URL.",
            )
            qr_color    = st.color_picker("QR Code Color",    "#1A1A2E")
            bg_color    = st.color_picker("Background Color", "#FFFFFF")
            box_size    = st.slider("Size",   min_value=5,  max_value=15, value=10)
            border_size = st.slider("Border", min_value=1,  max_value=6,  value=4)

            st.markdown("<br>", unsafe_allow_html=True)
            generate_btn = st.button(
                "🔲 Generate QR Code",
                use_container_width=True,
                key="gen_qr",
            )

        with qcol2:
            st.markdown("#### 👁️ QR Code Preview")

            if generate_btn:
                st.session_state["qr_generated"] = True
                st.session_state["qr_url"]       = menu_url
                st.session_state["qr_color"]     = qr_color
                st.session_state["qr_bg"]        = bg_color
                st.session_state["qr_box_size"]  = box_size
                st.session_state["qr_border"]    = border_size

            if st.session_state.get("qr_generated"):
                try:
                    qr = qrcode.QRCode(
                        version          = 1,
                        error_correction = qrcode.constants.ERROR_CORRECT_H,
                        box_size         = st.session_state["qr_box_size"],
                        border           = st.session_state["qr_border"],
                    )
                    qr.add_data(st.session_state["qr_url"])
                    qr.make(fit=True)

                    qr_image = qr.make_image(
                        fill_color = st.session_state["qr_color"],
                        back_color = st.session_state["qr_bg"],
                    )

                    buf = io.BytesIO()
                    qr_image.save(buf, format="PNG")
                    buf.seek(0)
                    qr_bytes = buf.getvalue()

                    dc1, dc2, dc3 = st.columns([1, 2, 1])
                    with dc2:
                        st.image(qr_bytes, width=250,
                                 caption=f"QR → {r_name} Menu")

                    st.markdown("<br>", unsafe_allow_html=True)
                    safe_name = r_name.replace(" ", "_").lower()
                    st.download_button(
                        label    = "⬇️ Download QR Code (PNG)",
                        data     = qr_bytes,
                        file_name= f"{safe_name}_qr_menu.png",
                        mime     = "image/png",
                        use_container_width=True,
                    )
                    st.success(
                        f"✅ QR Code generated! Links to:\n"
                        f"`{st.session_state['qr_url']}`"
                    )

                except Exception as e:
                    st.error(f"❌ Error generating QR: {e}")
            else:
                st.markdown(
                    """
                    <div style='background:#16213E;
                    border:2px dashed rgba(200,169,110,0.2);
                    border-radius:12px;padding:3rem;text-align:center;
                    color:#606070;font-family:Inter,sans-serif;'>
                        📱<br><br>Configure settings on the left<br>
                        and click <b>Generate QR Code</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
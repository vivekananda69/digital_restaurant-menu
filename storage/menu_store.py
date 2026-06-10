# ============================================================
#  storage/menu_store.py
#  The single source of truth for all menu data.
#  Handles reading and writing to data/menu.json
# ============================================================

import json
import time
import uuid
import shutil
from pathlib import Path


# ── Constants ────────────────────────────────────────────────
DATA_DIR    = Path("data")
IMAGES_DIR  = DATA_DIR / "images"
MENU_FILE   = DATA_DIR / "menu.json"

# Default structure written on first run
DEFAULT_MENU = {
    "restaurant": {
        "name":            "",
        "tagline":         "",
        "logo_path":       "",
        "currency_symbol": "₹",
    },
    "categories": [],
    "menu_items": [],
}


# ── Internal Helpers ─────────────────────────────────────────

def _ensure_dirs() -> None:
    """Create data/ and data/images/ folders if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)


def _load_raw() -> dict:
    """
    Read menu.json from disk and return as a Python dict.
    If the file doesn't exist yet, create it with default values.
    """
    _ensure_dirs()
    if not MENU_FILE.exists():
        _save_raw(DEFAULT_MENU)
        return DEFAULT_MENU.copy()
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_raw(data: dict) -> None:
    """
    Write a Python dict to menu.json on disk.
    indent=2 makes the file human-readable (pretty-printed).
    """
    _ensure_dirs()
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Restaurant Info ──────────────────────────────────────────

def get_restaurant() -> dict:
    """Return the restaurant info block."""
    return _load_raw().get("restaurant", {})


def save_restaurant(name: str, tagline: str, currency_symbol: str) -> None:
    """Update restaurant name, tagline, and currency symbol."""
    data = _load_raw()
    data["restaurant"]["name"]            = name.strip()
    data["restaurant"]["tagline"]         = tagline.strip()
    data["restaurant"]["currency_symbol"] = currency_symbol.strip()
    _save_raw(data)


def save_logo(uploaded_file) -> str:
    """
    Save an uploaded logo image to data/images/logo.<ext>
    Returns the saved file path as a string.
    uploaded_file is a Streamlit UploadedFile object.
    """
    _ensure_dirs()
    # Get the file extension (.png, .jpg, etc.)
    suffix = Path(uploaded_file.name).suffix.lower()
    logo_path = IMAGES_DIR / f"logo{suffix}"

    with open(logo_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Store the path in JSON
    data = _load_raw()
    data["restaurant"]["logo_path"] = str(logo_path)
    _save_raw(data)

    return str(logo_path)


# ── Categories ───────────────────────────────────────────────

def get_categories() -> list:
    """Return the list of category name strings."""
    return _load_raw().get("categories", [])


def add_category(name: str) -> tuple[bool, str]:
    """
    Add a new category. Returns (success, message).
    Prevents duplicates (case-insensitive).
    """
    name = name.strip()
    if not name:
        return False, "Category name cannot be empty."

    data = _load_raw()
    existing = [c.lower() for c in data["categories"]]

    if name.lower() in existing:
        return False, f"Category '{name}' already exists."

    data["categories"].append(name)
    _save_raw(data)
    return True, f"Category '{name}' added successfully."


def delete_category(name: str) -> tuple[bool, str]:
    """
    Delete a category by name.
    Also removes all menu items that belong to this category.
    """
    data = _load_raw()

    if name not in data["categories"]:
        return False, f"Category '{name}' not found."

    # Remove category
    data["categories"].remove(name)

    # Remove all items in this category
    before = len(data["menu_items"])
    data["menu_items"] = [
        item for item in data["menu_items"]
        if item.get("category") != name
    ]
    removed_items = before - len(data["menu_items"])

    _save_raw(data)
    msg = f"Category '{name}' deleted."
    if removed_items:
        msg += f" Also removed {removed_items} menu item(s) in this category."
    return True, msg


def reorder_categories(new_order: list) -> None:
    """Save categories in a new order (for drag-and-drop style reordering)."""
    data = _load_raw()
    data["categories"] = new_order
    _save_raw(data)


# ── Menu Items ───────────────────────────────────────────────

def get_all_items() -> list:
    """Return all menu items as a list of dicts."""
    return _load_raw().get("menu_items", [])


def get_items_by_category(category: str) -> list:
    """Return only items belonging to a specific category."""
    return [
        item for item in get_all_items()
        if item.get("category") == category
    ]


def add_item(
    name:        str,
    category:    str,
    price:       float,
    description: str,
    image_file=None,
) -> tuple[bool, str]:
    """
    Add a new menu item.
    image_file is an optional Streamlit UploadedFile.
    Returns (success, message).
    """
    name = name.strip()
    if not name:
        return False, "Item name cannot be empty."
    if not category:
        return False, "Please select a category."
    if price < 0:
        return False, "Price cannot be negative."

    # Generate a unique ID using timestamp
    item_id = f"item_{uuid.uuid4().hex[:12]}"

    # Save image if provided
    image_path = ""
    if image_file is not None:
        image_path = _save_item_image(item_id, image_file)

    new_item = {
        "id":          item_id,
        "name":        name,
        "category":    category,
        "price":       float(price),
        "description": description.strip(),
        "image_path":  image_path,
        "available":   True,
    }

    data = _load_raw()
    data["menu_items"].append(new_item)
    _save_raw(data)
    return True, f"'{name}' added to {category}."


def update_item(
    item_id:     str,
    name:        str,
    category:    str,
    price:       float,
    description: str,
    image_file=None,
) -> tuple[bool, str]:
    """Update an existing menu item by its ID."""
    data = _load_raw()

    for item in data["menu_items"]:
        if item["id"] == item_id:
            item["name"]        = name.strip()
            item["category"]    = category
            item["price"]       = float(price)
            item["description"] = description.strip()

            # Replace image only if a new one is uploaded
            if image_file is not None:
                image_path = _save_item_image(item_id, image_file)
                item["image_path"] = image_path

            _save_raw(data)
            return True, f"'{name}' updated successfully."

    return False, f"Item with ID '{item_id}' not found."


def delete_item(item_id: str) -> tuple[bool, str]:
    """Delete a menu item by its ID. Also deletes its image file."""
    data = _load_raw()

    item_to_delete = next(
        (item for item in data["menu_items"] if item["id"] == item_id),
        None,
    )

    if item_to_delete is None:
        return False, "Item not found."

    # Delete image file from disk if it exists
    img_path = item_to_delete.get("image_path", "")
    if img_path and Path(img_path).exists():
        Path(img_path).unlink()

    # Remove from list
    data["menu_items"] = [
        item for item in data["menu_items"]
        if item["id"] != item_id
    ]
    _save_raw(data)
    return True, f"'{item_to_delete['name']}' deleted."


def toggle_availability(item_id: str) -> tuple[bool, str]:
    """Toggle an item between available and unavailable."""
    data = _load_raw()

    for item in data["menu_items"]:
        if item["id"] == item_id:
            item["available"] = not item.get("available", True)
            status = "available" if item["available"] else "unavailable"
            _save_raw(data)
            return True, f"'{item['name']}' marked as {status}."

    return False, "Item not found."


# ── Image Helper ─────────────────────────────────────────────

def _save_item_image(item_id: str, uploaded_file) -> str:
    """
    Save a food image to data/images/<item_id>.<ext>
    Returns the saved path as a string.
    """
    _ensure_dirs()
    suffix    = Path(uploaded_file.name).suffix.lower()
    img_path  = IMAGES_DIR / f"{item_id}{suffix}"

    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(img_path)


# ── Full Reset ───────────────────────────────────────────────

def reset_all_data() -> None:
    """
    Delete everything and start fresh.
    Removes menu.json and all uploaded images.
    Used for demo/testing purposes.
    """
    if MENU_FILE.exists():
        MENU_FILE.unlink()
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR)
    _ensure_dirs()
    _save_raw(DEFAULT_MENU)


# ── Quick Stats ──────────────────────────────────────────────

def get_stats() -> dict:
    """Return summary counts for the dashboard."""
    data = _load_raw()
    items = data.get("menu_items", [])
    return {
        "total_categories": len(data.get("categories", [])),
        "total_items":      len(items),
        "available_items":  sum(1 for i in items if i.get("available", True)),
        "restaurant_name":  data["restaurant"].get("name", ""),
    }
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="🛍 Katalog"), KeyboardButton(text="🛒 Savatcha")],
        [KeyboardButton(text="📦 Buyurtmalarim"), KeyboardButton(text="ℹ️ Ma'lumot")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def categories_keyboard(categories):
    kb = []
    for cat in categories:
        kb.append([InlineKeyboardButton(text=cat[1], callback_data=f"category_{cat[0]}")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def product_keyboard(product_id):
    kb = [
        [InlineKeyboardButton(text="➕ Savatchaga qo'shish", callback_data=f"add_to_cart_{product_id}")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_categories")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

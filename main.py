import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from database import db
from keyboards import main_menu, categories_keyboard, product_keyboard

load_dotenv()

# Logger sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot obyektini yaratish
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}! 👋\nKiyim do'konimizga xush kelibsiz.",
        reply_markup=main_menu()
    )

@dp.message(F.text == "🛍 Katalog")
async def show_categories(message: Message):
    categories = db.get_categories()
    if not categories:
        # Test uchun bir nechta kategoriya qo'shamiz agar bo'sh bo'lsa
        db.cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Erkaklar kiyimi",))
        db.cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Ayollar kiyimi",))
        db.connection.commit()
        categories = db.get_categories()
        
    await message.answer("Kategoriyani tanlang:", reply_markup=categories_keyboard(categories))

@dp.callback_query(F.data.startswith("category_"))
async def show_products(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    products = db.get_products_by_category(category_id)
    
    if not products:
        await callback.answer("Hozircha bu bo'limda mahsulotlar yo'q.", show_alert=True)
        return

    for product in products:
        text = f"👕 **{product[2]}**\n\n📝 {product[3]}\n\n💰 Narxi: {product[4]} so'm"
        if product[5]: # image_url
            await callback.message.answer_photo(product[5], caption=text, reply_markup=product_keyboard(product[0]))
        else:
            await callback.message.answer(text, reply_markup=product_keyboard(product[0]))
    
    await callback.answer()

@dp.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])
    # Note: In a real app, you'd store this in a 'cart' table in the DB
    # or use Dispatcher's FSM (Finite State Machine)
    await callback.answer("Mahsulot savatchaga qo'shildi! ✅", show_alert=False)

@dp.message(F.text == "🛒 Savatcha")
async def show_cart(message: Message):
    # This is a placeholder for actual cart logic
    await message.answer("Sizning savatchangiz hozircha bo'sh. 🛒\n\n(Bu qism tez orada yakunlanadi)")

@dp.message(F.text == "📦 Buyurtmalarim")
async def show_orders(message: Message):
    orders = db.get_user_orders(message.from_user.id)
    if not orders:
        await message.answer("Sizda hali buyurtmalar yo'q. 📦")
        return
    
    res = "Sizning oxirgi buyurtmalaringiz:\n\n"
    for order in orders:
        res += f"📄 Buyurtma #{order[0]}\n💰 Narxi: {order[3]} so'm\n📊 Holati: {order[4]}\n\n"
    await message.answer(res)

@dp.message(F.text == "ℹ️ Ma'lumot")
async def info_handler(message: Message):
    await message.answer("Bu kiyim do'koni boti orqali siz eng so'nggi modadagi kiyimlarni buyurtma qilishingiz mumkin.\n\nYordam uchun: @admin")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")

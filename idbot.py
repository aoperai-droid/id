# get_id_bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

# ---------------- КОНФИГ ----------------
BOT_TOKEN = "893982YkLjM4RwVkXA"  # Токен от @BotFather

# ---------------- ЛОГИРОВАНИЕ ----------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ---------------- ОБРАБОТЧИКИ ----------------

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 <b>Бот для получения ID</b>\n\n"
        "📝 <b>Как использовать:</b>\n"
        "• Добавь меня в группу/канал\n"
        "• Напиши <code>/id</code> в этом чате\n"
        "• Или перешли любое сообщение из нужного чата\n\n"
        "Я покажу ID чата и отправителя!",
        parse_mode="HTML"
    )

@dp.message(Command("id"))
async def get_chat_id(message: Message):
    chat = message.chat
    user = message.from_user
    
    # Информация о чате
    chat_type = chat.type
    chat_id = chat.id
    
    type_emoji = {
        "private": "👤",
        "group": "👥",
        "supergroup": "👥",
        "channel": "📢"
    }
    
    type_names = {
        "private": "Личка",
        "group": "Группа",
        "supergroup": "Супергруппа",
        "channel": "Канал"
    }
    
    response = (
        f"{type_emoji.get(chat_type, '❓')} <b>Информация о чате:</b>\n\n"
        f"📝 Название: <b>{chat.title if chat.title else 'Нет'}</b>\n"
        f"🆔 ID чата: <code>{chat_id}</code>\n"
        f"📋 Тип: {type_names.get(chat_type, chat_type)}\n"
    )
    
    if chat.username:
        response += f"🔗 Username: @{chat.username}\n"
    
    response += (
        f"\n👤 <b>Отправитель:</b>\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user.full_name}\n"
    )
    
    if user.username:
        response += f"🔗 Username: @{user.username}\n"
    
    await message.answer(response, parse_mode="HTML")

@dp.message(F.forward_from_chat)
async def forwarded_from_chat(message: Message):
    """Показывает ID чата из пересланного сообщения"""
    forward_chat = message.forward_from_chat
    
    await message.answer(
        "📨 <b>Пересланное сообщение из:</b>\n\n"
        f"📝 Название: <b>{forward_chat.title or 'Нет'}</b>\n"
        f"🆔 ID чата: <code>{forward_chat.id}</code>\n"
        f"📋 Тип: {forward_chat.type}\n"
        f"{f'🔗 Username: @{forward_chat.username}' if forward_chat.username else ''}",
        parse_mode="HTML"
    )

@dp.message(F.forward_from)
async def forwarded_from_user(message: Message):
    """Показывает ID пользователя из пересланного сообщения"""
    forward_user = message.forward_from
    
    await message.answer(
        "📨 <b>Пересланное сообщение от:</b>\n\n"
        f"🆔 ID: <code>{forward_user.id}</code>\n"
        f"👤 Имя: {forward_user.full_name}\n"
        f"{f'🔗 Username: @{forward_user.username}' if forward_user.username else ''}",
        parse_mode="HTML"
    )

@dp.message()
async def any_message(message: Message):
    """На любое другое сообщение показывает ID"""
    await get_chat_id(message)

# ---------------- ЗАПУСК ----------------
async def main():
    logger.info("Бот для получения ID запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

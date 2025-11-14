from aiogram import Router, types
from aiogram.filters import CommandStart

from bots.filters.isAdmin import IsAdmin
from keyboards import main_keyboard_handler
from database import add_user
start_router = Router()

@start_router.message(CommandStart(), IsAdmin())
async def start_command_handler(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer("Hello! Welcome to the bot. Use /help to see available commands.", reply_markup=await main_keyboard_handler())
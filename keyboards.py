from aiogram import types


async def main_keyboard_handler():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text="Analyze now")],
        [types.KeyboardButton(text="Choose folder")],
        [types.KeyboardButton(text="Configure GPT Request")],
    ])
    return keyboard

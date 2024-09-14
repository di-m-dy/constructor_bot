"""
This file contains all the menu keyboards that are used in the bot.
"""
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardMarkup


def admin_keyboard():
    """
    en: The admin keyboard.
    """
    buttons = [
        [InlineKeyboardButton(
            text="- Админ панель -",
            web_app=WebAppInfo(url="https://himmash-promenade.ru/admin"))],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def callback_keyboard(reply_buttons: list = None):
    buttons = []
    if reply_buttons:
        buttons += [
            [InlineKeyboardButton(text=item['button_text'], callback_data=item['callback'])]
            for item in reply_buttons
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


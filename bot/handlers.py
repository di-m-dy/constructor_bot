"""
Module for handling main requests
"""
import os
import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
import keyboards as kb
from config import BotMessage, Position, check_user, get_admins
from config import GOD_ID, MAIN_URL, WEB_APP_DIR
from config import API_BOT_MESSAGE, API_POSITION

router = Router()

bot_messages = BotMessage(API_BOT_MESSAGE)
bot_position = Position(API_POSITION)
# update data
bot_messages.get_update()
bot_position.get_update()


async def check_user_db(message: Message):
    """
    Check users in db
    """
    try:
        check_user(
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username
        )
    # adding new users
    except Exception as e:
        for admin in get_admins():
            await message.bot.send_message(
                chat_id=admin,
                text=f"Error adding user to db {e}"
            )


async def send_photo(
        message: Message | CallbackQuery,
        file: str,
        caption: str,
        reply_markup: any = None,
        file_id: str = None):
    """
    send file_id or file with adding file_id to db
    :return: Message or None
    """
    try:
        await message.answer_photo(
            photo=file_id,
            caption=caption,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    except Exception as e:
        await message.bot.send_message(chat_id=GOD_ID, text=f"error file_id: {e}")
        try:
            file_path = FSInputFile(file)
            send_file = await message.answer_photo(
                photo=file_path,
                caption=caption,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            return send_file.photo[-1].file_id
        except Exception as e:
            await message.bot.send_message(chat_id=GOD_ID, text=f"error file_path: {e}")
            await message.answer(caption, parse_mode='HTML', reply_markup=reply_markup)


async def send_audio(
        message: Message | CallbackQuery,
        file: str,
        reply_markup: any = None,
        file_id: str = None,
        caption: str = None,
        title: str = None,
        performer: str = None,
        thumbnail_path: str = None
):
    """
    send file_id or file with adding file_id to db
    """

    try:
        await message.answer_audio(
            audio=file_id,
            caption=caption,
            title=title,
            performer=performer,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    except Exception as e:
        await message.bot.send_message(chat_id=GOD_ID, text=f"error file_id: {e}")
        try:
            file_path = FSInputFile(file)
            if thumbnail_path:
                thumbnail_path = FSInputFile(thumbnail_path)
            send_file = await message.answer_audio(
                audio=file_path,
                caption=caption,
                performer=performer,
                thumbnail=thumbnail_path,
                title=title,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            return send_file.audio.file_id
        except Exception as e:
            await message.bot.send_message(chat_id=GOD_ID, text=f"error file_path: {e}")
            if caption:
                await message.answer(caption, parse_mode='HTML', reply_markup=reply_markup)
            else:
                await message.answer('error: no audio, no text', parse_mode='HTML', reply_markup=reply_markup)


async def send_message(
        message: Message | CallbackQuery,
        data: dict
):
    message_type = data.get('type')
    if message_type == 'simple':
        await message.answer(
            text=data['text'],
            reply_markup=kb.callback_keyboard(data['reply_markup']),
            parse_mode='HTML'
        )
    elif message_type == 'image':
        await send_photo(
            message=message,
            file=data['image']['path'],
            file_id=data['image']['file_id'],
            caption=data['caption'],
            reply_markup=kb.callback_keyboard(data['reply_markup'])
        )
    elif message_type == 'audio':
        await send_audio(
            message=message,
            file=data['audio']['path'],
            file_id=data['audio']['file_id'],
            caption=data['caption'],
            title=data['audio']['title'],
            performer=data['audio']['performer'],
            thumbnail_path=data['audio']['thumbnail']['path'] if data['audio']['thumbnail'] else None,
            reply_markup=kb.callback_keyboard(data['reply_markup'])
        )
    elif message_type == 'map':
        await message.answer_venue(
            latitude=data['location']['latitude'],
            longitude=data['location']['longitude'],
            title=data['location']['name'],
            address=data['location']['name'],
            reply_markup=kb.callback_keyboard(data['reply_markup'])
        )
    else:
        await message.answer('Нет данных')


@router.message(Command('update'))
async def update_data(message: Message):
    if int(message.from_user.id) in get_admins():
        try:
            bot_messages.get_update()
            bot_position.get_update()
            await message.answer('data updated')
        except Exception as e:
            await message.answer(f"Error: {e}")


@router.message(Command('admin_panel'))
async def admin_panel(message: Message):
    if int(message.from_user.id) in get_admins():
        await message.answer(
            "Войти в админ панель",
            reply_markup=kb.admin_keyboard()
        )


@router.callback_query(F.data.startswith('position_'))
async def user_position(call: CallbackQuery):
    """
    Handler for positions
    """
    positions = set(bot_position.position_list())
    if call.data not in positions:
        return
    position = bot_position.get_position(call.data)
    for item in position['messages']:
        await send_message(call.message, item)

    await call.answer(f"Position{position['position']}")


@router.message(F.text.startswith('/'))
async def user_command(message: Message):
    command_list = set(bot_messages.command_list())
    if message.text not in command_list:
        return
    command_data = bot_messages.get_command(message.text)
    if command_data['command'] == '/start':
        await check_user_db(message)
    text = command_data['text']
    reply_markup = kb.callback_keyboard(command_data['reply_markup'])
    if command_data['img']:
        image_id = command_data['img']['id']
        img_file_id = command_data['img']['file_id']
        img = command_data['img']['path']
        send_file = await send_photo(
            message=message,
            file_id=img_file_id,
            file=img,
            caption=text,
            reply_markup=reply_markup
        )
        if send_file:
            img_file_id = send_file
    else:
        await message.answer(text, reply_markup=reply_markup, parse_mode='HTML')

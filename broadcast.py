from time import time
from uuid import uuid4
from asyncio import sleep
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from info import DATABASE_URL
from bot.helper.telegram_helper.button_build import ButtonMaker
from other import new_task, get_readable_time, sendMessage, editMessage, DbManger

@Client.on_message(filters.incoming & filters.chat(BROADCAST_CHANNEL))
async def broadcast(bot: Client, message: Message):
    chat_id = BROADCAST_CHANNEL
    try:
        copied_message = await bot.copy_message(chat_id=chat_id, message_id=message.message_id)
        total_users = await db.total_users_count()
        s = 0
        time = time() 
        for user in total_users:
            await bot.send_message(chat_id=user, text=copied_message, disable_web_page_preview=True)
            await asyncio.sleep(0.2)
            s += 1
        f = total_users - s

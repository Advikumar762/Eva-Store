import asyncio
from typing import (
    Union
)
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    if (await is_invite_link(chat_id)):
        invite_link = await db.invite_link(chat_id, True, f'Invite Link by: {BOT_USERNAME}')
    else:
        try:
            invite_link = await bot.create_chat_invite_link(chat_id=chat_id, creates_join_request=True, name=f'Invite Link by: {BOT_USERNAME}')
            return invite_link
        except FloodWait as e:
            print(f"Sleep of {e.value}s caused by FloodWait ...")
            await asyncio.sleep(e.value)
            return invite_link

async def handle_force_sub(bot: Client, cmd: Message):
    if UPDATES_CHANNEL and UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(UPDATES_CHANNEL)
    elif UPDATES_CHANNEL and (not UPDATES_CHANNEL.startswith("-100")):
        channel_chat_id = UPDATES_CHANNEL
    else:
        return 200
    try:
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JoinOT).",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await db.get_invite_link(channel_chat_id)
        except Exception as err:
            print(f"Unable to do Force Subscribe to {UPDATES_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\n"
                 "Due to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Something went Wrong. Contact my.",
            disable_web_page_preview=True
        )
        return 200
    return 200 

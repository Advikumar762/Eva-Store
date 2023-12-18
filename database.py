import datetime
import motor.motor_asyncio
from plugins.info import DATABASE_URL, BOT_USERNAME

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.user = self.db.users
        self.link = self.db.links  

    async def new_user(self, id, name, time):
        user_info = {
            'user_id': id,
            'user_name': name,
            'joined_time': time
        }
        await self.user.insert_one(user_info)

    async def is_user(self, id):
        user_info = await self.user.find_one({'user_id': int(id)})
        return True if user_info else False

    async def new_link(self, id, s_link, f_link):
        link_info = {
            'link_owner': id,
            'stored_link': s_link,
            'final_link': f_link,
        }
        await self.link.insert_one(link_info)

    async def is_link(self, id):
        link_info = await self.link.find_one({'link_owner': int(id)})
        return True if link_info else False

    async def users_count(self):
        total_users_count = await self.user.count_documents({})
        return total_users_count

    async def users_list(self):
        all_users = await self.user.find({}).to_list(length=None)
        return all_users

    async def ban_user(self, id, banned_on, ban_duration, ban_reason):
        ban_info = {
            'user_id': id,
            'banned_on': banned_on,
            'ban_duration': ban_duration,
            'ban_reason': ban_reason,
            'is_banned': True
        }
        await self.user.update_one({'user_id': id}, {'$set': {'is_banned': True}})
        
    async def unban_user(self, id):
        is_banned = False
        await self.user.update_one({'user_id': id}, {'$set': {'is_banned': is_banned}})
        
    async def increase_count(self, link):
        count = await self.link_count(link)
        return count + 1
        
    async def link_count(self, link):
        total_link_count = await self.link.count_documents({'stored_link': link})
        return total_link_count

db = Database(DATABASE_URL, BOT_USERNAME) 

def add_user(bot: Client, cmd: Message):
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id)
        if LOG_CHANNEL is not None:
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
    )

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        await bot.send_message(
            Config.LOG_CHANNEL,
            f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned to Use This Bot 🥺", quote=True)
            return
    await cmd.continue_propagation()

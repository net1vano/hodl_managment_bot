from typing import List
from aiogram import Bot
from utils.roles import get_users_by_role

async def broadcast(bot: Bot, text:str, roles: List[str]):
    user_ids = get_users_by_role(*roles)
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception:
            # Пользователь мог заблокировать бота
            pass
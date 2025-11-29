from functools import wraps
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.locales import BotResponse as Resp
from keyboards import unauth_menu
from utils.auth import get_user_role, get_user_alias, get_users_by_role, get_user_by_id

ROLES = ["admin", "worker"]

def require_role(required_role: str):
    """
    Декоратор для проверки роли пользователя
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
            user_id = message.from_user.id
            role = get_user_role(user_id)

            if role != required_role:
                alias = get_user_alias(user_id) or str(user_id)
                await message.answer(Resp.ACCESS_DENIED.value.format(alias, required_role), reply_markup=unauth_menu)
                await state.clear()
                return

            # Обновляем роль и alias в FSM, чтобы в обработчике можно было использовать
            await state.update_data(role=role, alias=get_user_alias(user_id) or str(user_id))
            return await func(message, state, *args, **kwargs)

        return wrapper
    return decorator

def require_any_role(*allowed_roles: str):
    """
    Декоратор для проверки, что у пользователя есть одна из разрешённых ролей
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
            user_id = message.from_user.id
            role = get_user_role(user_id)
            if role not in allowed_roles:
                alias = get_user_alias(user_id) or str(user_id)
                await message.answer(Resp.ACCESS_DENIED.value.format(alias, ", ".join(allowed_roles)), reply_markup=unauth_menu)
                await state.clear()
                return

            await state.update_data(role=role, alias=get_user_alias(user_id) or str(user_id))
            return await func(message, state, *args, **kwargs)

        return wrapper
    return decorator
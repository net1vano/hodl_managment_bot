from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu, unauth_menu
from keyboards.keyboard_factory import get_keyboard


from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext
from utils.roles import  require_role, require_any_role, get_user_role, ROLES
from utils.locales import BotResponse as Resp




router = Router()


@require_any_role(*ROLES)
@router.message(Command("start"))
async def cmd_test(message: Message, state: FSMContext):
    # await message.delete()
    role = get_user_role(message.from_user.id)
    await state.set_state(MenuStates.main_menu)
    await message.answer(Resp.CHOOSE.value, reply_markup=get_keyboard(role=role, page="main_menu"))



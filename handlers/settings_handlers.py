from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.types.inaccessible_message import InaccessibleMessage
from keyboards import main_menu, worker_menu,settings_menu, shift_menu
#from utils.api_client import fetch_language_from_api
from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext
from utils.locales import BotResponse as Resp
from utils.roles import get_user_role
import logging

from keyboards.keyboard_factory import get_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "worker")
async def handle_worker(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.worker_menu)
    shift = await state.get_data()
    if shift.get("shift"):
        menu = get_keyboard(role="worker", page="shift_open")
    else:
        menu = get_keyboard(role="worker", page="worker")
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=menu)
    await callback.answer()

@router.callback_query(lambda c: c.data == "notif")
async def handle_notif(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    #await state.set_state(MenuStates.worker_menu)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=main_menu)
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_settings")
async def handle_back_to_settings(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.settings_menu)
    role = get_user_role(callback.from_user.id)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=get_keyboard(role=role, page="settings"))
    await callback.answer()

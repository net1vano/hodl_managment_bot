from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards import main_menu, worker_menu, settings_menu, shift_menu
#from utils.api_client import fetch_language_from_api
from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext
from utils.auth import get_user_role, add_user_to_file, update_user_role
from utils.locales import BotResponse as Resp
from keyboards.keyboard_factory import get_keyboard
import logging



router = Router()

@router.callback_query(lambda c: c.data == "main_worker")
async def handle_main_worker(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.main_worker)
    shift = await state.get_data()
    if shift.get("shift"):
        menu = get_keyboard(role="worker", page="shift_open")
    else:
        menu = get_keyboard(role="worker", page="shift_menu")
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=menu)
    await callback.answer()

@router.callback_query(lambda c: c.data == "helper")
async def handle_helper(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.helper_worker)
    shift = await state.get_data()
    if shift.get("shift"):
        menu = get_keyboard(role="worker", page="shift_open")
    else:
        menu = get_keyboard(role="worker", page="shift_menu")
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=menu)
    await callback.answer()


@router.callback_query(lambda c: c.data == "newbie")
async def handle_newbie(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.newbie_worker)
    shift = await state.get_data()
    if shift.get("shift"):
        menu = get_keyboard(role="worker", page="shift_open")
    else:
        menu = get_keyboard(role="worker", page="shift_menu")
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=menu)
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_settings")
async def handle_back_to_settings(callback: CallbackQuery, state: FSMContext):
    role = get_user_role(callback.from_user.id)
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.settings_menu)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=get_keyboard(role=role, page="settings"))
    await callback.answer()


import logging

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.types.inaccessible_message import InaccessibleMessage

from keyboards import *
#from utils.api_client import fetch_language_from_api
from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext

from utils.auth import add_user_to_file, update_user_role, update_user_alias, load_users, delete_user
from utils.roles import  require_role, require_any_role, get_user_role, get_users_by_role
from utils.locales import BotResponse as Resp
from utils.broadcaster import broadcast



router = Router()

@require_role("admin")
@router.callback_query(lambda c: c.data == "add_worker")
async def handle_admin_add_worker(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.waiting_for_number)
    await callback.message.answer(Resp.ADD_USER.value)
    await callback.answer()

@router.message(MenuStates.waiting_for_number)
async def handle_number_input(message: Message, state: FSMContext):
    try:
        number = int(message.text)
        await state.update_data(user_id=number)
        await message.answer(Resp.CHOOSE_ROLE.value, reply_markup=admin_add_worker_inline_menu)
        await state.set_state(MenuStates.waiting_for_role)
    except ValueError:
        await message.answer("❌ Это не число. Попробуйте снова.")

@router.callback_query(lambda c: c.data.startswith("role:"), MenuStates.waiting_for_role)
async def handle_choose_role(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    role = callback.data.split(":", 1)[1]
    await state.update_data(user_role=role)
    await callback.message.answer(Resp.ADD_ALIAS.value)
    await state.set_state(MenuStates.waiting_for_alias)

@router.message(MenuStates.waiting_for_alias)
async def handle_input_alias(message: Message, state: FSMContext):
    try:
        await message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await message.answer(Resp.ADD_ALIAS.value)
    user_name = message.text
    data = await state.get_data()
    add_user_to_file(user_id=data['user_id'], role=data['user_role'], alias=user_name)
    await message.answer(Resp.USER_ADDED.value.format(data['user_id'], data['user_role']), reply_markup=main_menu)
    await state.clear()

@require_role("admin")
@router.callback_query(lambda c: c.data == "list_workers")
async def handle_admin_list_users(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await callback.message.answer(Resp.ADD_USER.value, reply_markup=form_list())


@require_role("admin")
@router.callback_query(lambda c: c.data == "change_role")
async def handle_admin_change_role(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.update_role)
    await callback.message.answer(Resp.CHOOSE_ROLE.value, reply_markup=admin_add_worker_inline_menu)

@router.callback_query(lambda c: c.data.startswith("user:"))
async def handle_choose_role(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    user_id = callback.data.split(":")[1]
    await state.update_data(user_id=user_id)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=admin_user_page)

@router.callback_query(lambda c: c.data.startswith("role:"), MenuStates.update_role)
async def handle_update_role(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    role = callback.data.split(":", 1)[1]
    data = await state.get_data()
    update_user_role(user_id=int(data['user_id']), new_role=role)
    await callback.message.answer(Resp.USER_UPDATED.value.format(data['user_id'], role), reply_markup=main_menu)
    await state.clear()

@require_role("admin")
@router.callback_query(lambda c: c.data == "change_alias")
async def handle_admin_change_alias(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await callback.message.answer(Resp.ADD_ALIAS.value)
    await state.set_state(MenuStates.update_alias)

@router.message(MenuStates.update_alias)
async def handle_update_alias(message: Message, state: FSMContext):
    try:
        await message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    user_name = message.text
    data = await state.get_data()
    update_user_alias(user_id=int(data['user_id']), new_alias=user_name)
    await message.answer(Resp.AlIAS_UPDATED.value.format(user_name), reply_markup=main_menu)
    await state.clear()

@require_role("admin")
@router.callback_query(lambda c: c.data == "delete_user")
async def handle_admin_delete_user(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    data = await state.get_data()
    delete_user(int(data['user_id']))
    await callback.message.answer(Resp.USER_DELETED.value.format(data['user_id']), reply_markup=main_menu)
    await state.clear()
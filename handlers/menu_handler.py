from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.types.inaccessible_message import InaccessibleMessage

from keyboards import *
from keyboards.all_keyboard import main_menu
#from utils.api_client import fetch_language_from_api
from keyboards.keyboard_factory import get_keyboard

from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext
from keyboards.keyboard_factory import get_keyboard
from APIs.auth import Spreads
from utils.my_utils import  current_month, current_year, start_timer, subtract_months, calculate_duration
from utils.roles import  require_role, require_any_role, get_user_role, get_users_by_role, get_user_alias
from utils.locales import BotResponse as Resp
from utils.broadcaster import broadcast
from utils.stats_dataclass import months_int, months, AllData
from datetime import datetime
import logging

from pprint import pprint

gc = Spreads()

data = None

async def refresh_data():
    global data
    if data is not None:
         if calculate_duration(data.timestamp, datetime.now()) > 4.0:
             data = await gc.parse_data_to_dataclass(await gc.get_sheet_data("Расчетный лист!1:1000"))
    else:
        data = await gc.parse_data_to_dataclass(await gc.get_sheet_data("Расчетный лист!1:1000"))
    return data





router = Router()
@require_any_role(*["worker", "admin"])
@router.callback_query(lambda c: c.data == "stats")
async def handle_stats(callback: CallbackQuery, state: FSMContext):
    role = get_user_role(callback.from_user.id)
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    global data
    data = await refresh_data()
    date = start_timer()
    parse_months = [subtract_months(date, months=2), subtract_months(date, months=1), date]
    parse_months = [f'{x.year}:{x.month}' for x in parse_months]
    if role != "unauthorized":
        await callback.message.answer(Resp.CHOOSE.value, reply_markup=generate_months_menu(parse_months)) #TODO добавить потом функционал
    else:
        await callback.message.answer(Resp.ACCESS_DENIED.value,reply_markup=get_keyboard(role, page="main_menu"))
    await callback.answer()

@require_any_role(*["worker", "admin"])
@router.callback_query(lambda c: c.data.startswith("month:"))
async def handle_choose_month(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    global data
    data = await refresh_data()
    year = callback.data.split(":")[1]
    month = int(callback.data.split(":")[-1])
    info = ""
    for person in data.get(year).get(month):
        if person.name == get_user_alias(callback.from_user.id):
            info = person
            await callback.message.answer(
            f"Месяц {months_int[month]}: \n\n 💳 Ваш остаток: {info.balance} \n\n 💰 Всего за месяц:{info.total_amount}")
    if info == "":
        await callback.message.answer(Resp.ERROR_OCCURRED.value.format("нет данных"), reply_markup=main_menu)

@require_any_role(*["worker", "admin"])
@router.callback_query(lambda c: c.data == "support")
async def handle_support(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=main_menu) #TODO добавить потом функционал, кнопка выкл
    await callback.answer()

@require_any_role(*["worker", "admin"])
@router.callback_query(lambda c: c.data == "settings")
async def handle_settings(callback: CallbackQuery, state: FSMContext):
    role = get_user_role(callback.from_user.id)
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.settings_menu)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=get_keyboard(role=role, page="settings"))
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_main")
async def handle_settings(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.main_menu)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=main_menu)
    await callback.answer()

@require_any_role(*["unauthorized"])
@router.callback_query(lambda c: c.data == "request_for")
async def handle_unath(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    auth_name = callback.from_user.username
    text = f'Пользователь @{auth_name}  id={callback.from_user.id} запросил доступ'
    await broadcast(bot, text,["admin"])
    await state.clear()
    await callback.message.answer(Resp.UNAUTHORIZED.value)


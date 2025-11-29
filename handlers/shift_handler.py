import logging

from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.types.inaccessible_message import InaccessibleMessage

from keyboards import main_menu, worker_menu,settings_menu
#from utils.api_client import fetch_language_from_api
from states.user_states import MenuStates
from aiogram.fsm.context import FSMContext
from utils.my_utils import start_timer, calculate_duration, POSITIONS
from datetime import datetime
from APIs.auth import Spreads
from utils.auth import get_user_role, add_user_to_file, update_user_role, get_user_alias
from utils.locales import BotResponse as Resp
from keyboards.keyboard_factory import get_keyboard
from utils.broadcaster import broadcast

position = {"main_worker": "о", "helper_worker": "п", "newbie": "с"}
position_worker = {"main_worker": "Основной бариста", "helper_worker": "Помощник", "newbie": "Стажёр"}

router = Router()
gc = Spreads()

@router.callback_query(lambda c: c.data == "open_shift")
async def handle_open_shift(callback: CallbackQuery, state: FSMContext, bot: Bot):
    start_time = start_timer()
    curr = await state.get_state()
    await state.update_data(user_id = callback.from_user.id,
                            shift=True,
                            worker_position=curr.split(sep=':')[1],
                            start_time=start_time.timestamp())
    data = await state.get_data()
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")

    await callback.message.answer(Resp.SHIFT_OPEN.value.format(POSITIONS.get(curr.split(sep=":")[1]),
                                                               start_time.strftime("%d-%m-%Y %H:%M:%S")))
    await broadcast(bot,
                    text=Resp.BROADCAST_SHIFT_OPENED.value.format(
                        get_user_alias(int(data['user_id'])),
                              position_worker[data['worker_position']],
                             start_time.strftime("%d-%m-%Y %H:%M:%S"),
                    ),
                    roles=["admin"])
    await callback.answer()




@router.callback_query(lambda c: c.data == "close_shift")
async def handle_close_shift(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    shift = await state.get_data()
    shift = shift.get("shift", None)
    if shift is False or None or not shift:
        await callback.message.answer(Resp.ERROR_OCCURRED.value.format("время начала не найдено."))
        await state.clear()
        return
    start_time = datetime.fromtimestamp(data.get("start_time"))
    if not start_time:
        await callback.message.answer(Resp.ERROR_OCCURRED.value.format("время начала не найдено."))
        await state.clear()
        return
    end_time = datetime.now()
    await state.update_data(end_time=end_time.timestamp())
    duration = calculate_duration(start_time, end_time)
    if duration >= 0.5:
        data_to_send = [start_time.strftime("%d-%m-%Y"),
                        get_user_alias(int(data["user_id"])),
                        duration,
                        position[data["worker_position"]],
                        start_time.strftime("%H:%M:%S"),
                        end_time.strftime("%H:%M:%S")]
        await gc.append_row_data([data_to_send])
        await state.update_data(shift_open=False)
    else:
        logging.warning("Время работы меньше получаса - отмена отправки в таблицу")

    await broadcast(bot,
                    text=Resp.BROADCAST_SHIFT_CLOSED.value.format(
                        get_user_alias(int(data['user_id'])),
                              position_worker[data['worker_position']],
                              end_time.strftime("%d-%m-%Y %H:%M:%S"),
                    ),
                    roles=["admin"])
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.clear()
    await callback.message.answer(Resp.SHIFT_CLOSED.value.format(end_time.strftime("%d-%m-%Y %H:%M:%S"),
                                                                 duration))


@router.callback_query(lambda c: c.data == "back_to_worker")
async def handle_worker(callback: CallbackQuery, state: FSMContext):
    role = get_user_role(callback.message.from_user.id)
    try:
        await callback.message.delete()
    except Exception as error:
        logging.warning(f"Bot trying to delete non existing message: {error}")
    await state.set_state(MenuStates.worker_menu)
    await callback.message.answer(Resp.CHOOSE.value, reply_markup=get_keyboard(role=role, page="worker"))
    await callback.answer()

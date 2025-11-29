from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.stats_dataclass import *
from utils.my_utils import current_month, current_year, subtract_months

stats_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Остаток", callback_data="cash_remains")],
        [InlineKeyboardButton(text="🔔 Общая сумма", callback_data="full_salary")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)


def generate_months_menu(gen_months: list):
    data = []
    for month in gen_months:
        data.append([InlineKeyboardButton(text=months_int[int(month.split(sep=":")[1])], callback_data=f"month:{month}")])
    data.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=data)


stats_months_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Остаток", callback_data="cash_remains")],
        [InlineKeyboardButton(text="🔔 Общая сумма", callback_data="full_salary")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)

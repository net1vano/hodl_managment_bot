from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


shift_inline_menu_opened  = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть смену", callback_data="close_shift")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_worker")]
    ]
)

shift_inline_menu_no_shift  = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Открыть смену", callback_data="open_shift")],
        [InlineKeyboardButton(text="Закрыть смену", callback_data="close_shift")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_worker")]
    ]
)
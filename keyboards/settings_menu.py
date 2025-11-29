from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings_inline_base_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Сотрудник", callback_data="worker")],
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notif")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)

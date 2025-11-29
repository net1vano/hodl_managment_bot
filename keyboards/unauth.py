from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

unauth_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Запросить доступ", callback_data="request_for")],
    ]
)
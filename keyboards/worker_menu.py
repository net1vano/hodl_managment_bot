from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

chooser_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Основной работник", callback_data="main_worker")],
        [InlineKeyboardButton(text="Помощник", callback_data="helper")],
        [InlineKeyboardButton(text="Стажер", callback_data="newbie")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]
    ]
)

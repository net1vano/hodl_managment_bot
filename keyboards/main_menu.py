from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="⚙️ Учет времени", callback_data="settings")],
        #[InlineKeyboardButton(text="📞 inprogress", callback_data="support")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)

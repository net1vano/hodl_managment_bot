from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.auth import load_users


## ADMIN WORKER MENU
admin_settings_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👤 Сотрудник", callback_data="worker")],
        [InlineKeyboardButton(text="🌐 Добавить сотрудника", callback_data="add_worker")],
        [InlineKeyboardButton(text="👥 Список сотрудников", callback_data="list_workers")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)

##ADMIN ADDER MENU
admin_add_worker_inline_menu =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Работник", callback_data="role:worker")],
        [InlineKeyboardButton(text="🌐 Администратор", callback_data="role:admin")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ]
)

def form_list():
    users = load_users()
    menu = []
    for user_id, info in users.items():
        text = "🤖 " + info['alias'] if info['role'] == "admin" else "👤 " + info['alias']
        button = [InlineKeyboardButton(text=text, callback_data=f"user:{user_id}")]
        menu.append(button)
    menu.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    formed_menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return formed_menu


admin_user_page = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Поменять роль", callback_data="change_role")],
        [InlineKeyboardButton(text="✏️ Поменять имя", callback_data="change_alias")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data="delete_user")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_list")]
    ]
)

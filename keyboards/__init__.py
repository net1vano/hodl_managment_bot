from .main_menu import main_inline_menu as main_menu
from .settings_menu import settings_inline_base_menu as settings_menu
from .shift_menu import shift_inline_menu_no_shift as shift_menu
from .shift_menu import shift_inline_menu_opened as shift_open
from .worker_menu import chooser_inline_menu as worker_menu
from .unauth import unauth_inline_menu as unauth_menu
from .admin_keyboard import admin_add_worker_inline_menu,  admin_settings_inline_menu, form_list, admin_user_page
from .stats_keyboard import generate_months_menu, stats_months_inline_menu, stats_inline_menu

__all__ = [
    "main_menu",
    "settings_menu",
    "shift_menu",
    "worker_menu",
    "unauth_menu",
    "admin_add_worker_inline_menu",
    "admin_settings_inline_menu",
    "form_list",
    "admin_user_page",
    "generate_months_menu",
    "stats_inline_menu",
    "stats_months_inline_menu"
]
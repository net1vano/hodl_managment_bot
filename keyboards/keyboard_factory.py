from keyboards import admin_keyboard, main_menu, settings_menu, shift_menu, worker_menu, unauth_menu, \
    admin_settings_inline_menu, stats_months_inline_menu, generate_months_menu, stats_inline_menu
from keyboards.shift_menu import shift_inline_menu_no_shift, shift_inline_menu_opened

ALL_MENUS = {
    'main_menu': {'admin': main_menu,
                  'worker': main_menu,
                  'unauthorized': unauth_menu},
    'stats': {'admin': stats_inline_menu,
                  'worker': stats_inline_menu,
                  'unauthorized': unauth_menu},
    'settings': {'admin': admin_settings_inline_menu,
                  'worker': settings_menu,
                  'unauthorized': unauth_menu},
    'worker': {'admin': worker_menu,
               'worker': worker_menu,
                'unauthorized': unauth_menu},
    'shift_menu': {'admin': shift_inline_menu_no_shift,
                   'worker': shift_inline_menu_no_shift,
                   'unauthorized': unauth_menu},
    'shift_open': {'admin': shift_inline_menu_opened,
                   'worker': shift_inline_menu_opened,
                   'unauthorized': unauth_menu},

}

def get_keyboard(role: str, page:str):
    return ALL_MENUS.get(page).get(role)
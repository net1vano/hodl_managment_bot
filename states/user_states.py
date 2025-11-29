from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    main_menu = State()
    worker_menu = State()
    settings_menu = State()
    shift_menu = State()

    main_worker = State()
    helper_worker = State()
    newbie_worker = State()

    waiting_for_finish = State()
    waiting_for_number = State()
    waiting_for_role = State()
    waiting_for_alias = State()

    update_role = State()
    update_alias = State()

    worker_position = State()
    shift_open = State()
    shift_closed = State()

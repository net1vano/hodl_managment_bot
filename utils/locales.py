from enum import Enum

class BotResponse(Enum):
    # Простые сообщения
    WELCOME = "Добро пожаловать!"
    CHOOSE = "Выберите действие:"
    UNAUTHORIZED = "❌ Вы не авторизованы. Обратитесь к администратору."
    ACCESS_DENIED = "❌ У вас нет прав для выполнения этой команды. Требуется роль: {}"

    USER_ADDED = "✅ Пользователь {} добавлен с ролью: {}"
    USER_UPDATED = "✅ Роль пользователя {} обновлена на: {}"
    USER_NOT_FOUND = "❌ Пользователь {} не найден."
    USER_ALREADY_EXISTS = "⚠️ Пользователь {} уже существует с ролью: {}. Используйте /update_role, чтобы изменить."
    USAGE_ADD_USER = "❌ Использование: /add_user <user_id> <role>"
    USAGE_UPDATE_ROLE = "❌ Использование: /update_role <user_id> <role>"
    ROLE_INVALID = "❌ Роль должна быть: admin или participant"
    USER_ID_INVALID = "❌ user_id должен быть числом."
    ERROR_OCCURRED = "❌ Ошибка: {}"
    SHIFT_OPEN = "✅ Смена открыта как {}!\n\n {}"
    SHIFT_CLOSED = "✅ Смена закрыта!\n\n{}\n\n Время работы: {} часов."
    ADD_USER = "⚠️ Введите ID пользователя."
    CHOOSE_ROLE = "⚠️ Выберите роль пользователя"
    ADD_ALIAS = "⚠️ Выберите имя пользователя"
    AlIAS_UPDATED ="✅ Имя пользователя обновлено на {}"
    USER_DELETED = "✅ Пользователь {} удалён"
    BROADCAST_SHIFT_OPENED = "✅ {} открыл смену как {} в {}."
    BROADCAST_SHIFT_CLOSED = "✅ {} закрыл смену как {} в {}."


    # Можно добавлять больше
    START_MESSAGE = "Привет, {}! Вы авторизованы как: {}"
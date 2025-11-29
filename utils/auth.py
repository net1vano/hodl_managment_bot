from typing import Optional, Dict, List

USER_FILE = 'users.txt'

def load_users() -> Dict[int, Dict[str, str]]:
    """
    Возвращает словарь: { user_id: {'role': '...', 'alias': '...'} }
    """
    users = {}
    try:
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(':', 2)  # Разбиваем на 3 части: id, role, alias
                    if len(parts) == 3:
                        user_id, role, alias = parts
                        users[int(user_id)] = {'role': role, 'alias': alias}
    except FileNotFoundError:
        pass
    return users

def get_user_role(user_id: int) -> str:
    users = load_users()
    return users.get(user_id, {}).get('role', 'unauthorized')

def get_user_alias(user_id: int) -> Optional[str]:
    users = load_users()
    return users.get(user_id, {}).get('alias')

def get_users_by_role(target_role: str) -> List[int]:
    """
    Возвращает список user_id, у которых роль = target_role
    """
    users = load_users()
    return [user_id for user_id, data in users.items() if data['role'] == target_role]

def get_user_by_id(user_id: int) -> Optional[Dict[str, str]]:
    users = load_users()
    return users.get(user_id)

def save_users(users: Dict[int, Dict[str, str]]):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        for uid, data in users.items():
            f.write(f"{uid}:{data['role']}:{data['alias']}\n")

def add_user_to_file(user_id: int, role: str, alias: str):
    users = load_users()
    users[user_id] = {'role': role, 'alias': alias}
    save_users(users)

def update_user_role(user_id: int, new_role: str) -> bool:
    users = load_users()
    if user_id not in users:
        return False  # Пользователь не найден
    users[user_id]['role'] = new_role
    save_users(users)
    return True

def update_user_alias(user_id: int, new_alias: str) -> bool:
    users = load_users()
    if user_id not in users:
        return False  # Пользователь не найден
    users[user_id]['alias'] = new_alias
    save_users(users)
    return True

def delete_user(user_id: int,) -> bool:
    users = load_users()
    if user_id in users:
        users.pop(user_id)
        save_users(users)
        return True
    return False

def get_all_aliases() -> List[int]:
    names = []
    users = load_users()
    for user_id in users:
        names.append(users[user_id]['alias'])
    return names


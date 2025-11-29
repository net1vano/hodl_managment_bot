from .start import router as start_router
from .menu_handler import router as menu_router
from .settings_handlers import router as settings_router
from .shift_handler import router as shift_router
from .worker_handler import router as worker_router
from .admin_handler import router as admin_router

__all__ = [
    "start_router",
    "menu_router",
    "settings_router",
    "worker_router",
    "shift_router",
    "admin_router"
]
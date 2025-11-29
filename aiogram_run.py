import asyncio
from create_bot import bot, dp, scheduler
from handlers import *
# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(shift_router)
    dp.include_router(menu_router)
    dp.include_router(settings_router)
    dp.include_router(worker_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())